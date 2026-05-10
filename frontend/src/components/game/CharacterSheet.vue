<template>
  <div class="character-sheet" :class="{ 'is-npc': char.is_npc }">
    <!-- Header -->
    <div class="sheet-header">
      <span class="sheet-icon">
        <img v-if="char.avatar" :src="char.avatar" class="sheet-avatar-img" />
        <span v-else>{{ char.is_npc ? '👾' : '🧑' }}</span>
      </span>
      <div class="sheet-title">
        <span class="sheet-name">{{ char.name }}</span>
        <span v-if="char.profession" class="sheet-profession">{{ char.profession }}</span>
      </div>
      <span v-if="char.is_npc" class="sheet-tag npc">NPC</span>
      <div v-if="isGM" class="sheet-actions">
        <AppButton v-if="showPlaceOnMap" size="small" variant="secondary" @click="$emit('place-on-map', char)" title="放置到地图">📍</AppButton>
        <AppButton size="small" variant="ghost" @click="$emit('edit', char)">✎</AppButton>
        <AppButton size="small" variant="ghost" @click="$emit('delete', char)">✕</AppButton>
      </div>
    </div>

    <!-- HP / SAN / MP bars -->
    <div class="bar-group">
      <div class="stat-bar-row" @click="isGM && startEdit('hp')">
        <span class="bar-label">HP</span>
        <div class="bar-track hp-track">
          <div class="bar-fill hp-fill" :style="{ width: barPercent(char.hp, char.max_hp) }"></div>
        </div>
        <span class="bar-value" :class="{ editable: isGM }">
          <template v-if="editing === 'hp'">
            <input ref="editInput" v-model.number="editValue" class="inline-edit" type="number" :min="0" :max="char.max_hp" @keydown.enter="saveEdit" @keydown.escape="cancelEdit" @blur="saveEdit" />
          </template>
          <template v-else>{{ char.hp }}/{{ char.max_hp }}</template>
        </span>
      </div>

      <div class="stat-bar-row" @click="isGM && startEdit('san')">
        <span class="bar-label">SAN</span>
        <div class="bar-track san-track">
          <div class="bar-fill san-fill" :style="{ width: barPercent(char.san, willpower) }"></div>
        </div>
        <span class="bar-value" :class="{ editable: isGM }">
          <template v-if="editing === 'san'">
            <input ref="editInput" v-model.number="editValue" class="inline-edit" type="number" :min="0" :max="willpower" @keydown.enter="saveEdit" @keydown.escape="cancelEdit" @blur="saveEdit" />
          </template>
          <template v-else>{{ char.san }}/{{ willpower }}</template>
        </span>
      </div>

      <div v-if="char.max_mp > 0" class="stat-bar-row" @click="isGM && startEdit('mp')">
        <span class="bar-label">MP</span>
        <div class="bar-track mp-track">
          <div class="bar-fill mp-fill" :style="{ width: barPercent(char.mp, char.max_mp) }"></div>
        </div>
        <span class="bar-value" :class="{ editable: isGM }">
          <template v-if="editing === 'mp'">
            <input ref="editInput" v-model.number="editValue" class="inline-edit" type="number" :min="0" :max="char.max_mp" @keydown.enter="saveEdit" @keydown.escape="cancelEdit" @blur="saveEdit" />
          </template>
          <template v-else>{{ char.mp }}/{{ char.max_mp }}</template>
        </span>
      </div>
    </div>

    <!-- Six attributes (compact 2-col) -->
    <div class="attr-grid">
      <div v-for="attr in attributeList" :key="attr.key" class="attr-item" @click="isGM && startEditAttr(attr.key)">
        <span class="attr-label">{{ attr.label }}</span>
        <span class="attr-value" :class="{ editable: isGM }">
          <template v-if="editing === 'attr_' + attr.key">
            <input ref="editInput" v-model.number="editValue" class="inline-edit inline-edit-sm" type="number" :min="1" :max="99" @keydown.enter="saveEditAttr(attr.key)" @keydown.escape="cancelEdit" @blur="saveEditAttr(attr.key)" />
          </template>
          <template v-else>{{ attr.value }}</template>
        </span>
      </div>
    </div>

    <!-- Skills collapsible -->
    <div class="collapse-section">
      <div class="collapse-header" @click="skillsOpen = !skillsOpen">
        <span class="collapse-arrow">{{ skillsOpen ? '▼' : '▶' }}</span>
        <span class="collapse-title">专长 ({{ parsedSkills.length }})</span>
      </div>
      <div v-if="skillsOpen" class="collapse-body">
        <div v-for="(skill, i) in parsedSkills" :key="i" class="skill-row">
          <span class="skill-name">{{ skill.name }}</span>
          <span class="skill-value" :class="{ editable: isGM }" @click="isGM && startEditSkill(i)">
            <template v-if="editing === 'skill_' + i">
              <input ref="editInput" v-model.number="editValue" class="inline-edit inline-edit-sm" type="number" :min="0" :max="80" @keydown.enter="saveEditSkill(i)" @keydown.escape="cancelEdit" @blur="saveEditSkill(i)" />
            </template>
            <template v-else>{{ skill.value }}</template>
          </span>
          <span class="skill-attr-tag">[{{ attrLabel(skill.attribute) }}]</span>
          <span v-if="skill.is_career" class="skill-career" title="职业专长">⭐</span>
          <AppButton v-if="isGM" size="small" variant="ghost" @click="removeSkill(i)">✕</AppButton>
        </div>
        <div v-if="isGM" class="add-row">
          <input v-model="newSkillName" class="add-input" placeholder="专长名称" />
          <input v-model.number="newSkillValue" class="add-input add-input-sm" type="number" placeholder="数值" :min="0" :max="80" />
          <select v-model="newSkillAttr" class="add-select">
            <option value="strength">力量</option>
            <option value="constitution">体质</option>
            <option value="dexterity">敏捷</option>
            <option value="intelligence">智力</option>
            <option value="willpower">意志</option>
            <option value="charisma">魅力</option>
          </select>
          <label class="add-checkbox-sm"><input type="checkbox" v-model="newSkillCareer" /> 职业</label>
          <AppButton size="small" :disabled="!newSkillName.trim()" @click="addSkill">+</AppButton>
        </div>
        <div v-if="parsedSkills.length === 0 && !isGM" class="empty-hint">暂无专长</div>
      </div>
    </div>

    <!-- Items collapsible -->
    <div class="collapse-section">
      <div class="collapse-header" @click="itemsOpen = !itemsOpen">
        <span class="collapse-arrow">{{ itemsOpen ? '▼' : '▶' }}</span>
        <span class="collapse-title">随身物品 ({{ parsedItems.length }})</span>
      </div>
      <div v-if="itemsOpen" class="collapse-body">
        <div v-for="(item, i) in parsedItems" :key="i" class="item-row">
          <span class="item-icon">{{ itemIcon(item.type) }}</span>
          <span class="item-name">{{ item.name }}</span>
          <span v-if="item.detail" class="item-detail">{{ item.detail }}</span>
          <AppButton v-if="isGM" size="small" variant="ghost" @click="removeItem(i)">✕</AppButton>
        </div>
        <div v-if="isGM" class="add-row">
          <input v-model="newItemName" class="add-input" placeholder="物品名称" />
          <select v-model="newItemType" class="add-select">
            <option value="weapon">武器</option>
            <option value="tool">工具</option>
            <option value="other">其他</option>
          </select>
          <input v-model="newItemDetail" class="add-input add-input-sm" placeholder="详情" />
          <AppButton size="small" :disabled="!newItemName.trim()" @click="addItem">+</AppButton>
        </div>
        <div v-if="parsedItems.length === 0 && !isGM" class="empty-hint">暂无物品</div>
      </div>
    </div>

    <!-- Spells collapsible -->
    <div class="collapse-section">
      <div class="collapse-header" @click="spellsOpen = !spellsOpen">
        <span class="collapse-arrow">{{ spellsOpen ? '▼' : '▶' }}</span>
        <span class="collapse-title">法术 ({{ parsedSpells.length }})</span>
      </div>
      <div v-if="spellsOpen" class="collapse-body">
        <div v-for="(spell, i) in parsedSpells" :key="i" class="spell-row">
          <span class="spell-icon">{{ spellIcon(spell.level) }}</span>
          <span class="spell-name">{{ spell.name }}</span>
          <span class="spell-level">{{ spell.level }}</span>
          <span class="spell-cost">{{ spell.mp_cost }}MP</span>
          <AppButton v-if="isGM" size="small" variant="ghost" @click="removeSpell(i)">✕</AppButton>
        </div>
        <div v-if="isGM" class="add-row">
          <input v-model="newSpellName" class="add-input" placeholder="法术名称" />
          <select v-model="newSpellLevel" class="add-select">
            <option value="日常级">日常级</option>
            <option value="简单级">简单级</option>
            <option value="中等级">中等级</option>
            <option value="困难级">困难级</option>
            <option value="传说级">传说级</option>
          </select>
          <input v-model.number="newSpellCost" class="add-input add-input-sm" type="number" placeholder="MP" :min="0" />
          <AppButton size="small" :disabled="!newSpellName.trim()" @click="addSpell">+</AppButton>
        </div>
        <div v-if="parsedSpells.length === 0 && !isGM" class="empty-hint">暂无法术</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import AppButton from '@/components/common/AppButton.vue'

const props = defineProps({
  char: { type: Object, required: true },
  isGM: { type: Boolean, default: false },
  showPlaceOnMap: { type: Boolean, default: false }
})

const emit = defineEmits(['update', 'edit', 'delete', 'place-on-map'])

// Parse JSON fields
const parsedAttrs = computed(() => {
  try { return JSON.parse(props.char.attributes || '{}') } catch { return {} }
})
const parsedSkills = computed(() => {
  try { return JSON.parse(props.char.skills || '[]') } catch { return [] }
})
const parsedItems = computed(() => {
  try { return JSON.parse(props.char.items || '[]') } catch { return [] }
})
const parsedSpells = computed(() => {
  try { return JSON.parse(props.char.spells || '[]') } catch { return [] }
})

const willpower = computed(() => parsedAttrs.value.willpower || 50)

const ATTR_MAP = {
  strength: '力量', constitution: '体质', dexterity: '敏捷',
  intelligence: '智力', willpower: '意志', charisma: '魅力'
}

const attributeList = computed(() =>
  Object.entries(ATTR_MAP).map(([key, label]) => ({
    key, label, value: parsedAttrs.value[key] || 0
  }))
)

function attrLabel(key) { return ATTR_MAP[key] || key }

// Collapse state
const skillsOpen = ref(false)
const itemsOpen = ref(false)
const spellsOpen = ref(false)

// Inline edit state
const editing = ref(null)
const editValue = ref(0)
const editInput = ref(null)

function startEdit(field) {
  if (!props.isGM) return
  editing.value = field
  editValue.value = props.char[field]
  nextTick(() => editInput.value?.focus())
}

function startEditAttr(key) {
  if (!props.isGM) return
  editing.value = 'attr_' + key
  editValue.value = parsedAttrs.value[key] || 0
  nextTick(() => editInput.value?.focus())
}

function startEditSkill(index) {
  if (!props.isGM) return
  editing.value = 'skill_' + index
  editValue.value = parsedSkills.value[index]?.value || 0
  nextTick(() => editInput.value?.focus())
}

function cancelEdit() {
  editing.value = null
}

function saveEdit() {
  if (!editing.value || editValue.value === null) { cancelEdit(); return }
  const field = editing.value
  emit('update', props.char.id, { [field]: editValue.value })
  cancelEdit()
}

function saveEditAttr(key) {
  if (editValue.value === null) { cancelEdit(); return }
  const newAttrs = { ...parsedAttrs.value, [key]: editValue.value }
  emit('update', props.char.id, { attributes: JSON.stringify(newAttrs) })
  cancelEdit()
}

function saveEditSkill(index) {
  if (editValue.value === null) { cancelEdit(); return }
  const newSkills = [...parsedSkills.value]
  newSkills[index] = { ...newSkills[index], value: editValue.value }
  emit('update', props.char.id, { skills: JSON.stringify(newSkills) })
  cancelEdit()
}

// Item management
const newItemName = ref('')
const newItemType = ref('weapon')
const newItemDetail = ref('')

function addItem() {
  if (!newItemName.value.trim()) return
  const newItems = [...parsedItems.value, { name: newItemName.value.trim(), type: newItemType.value, detail: newItemDetail.value.trim() }]
  emit('update', props.char.id, { items: JSON.stringify(newItems) })
  newItemName.value = ''
  newItemDetail.value = ''
}

function removeItem(index) {
  const newItems = parsedItems.value.filter((_, i) => i !== index)
  emit('update', props.char.id, { items: JSON.stringify(newItems) })
}

// Skill management
const newSkillName = ref('')
const newSkillValue = ref(10)
const newSkillAttr = ref('strength')
const newSkillCareer = ref(false)

function addSkill() {
  if (!newSkillName.value.trim()) return
  const newSkills = [...parsedSkills.value, {
    name: newSkillName.value.trim(),
    value: newSkillValue.value || 10,
    attribute: newSkillAttr.value,
    is_career: newSkillCareer.value
  }]
  emit('update', props.char.id, { skills: JSON.stringify(newSkills) })
  newSkillName.value = ''
  newSkillValue.value = 10
  newSkillCareer.value = false
}

function removeSkill(index) {
  const newSkills = parsedSkills.value.filter((_, i) => i !== index)
  emit('update', props.char.id, { skills: JSON.stringify(newSkills) })
}

// Spell management
const newSpellName = ref('')
const newSpellLevel = ref('简单级')
const newSpellCost = ref(0)

function addSpell() {
  if (!newSpellName.value.trim()) return
  const newSpells = [...parsedSpells.value, { name: newSpellName.value.trim(), level: newSpellLevel.value, mp_cost: newSpellCost.value || 0 }]
  emit('update', props.char.id, { spells: JSON.stringify(newSpells) })
  newSpellName.value = ''
  newSpellCost.value = 0
}

function removeSpell(index) {
  const newSpells = parsedSpells.value.filter((_, i) => i !== index)
  emit('update', props.char.id, { spells: JSON.stringify(newSpells) })
}

// Helpers
function barPercent(current, max) {
  if (!max) return '0%'
  return Math.max(0, Math.min(100, (current / max) * 100)) + '%'
}

function itemIcon(type) {
  const icons = { weapon: '🗡', tool: '🔧', other: '📦' }
  return icons[type] || '📦'
}

function spellIcon(level) {
  const icons = { '日常级': '✨', '简单级': '🔥', '中等级': '⚡', '困难级': '🔮', '传说级': '🌟' }
  return icons[level] || '✨'
}
</script>

<style scoped>
.character-sheet {
  padding: 10px 12px;
  background: var(--bg-card);
  border-radius: var(--radius-md);
  border: 2px solid transparent;
  transition: border-color 0.2s;
}
.character-sheet.is-npc { border-left: 3px solid var(--color-danger); }

.sheet-header {
  display: flex; align-items: center; gap: 6px; margin-bottom: 8px;
}
.sheet-icon { font-size: 14px; flex-shrink: 0; width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; border-radius: 50%; overflow: hidden; }
.sheet-avatar-img { width: 100%; height: 100%; object-fit: cover; }
.sheet-title { flex: 1; display: flex; flex-direction: column; gap: 1px; }
.sheet-name { font-weight: 600; font-size: 14px; color: var(--text-primary); }
.sheet-profession { font-size: 11px; color: var(--text-muted); }
.sheet-tag { padding: 1px 6px; border-radius: 8px; font-size: 10px; font-weight: 600; }
.sheet-tag.npc { background: var(--color-danger-dim); color: var(--color-danger); }
.sheet-actions { display: flex; gap: 2px; }

/* ====== Stat bars ====== */
.bar-group { display: flex; flex-direction: column; gap: 4px; margin-bottom: 8px; }

.stat-bar-row {
  display: flex; align-items: center; gap: 6px;
  cursor: default;
}
.stat-bar-row .editable { cursor: pointer; }

.bar-label { font-size: 11px; font-weight: 700; min-width: 26px; color: var(--text-muted); }
.bar-track { flex: 1; height: 6px; background: rgba(255,255,255,0.06); border-radius: 3px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 3px; transition: width 0.3s ease; }
.hp-fill { background: var(--color-danger); }
.san-fill { background: var(--color-info); }
.mp-fill { background: #a855f7; }

.bar-value { font-size: 11px; color: var(--text-secondary); white-space: nowrap; min-width: 48px; text-align: right; }
.bar-value.editable:hover { color: var(--accent-gold); }

/* ====== Attributes ====== */
.attr-grid {
  display: grid; grid-template-columns: 1fr 1fr; gap: 2px 12px;
  padding: 6px 0; border-top: 1px solid var(--border-subtle); margin-bottom: 4px;
}
.attr-item { display: flex; justify-content: space-between; align-items: center; padding: 1px 0; }
.attr-label { font-size: 11px; color: var(--text-muted); }
.attr-value { font-size: 12px; font-weight: 600; color: var(--text-secondary); }
.attr-value.editable:hover { color: var(--accent-gold); cursor: pointer; }

/* ====== Collapse sections ====== */
.collapse-section { border-top: 1px solid var(--border-subtle); }

.collapse-header {
  display: flex; align-items: center; gap: 4px; padding: 5px 0;
  cursor: pointer; user-select: none;
}
.collapse-header:hover { color: var(--accent-gold); }
.collapse-arrow { font-size: 9px; color: var(--text-muted); }
.collapse-title { font-size: 11px; font-weight: 600; color: var(--text-muted); }

.collapse-body { padding: 0 0 6px 14px; }

/* ====== Skills ====== */
.skill-row { display: flex; align-items: center; gap: 4px; padding: 2px 0; }
.skill-name { font-size: 12px; color: var(--text-primary); min-width: 48px; }
.skill-value { font-size: 12px; font-weight: 600; color: var(--text-secondary); min-width: 20px; }
.skill-value.editable:hover { color: var(--accent-gold); cursor: pointer; }
.skill-attr-tag { font-size: 10px; color: var(--text-muted); background: var(--bg-secondary); padding: 0 4px; border-radius: 3px; }
.skill-career { font-size: 10px; }

/* ====== Items ====== */
.item-row { display: flex; align-items: center; gap: 4px; padding: 2px 0; }
.item-icon { font-size: 12px; }
.item-name { font-size: 12px; color: var(--text-primary); }
.item-detail { font-size: 11px; color: var(--text-muted); flex: 1; }

/* ====== Spells ====== */
.spell-row { display: flex; align-items: center; gap: 4px; padding: 2px 0; }
.spell-icon { font-size: 12px; }
.spell-name { font-size: 12px; color: var(--text-primary); }
.spell-level { font-size: 10px; color: var(--text-muted); }
.spell-cost { font-size: 10px; color: #a855f7; }

/* ====== Add rows ====== */
.add-row { display: flex; align-items: center; gap: 4px; margin-top: 4px; flex-wrap: wrap; }
.add-input {
  padding: 3px 6px; font-size: 11px; font-family: var(--font-body);
  border: 1px solid var(--border-default); border-radius: var(--radius-sm);
  background: var(--bg-input); color: var(--text-primary); outline: none;
}
.add-input:focus { border-color: var(--border-focus); }
.add-input-sm { width: 48px; }
.add-select {
  padding: 3px 4px; font-size: 11px; font-family: var(--font-body);
  border: 1px solid var(--border-default); border-radius: var(--radius-sm);
  background: var(--bg-input); color: var(--text-primary); outline: none;
}

/* ====== Inline edit ====== */
.inline-edit {
  width: 44px; padding: 1px 4px; font-size: 11px; text-align: center;
  border: 1px solid var(--accent-gold); border-radius: 3px;
  background: var(--bg-input); color: var(--text-primary); outline: none;
}
.inline-edit-sm { width: 36px; }

.empty-hint { font-size: 11px; color: var(--text-muted); padding: 4px 0; }

.add-checkbox-sm {
  display: flex; align-items: center; gap: 3px;
  font-size: 11px; color: var(--text-muted); cursor: pointer; white-space: nowrap;
}
.add-checkbox-sm input { accent-color: var(--accent-gold); }
</style>
