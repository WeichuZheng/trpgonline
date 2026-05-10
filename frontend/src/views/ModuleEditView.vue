<template>
  <div class="module-edit">
    <div class="module-edit-header">
      <AppButton variant="ghost" @click="goBack">← 返回</AppButton>
      <h2>{{ module?.title || '加载中...' }}</h2>
    </div>

    <div class="module-edit-content" v-if="module">
      <!-- Tab 切换 -->
      <div class="tab-bar">
        <button class="tab-btn" :class="{ active: activeTab === 'resources' }" @click="activeTab = 'resources'">资源管理</button>
        <button class="tab-btn" :class="{ active: activeTab === 'maps' }" @click="activeTab = 'maps'">地图管理</button>
        <button class="tab-btn" :class="{ active: activeTab === 'characters' }" @click="activeTab = 'characters'">角色模板</button>
      </div>

      <!-- ====== 资源管理 Tab ====== -->
      <template v-if="activeTab === 'resources'">
        <AppCard title="资源管理">
          <template #header>
            <div class="section-header">
              <h3>资源管理</h3>
              <AppButton size="small" @click="showResourceForm = true">+ 添加资源</AppButton>
            </div>
          </template>

          <div class="resource-list">
            <div
              v-for="resource in resources"
              :key="resource.id"
              class="resource-item"
              :class="{ visible: resource.default_visible }"
            >
              <span class="resource-title">{{ resource.title }}</span>
              <span class="resource-type">{{ resource.type === 'image' ? '图片' : '文本' }}</span>
              <span class="resource-visibility" :class="resource.default_visible ? 'shown' : 'hidden'">
                {{ resource.default_visible ? '已显示' : '已隐藏' }}
              </span>
              <AppButton size="small" variant="secondary" @click="toggleVisibility(resource)">
                {{ resource.default_visible ? '隐藏' : '显示' }}
              </AppButton>
              <AppButton size="small" variant="danger" @click="confirmDeleteResource(resource)">删除</AppButton>
            </div>
            <div v-if="resources.length === 0" class="empty-state">
              暂无资源，点击上方按钮添加
            </div>
          </div>
        </AppCard>

        <!-- Add Resource Form -->
        <AppCard v-if="showResourceForm" title="添加资源">
          <form @submit.prevent="handleCreateResource">
            <AppSelect v-model="newResource.type" :options="typeOptions" label="类型" required></AppSelect>
            <AppInput v-model="newResource.title" label="标题" placeholder="请输入标题" required></AppInput>

            <div v-if="newResource.type === 'text'" class="form-group">
              <AppSelect v-model="newResource.display_type" :options="displayTypes" label="显示类型" required></AppSelect>
              <label>内容</label>
              <textarea v-model="newResource.content" placeholder="请输入文本内容" rows="6"></textarea>
            </div>

            <div v-if="newResource.type === 'image'" class="form-group">
              <label>选择图片</label>
              <input type="file" accept="image/*" @change="handleFileSelect">
            </div>

            <div class="form-actions">
              <AppButton variant="secondary" @click="showResourceForm = false">取消</AppButton>
              <AppButton type="submit" :loading="loading">保存</AppButton>
            </div>
          </form>
        </AppCard>
      </template>

      <!-- ====== 地图管理 Tab ====== -->
      <template v-if="activeTab === 'maps'">
        <AppCard title="地图管理">
          <template #header>
            <div class="section-header">
              <h3>地图管理</h3>
              <AppButton size="small" @click="showMapForm = true">+ 添加地图</AppButton>
            </div>
          </template>

          <div class="map-list">
            <div v-for="map in maps" :key="map.id" class="map-item">
              <div class="map-preview">
                <img v-if="map.image_url" :src="map.image_url" :alt="map.name" />
                <div v-else class="map-no-img">无图</div>
              </div>
              <div class="map-info">
                <span class="map-name">{{ map.name }}</span>
                <span v-if="map.grid_size" class="map-grid">网格: {{ map.grid_size }}px</span>
              </div>
              <AppButton size="small" variant="secondary" @click="editMapGrid(map)">网格</AppButton>
              <AppButton size="small" variant="danger" @click="confirmDeleteMap(map)">删除</AppButton>
            </div>
            <div v-if="maps.length === 0" class="empty-state">
              暂无地图，点击上方按钮添加
            </div>
          </div>
        </AppCard>

        <!-- Add Map Form -->
        <AppCard v-if="showMapForm" title="添加地图">
          <form @submit.prevent="handleCreateMap">
            <AppInput v-model="newMap.name" label="地图名称" placeholder="请输入地图名称" required></AppInput>
            <div class="form-group">
              <label>地图图片</label>
              <input type="file" accept="image/*" @change="handleMapFileSelect" required>
            </div>
            <details style="margin-top:8px; border:1px solid var(--border-subtle); border-radius:var(--radius-md); padding:6px 10px;">
              <summary style="font-size:13px; color:var(--text-muted); cursor:pointer;">高级：设置网格大小</summary>
              <p style="font-size:11px; color:var(--text-muted); margin:6px 0 4px;">如果地图本身没有网格线，可设置网格大小以显示网格覆盖层。一般可跳过此项。</p>
              <AppInput v-model.number="newMap.grid_size" type="number" label="网格大小(px)" placeholder="如 50" :min="1"></AppInput>
            </details>
            <div class="form-actions">
              <AppButton variant="secondary" @click="showMapForm = false">取消</AppButton>
              <AppButton type="submit" :loading="loading">保存</AppButton>
            </div>
          </form>
        </AppCard>
      </template>

      <!-- ====== 角色模板 Tab ====== -->
      <template v-if="activeTab === 'characters'">
        <AppCard title="角色模板">
          <template #header>
            <div class="section-header">
              <h3>角色模板</h3>
              <AppButton size="small" @click="openTemplateForm()">+ 添加模板</AppButton>
            </div>
          </template>

          <p class="tab-hint">角色模板可被 GM 在游戏房间中快速加载，无需手动输入角色属性。</p>

          <div class="template-list">
            <div v-for="tpl in characterTemplates" :key="tpl.id" class="template-item" :class="{ enemy: tpl.is_enemy }">
              <div class="template-icon">{{ tpl.is_enemy ? '👹' : '🧑' }}</div>
              <div class="template-info">
                <span class="template-name">{{ tpl.name }}</span>
                <span class="template-stats">HP {{ tpl.hp }}/{{ tpl.max_hp }} | SAN {{ tpl.san ?? 50 }}{{ tpl.profession ? ' | ' + tpl.profession : '' }}</span>
              </div>
              <span class="template-tag" :class="tpl.is_enemy ? 'enemy' : 'ally'">{{ tpl.is_enemy ? '敌方' : '友方' }}</span>
              <AppButton size="small" variant="secondary" @click="openTemplateForm(tpl)">编辑</AppButton>
              <AppButton size="small" variant="danger" @click="confirmDeleteTemplate(tpl)">删除</AppButton>
            </div>
            <div v-if="characterTemplates.length === 0" class="empty-state">
              暂无角色模板，点击上方按钮添加
            </div>
          </div>
        </AppCard>

        <!-- Add/Edit Template Form -->
        <AppCard v-if="showTemplateForm" :title="editingTemplate ? '编辑角色模板' : '添加角色模板'">
          <form @submit.prevent="handleSaveTemplate">
            <AppInput v-model="templateForm.name" label="名称" placeholder="角色名称" required></AppInput>
            <div class="form-row-label">头像</div>
            <AvatarUploader v-model="templateForm.avatar" />
            <AppInput v-model="templateForm.profession" label="职业" placeholder="职业 (可选)"></AppInput>
            <div class="stats-input">
              <AppInput v-model.number="templateForm.hp" type="number" label="当前HP" :min="0"></AppInput>
              <span class="stats-divider">/</span>
              <AppInput v-model.number="templateForm.max_hp" type="number" label="最大HP" :min="1"></AppInput>
            </div>
            <div class="stats-input">
              <AppInput v-model.number="templateForm.san" type="number" label="SAN" :min="0"></AppInput>
            </div>
            <div class="stats-input">
              <AppInput v-model.number="templateForm.mp" type="number" label="当前MP" :min="0"></AppInput>
              <span class="stats-divider">/</span>
              <AppInput v-model.number="templateForm.max_mp" type="number" label="最大MP" :min="0"></AppInput>
            </div>
            <details class="template-attrs-details" style="margin-top:12px">
              <summary class="template-attrs-summary">六维属性</summary>
              <div class="template-attrs-grid">
                <div class="template-attrs-row" v-for="(label, key) in ATTR_MAP" :key="key">
                  <label class="template-attrs-label">{{ label }}</label>
                  <input v-model.number="templateFormAttrs[key]" class="template-attrs-input" type="number" :min="1" :max="99" />
                </div>
              </div>
            </details>
            <AppInput v-model="templateForm.notes" label="备注" placeholder="可选" style="margin-top:12px"></AppInput>
            <div class="form-group">
              <label class="checkbox-label">
                <input type="checkbox" v-model="templateForm.is_enemy" />
                敌方角色
              </label>
            </div>
            <div class="form-actions">
              <AppButton variant="secondary" @click="showTemplateForm = false">取消</AppButton>
              <AppButton type="submit" :loading="loading">保存</AppButton>
            </div>
          </form>
        </AppCard>
      </template>
    </div>

    <!-- Delete Resource Confirm -->
    <AppModal v-model="showDeleteDialog" title="确认删除" size="small">
      <p>确定要删除资源"{{ deletingResource?.title }}"吗？</p>
      <template #footer>
        <AppButton variant="secondary" @click="showDeleteDialog = false">取消</AppButton>
        <AppButton variant="danger" @click="handleDeleteResource" :loading="loading">删除</AppButton>
      </template>
    </AppModal>

    <!-- Delete Map Confirm -->
    <AppModal v-model="showDeleteMapDialog" title="确认删除" size="small">
      <p>确定要删除地图"{{ deletingMap?.name }}"吗？地图上的所有单位也会被删除。</p>
      <template #footer>
        <AppButton variant="secondary" @click="showDeleteMapDialog = false">取消</AppButton>
        <AppButton variant="danger" @click="handleDeleteMap" :loading="loading">删除</AppButton>
      </template>
    </AppModal>

    <!-- Delete Template Confirm -->
    <AppModal v-model="showDeleteTemplateDialog" title="确认删除" size="small">
      <p>确定要删除角色模板"{{ deletingTemplate?.name }}"吗？</p>
      <template #footer>
        <AppButton variant="secondary" @click="showDeleteTemplateDialog = false">取消</AppButton>
        <AppButton variant="danger" @click="handleDeleteTemplate" :loading="loading">删除</AppButton>
      </template>
    </AppModal>

    <!-- Edit Grid Size Modal -->
    <AppModal v-model="showGridEditDialog" title="设置网格大小" size="small">
      <AppInput v-model.number="editingGridSize" type="number" label="网格大小(px)" placeholder="如 50" :min="1"></AppInput>
      <p style="font-size:12px;color:#9ca3af;margin-top:8px;">网格大小即每个格子占多少像素。可上传地图后在图片上对照设置。</p>
      <template #footer>
        <AppButton variant="secondary" @click="showGridEditDialog = false">取消</AppButton>
        <AppButton @click="handleSaveGrid" :loading="loading">保存</AppButton>
      </template>
    </AppModal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, inject } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useModulesStore } from '@/stores/modules'
import { resourceService } from '@/services/resourceService'
import mapService from '@/services/mapService'
import { characterTemplateService } from '@/services/characterTemplateService'
import AppButton from '@/components/common/AppButton.vue'
import AppCard from '@/components/common/AppCard.vue'
import AppInput from '@/components/common/AppInput.vue'
import AppModal from '@/components/common/AppModal.vue'
import AppSelect from '@/components/common/AppSelect.vue'
import AvatarUploader from '@/components/common/AvatarUploader.vue'

const route = useRoute()
const router = useRouter()
const modulesStore = useModulesStore()
const toast = inject('toast')

const module = ref(null)
const resources = ref([])
const maps = ref([])
const characterTemplates = ref([])
const loading = ref(false)
const activeTab = ref('resources')
const showResourceForm = ref(false)
const showDeleteDialog = ref(false)
const deletingResource = ref(null)
const showMapForm = ref(false)
const showDeleteMapDialog = ref(false)
const deletingMap = ref(null)
const showGridEditDialog = ref(false)
const editingMapId = ref(null)
const editingGridSize = ref(null)
const showTemplateForm = ref(false)
const editingTemplate = ref(null)
const showDeleteTemplateDialog = ref(false)
const deletingTemplate = ref(null)

const newResource = reactive({
  type: 'text',
  title: '',
  content: '',
  display_type: 'story',
  file: null
})

const newMap = reactive({
  name: '',
  grid_size: null,
  file: null
})

const templateForm = reactive({
  name: '',
  avatar: '',
  profession: '',
  hp: 10,
  max_hp: 10,
  san: 50,
  mp: 0,
  max_mp: 0,
  notes: '',
  is_enemy: false
})

const templateFormAttrs = reactive({
  strength: 50, constitution: 50, dexterity: 50,
  intelligence: 50, willpower: 50, charisma: 50
})

const ATTR_MAP = {
  strength: '力量', constitution: '体质', dexterity: '敏捷',
  intelligence: '智力', willpower: '意志', charisma: '魅力'
}

const typeOptions = [
  { value: 'text', label: '文本' },
  { value: 'image', label: '图片' }
]

const displayTypes = [
  { value: 'story', label: '背景故事' },
  { value: 'rule', label: '规则说明' },
  { value: 'clue', label: '线索卡' },
  { value: 'character', label: '角色描述' },
  { value: 'mission', label: '任务目标' }
]

onMounted(async () => {
  const moduleId = route.params.id
  try {
    module.value = await modulesStore.fetchModule(moduleId)
    await fetchResources()
    await fetchMaps()
    await fetchCharacterTemplates()
  } catch (error) {
    toast.error('加载失败')
  }
})

async function fetchResources() {
  try {
    const data = await resourceService.getModuleResources(route.params.id)
    resources.value = Array.isArray(data) ? data : []
  } catch {
    toast.error('加载资源失败')
  }
}

async function fetchMaps() {
  try {
    const data = await mapService.getModuleMaps(route.params.id)
    maps.value = Array.isArray(data) ? data : []
  } catch {
    toast.error('加载地图失败')
  }
}

async function fetchCharacterTemplates() {
  try {
    const data = await characterTemplateService.getModuleTemplates(route.params.id)
    characterTemplates.value = Array.isArray(data) ? data : []
  } catch {
    toast.error('加载角色模板失败')
  }
}

function goBack() {
  router.push('/dashboard')
}

// ====== Resources ======

function handleFileSelect(event) {
  const file = event.target.files[0]
  if (file) newResource.file = file
}

async function handleCreateResource() {
  if (!newResource.title.trim()) { toast.error('请输入标题'); return }
  if (newResource.type === 'text' && !newResource.content?.trim()) { toast.error('请输入文本内容'); return }
  if (newResource.type === 'image' && !newResource.file) { toast.error('请选择图片'); return }

  loading.value = true
  try {
    await resourceService.createResource(route.params.id, {
      type: newResource.type,
      title: newResource.title,
      content: newResource.content,
      display_type: newResource.display_type,
      file: newResource.file
    })
    toast.success('资源创建成功')
    showResourceForm.value = false
    await fetchResources()
    newResource.title = ''
    newResource.content = ''
    newResource.file = null
  } catch (error) {
    toast.error(error.message || '创建失败')
  } finally {
    loading.value = false
  }
}

async function toggleVisibility(resource) {
  try {
    await resourceService.toggleDefaultVisible(resource.id, !resource.default_visible)
    await fetchResources()
    toast.success('更新成功')
  } catch (error) {
    toast.error(error.message || '操作失败')
  }
}

function confirmDeleteResource(resource) {
  deletingResource.value = resource
  showDeleteDialog.value = true
}

async function handleDeleteResource() {
  loading.value = true
  try {
    await resourceService.deleteResource(deletingResource.value.id)
    await fetchResources()
    toast.success('删除成功')
    showDeleteDialog.value = false
  } catch (error) {
    toast.error(error.message || '删除失败')
  } finally {
    loading.value = false
  }
}

// ====== Maps ======

function handleMapFileSelect(event) {
  const file = event.target.files[0]
  if (file) newMap.file = file
}

async function handleCreateMap() {
  if (!newMap.name.trim()) { toast.error('请输入地图名称'); return }
  if (!newMap.file) { toast.error('请选择地图图片'); return }

  loading.value = true
  try {
    const formData = new FormData()
    formData.append('name', newMap.name)
    formData.append('file', newMap.file)
    if (newMap.grid_size) formData.append('grid_size', String(newMap.grid_size))

    await mapService.createMap(route.params.id, formData)
    toast.success('地图创建成功')
    showMapForm.value = false
    await fetchMaps()
    newMap.name = ''
    newMap.grid_size = null
    newMap.file = null
  } catch (error) {
    toast.error(error.message || '创建失败')
  } finally {
    loading.value = false
  }
}

function editMapGrid(map) {
  editingMapId.value = map.id
  editingGridSize.value = map.grid_size
  showGridEditDialog.value = true
}

async function handleSaveGrid() {
  loading.value = true
  try {
    await mapService.updateMap(editingMapId.value, { grid_size: editingGridSize.value })
    await fetchMaps()
    toast.success('网格大小已更新')
    showGridEditDialog.value = false
  } catch (error) {
    toast.error(error.message || '更新失败')
  } finally {
    loading.value = false
  }
}

function confirmDeleteMap(map) {
  deletingMap.value = map
  showDeleteMapDialog.value = true
}

async function handleDeleteMap() {
  loading.value = true
  try {
    await mapService.deleteMap(deletingMap.value.id)
    await fetchMaps()
    toast.success('地图已删除')
    showDeleteMapDialog.value = false
  } catch (error) {
    toast.error(error.message || '删除失败')
  } finally {
    loading.value = false
  }
}

// ====== Character Templates ======

function openTemplateForm(tpl = null) {
  editingTemplate.value = tpl
  if (tpl) {
    Object.assign(templateForm, {
      name: tpl.name,
      avatar: tpl.avatar || '',
      profession: tpl.profession || '',
      hp: tpl.hp,
      max_hp: tpl.max_hp,
      san: tpl.san ?? 50,
      mp: tpl.mp ?? 0,
      max_mp: tpl.max_mp ?? 0,
      notes: tpl.notes || '',
      is_enemy: tpl.is_enemy
    })
    try {
      const attrs = JSON.parse(tpl.attributes || '{}')
      Object.assign(templateFormAttrs, {
        strength: attrs.strength ?? 50, constitution: attrs.constitution ?? 50,
        dexterity: attrs.dexterity ?? 50, intelligence: attrs.intelligence ?? 50,
        willpower: attrs.willpower ?? 50, charisma: attrs.charisma ?? 50
      })
    } catch {
      Object.assign(templateFormAttrs, { strength: 50, constitution: 50, dexterity: 50, intelligence: 50, willpower: 50, charisma: 50 })
    }
  } else {
    Object.assign(templateForm, { name: '', avatar: '', profession: '', hp: 10, max_hp: 10, san: 50, mp: 0, max_mp: 0, notes: '', is_enemy: false })
    Object.assign(templateFormAttrs, { strength: 50, constitution: 50, dexterity: 50, intelligence: 50, willpower: 50, charisma: 50 })
  }
  showTemplateForm.value = true
}

async function handleSaveTemplate() {
  if (!templateForm.name.trim()) { toast.error('请输入角色名称'); return }

  loading.value = true
  try {
    const data = {
      ...templateForm,
      attributes: JSON.stringify({ ...templateFormAttrs }),
      skills: '[]',
      items: '[]',
      spells: '[]'
    }
    if (editingTemplate.value) {
      await characterTemplateService.updateTemplate(editingTemplate.value.id, data)
    } else {
      await characterTemplateService.createTemplate(route.params.id, data)
    }
    await fetchCharacterTemplates()
    toast.success(editingTemplate.value ? '模板已更新' : '模板已创建')
    showTemplateForm.value = false
  } catch (error) {
    toast.error(error.message || '保存失败')
  } finally {
    loading.value = false
  }
}

function confirmDeleteTemplate(tpl) {
  deletingTemplate.value = tpl
  showDeleteTemplateDialog.value = true
}

async function handleDeleteTemplate() {
  loading.value = true
  try {
    await characterTemplateService.deleteTemplate(deletingTemplate.value.id)
    await fetchCharacterTemplates()
    toast.success('模板已删除')
    showDeleteTemplateDialog.value = false
  } catch (error) {
    toast.error(error.message || '删除失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.module-edit { padding: 32px; max-width: 1200px; margin: 0 auto; }

.module-edit-header { display: flex; align-items: center; gap: 16px; margin-bottom: 24px; }
.module-edit-header h2 { font-family: var(--font-display); font-size: 22px; color: var(--accent-gold); letter-spacing: 0.04em; }

.module-edit-content { display: flex; flex-direction: column; gap: 20px; }

.tab-bar { display: flex; gap: 0; border-bottom: 2px solid var(--border-subtle); margin-bottom: 4px; }

.tab-btn {
  padding: 10px 24px;
  border: none;
  background: none;
  font-size: 15px;
  font-weight: 500;
  font-family: var(--font-body);
  color: var(--text-muted);
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -2px;
  transition: all 0.2s;
}

.tab-btn:hover { color: var(--accent-gold); }
.tab-btn.active { color: var(--accent-gold); border-bottom-color: var(--accent-gold); }

.section-header { display: flex; justify-content: space-between; align-items: center; }

.tab-hint { font-size: 13px; color: var(--text-muted); margin: 0 0 12px; }

.resource-list { display: flex; flex-direction: column; gap: 10px; }

.resource-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
}

.resource-title { flex: 1; font-weight: 500; color: var(--text-primary); }
.resource-type { color: var(--text-muted); font-size: 14px; }

.resource-visibility { padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: 500; }
.resource-visibility.shown { background: var(--color-success-dim); color: var(--color-success); }
.resource-visibility.hidden { background: var(--color-danger-dim); color: var(--color-danger); }

.map-list { display: flex; flex-direction: column; gap: 10px; }

.map-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
}

.map-preview {
  width: 64px;
  height: 48px;
  border-radius: var(--radius-sm);
  overflow: hidden;
  background: var(--bg-input);
  flex-shrink: 0;
}

.map-preview img { width: 100%; height: 100%; object-fit: cover; }

.map-no-img {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  font-size: 11px;
  color: var(--text-muted);
}

.map-info { flex: 1; display: flex; flex-direction: column; gap: 2px; }
.map-name { font-weight: 500; font-size: 14px; color: var(--text-primary); }
.map-grid { font-size: 12px; color: var(--text-muted); }

/* ====== 角色模板 ====== */
.template-list { display: flex; flex-direction: column; gap: 8px; }

.template-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  border-left: 3px solid var(--color-info);
}

.template-item.enemy { border-left-color: var(--color-danger); }

.template-icon { font-size: 20px; flex-shrink: 0; }

.template-info { flex: 1; display: flex; flex-direction: column; gap: 2px; }
.template-name { font-weight: 600; font-size: 14px; color: var(--text-primary); }
.template-stats { font-size: 12px; color: var(--text-muted); }

.template-tag {
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 600;
}
.template-tag.ally { background: var(--color-info-dim); color: var(--color-info); }
.template-tag.enemy { background: var(--color-danger-dim); color: var(--color-danger); }

.stats-input { display: flex; align-items: flex-end; gap: 8px; }
.stats-divider { font-size: 18px; color: var(--text-muted); padding-bottom: 8px; }

.template-attrs-details { border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 8px 12px; }
.template-attrs-summary { font-size: 13px; color: var(--text-muted); cursor: pointer; }
.template-attrs-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px 16px; margin-top: 8px; }
.template-attrs-row { display: flex; align-items: center; gap: 6px; }
.template-attrs-label { font-size: 13px; color: var(--text-muted); min-width: 32px; text-align: right; }
.template-attrs-input { width: 60px; padding: 4px 8px; border: 1px solid var(--border-default); border-radius: var(--radius-sm); background: var(--bg-input); color: var(--text-primary); font-size: 13px; text-align: center; outline: none; }
.template-attrs-input:focus { border-color: var(--border-focus); }

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: var(--text-secondary);
  cursor: pointer;
}
.checkbox-label input { accent-color: var(--accent-gold); }

.form-group { display: flex; flex-direction: column; gap: 8px; margin-top: 16px; }

.form-group textarea {
  padding: 10px 14px;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  font-size: 14px;
  font-family: var(--font-body);
  background: var(--bg-input);
  color: var(--text-primary);
  resize: vertical;
}

.form-group textarea:focus { outline: none; border-color: var(--border-focus); }

.form-actions { display: flex; justify-content: flex-end; gap: 12px; margin-top: 20px; }

.empty-state { text-align: center; padding: 40px; color: var(--text-muted); }

.form-row-label { font-size: 13px; color: var(--text-muted); margin-bottom: 4px; }

p { color: var(--text-secondary); }
</style>
