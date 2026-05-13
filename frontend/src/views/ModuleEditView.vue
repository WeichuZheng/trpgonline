<template>
  <div class="module-edit">
    <div class="module-edit-header">
      <AppButton variant="ghost" @click="goBack">← 返回</AppButton>
      <h2>{{ module?.title || '加载中...' }}</h2>
      <div class="header-theme-select">
        <label class="theme-label">推荐主题：</label>
        <select :value="module?.theme || 'dark'" @change="saveTheme($event.target.value)">
          <option value="dark">🌙 墨火羊皮卷</option>
          <option value="light">☀️ 象牙墨色</option>
          <option value="sepia">📜 古卷羊皮</option>
          <option value="forest">🌲 深林暗影</option>
          <option value="ocean">🌊 深海湛蓝</option>
        </select>
      </div>
    </div>

    <div class="module-edit-content" v-if="module">
      <!-- Tab 切换 -->
      <div class="tab-bar">
        <button class="tab-btn" :class="{ active: activeTab === 'resources' }" @click="activeTab = 'resources'">资源管理</button>
        <button class="tab-btn" :class="{ active: activeTab === 'maps' }" @click="activeTab = 'maps'">地图管理</button>
        <button class="tab-btn" :class="{ active: activeTab === 'characters' }" @click="activeTab = 'characters'">角色模板</button>
        <button class="tab-btn" :class="{ active: activeTab === 'tasks' }" @click="activeTab = 'tasks'">📋 任务板</button>
        <button class="tab-btn" :class="{ active: activeTab === 'chapters' }" @click="activeTab = 'chapters'">📖 章节管理</button>
      </div>

      <!-- ====== 资源管理 Tab ====== -->
      <template v-if="activeTab === 'resources'">
        <!-- Document list view -->
        <template v-if="!editingResourceId">
          <AppCard title="文档管理">
            <template #header>
              <div class="section-header">
                <h3>文档管理</h3>
                <AppButton size="small" @click="openNewDocForm">+ 新建文档</AppButton>
              </div>
            </template>

            <p class="tab-hint">文档支持富文本编辑，GM可在房间中控制段落级可见性。</p>

            <div class="resource-list">
              <div v-for="resource in resources" :key="resource.id" class="resource-item" @click="openDocEditor(resource)">
                <span class="resource-doc-icon">📄</span>
                <div class="resource-info">
                  <span class="resource-title">{{ resource.title }}</span>
                </div>
                <AppButton size="small" variant="secondary" @click.stop="openDocEditor(resource)">编辑</AppButton>
                <AppButton size="small" variant="danger" @click.stop="confirmDeleteResource(resource)">删除</AppButton>
              </div>
              <div v-if="resources.length === 0" class="empty-state">
                暂无文档，点击上方按钮创建
              </div>
            </div>
          </AppCard>
        </template>

        <!-- Document editor view -->
        <template v-else>
          <div class="doc-editor-view">
            <div class="doc-editor-header">
              <AppButton variant="ghost" @click="closeDocEditor">← 返回文档列表</AppButton>
              <AppInput v-model="editingResourceTitle" placeholder="文档标题" class="doc-title-input" />
              <AppButton :variant="editingResourceTitle.trim() ? 'primary' : 'secondary'" @click="saveDocContent" :loading="loading">保存</AppButton>
            </div>
            <ResourceEditor v-model="editingResourceContent" :is-gm="true" :placeholder="'开始编写 ' + editingResourceTitle + '...'" />
          </div>
        </template>

        <!-- New Doc Form Modal -->
        <AppModal v-model="showNewDocForm" title="新建文档" size="small">
          <form @submit.prevent="handleCreateDoc">
            <AppInput v-model="newDocTitle" label="文档标题" placeholder="如：第一章 神秘的庄园" required></AppInput>
            <div class="form-actions">
              <AppButton variant="secondary" @click="showNewDocForm = false">取消</AppButton>
              <AppButton type="submit" :variant="newDocTitle.trim() ? 'primary' : 'secondary'" :disabled="!newDocTitle.trim()">创建</AppButton>
            </div>
          </form>
        </AppModal>
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
              <AppButton type="submit" :loading="loading" :variant="newMap.name.trim() ? 'primary' : 'secondary'">保存</AppButton>
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
              <div class="template-icon">
                <img v-if="tpl.avatar" :src="tpl.avatar" class="template-avatar-img" />
                <span v-else>{{ tpl.is_enemy ? '👹' : '🧑' }}</span>
              </div>
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

            <!-- Skills -->
            <details class="template-section-details" style="margin-top:12px" open>
              <summary class="template-section-summary">专长 ({{ templateSkills.length }})</summary>
              <div class="template-section-body">
                <div v-for="(skill, i) in templateSkills" :key="i" class="tpl-skill-row">
                  <span class="tpl-skill-name">{{ skill.name }}</span>
                  <span class="tpl-skill-value">{{ skill.value }}</span>
                  <span class="tpl-skill-attr">[{{ ATTR_MAP[skill.attribute] || skill.attribute }}]</span>
                  <span v-if="skill.is_career" class="tpl-skill-career" title="职业专长">⭐</span>
                  <button type="button" class="tpl-remove-btn" @click="templateSkills.splice(i, 1)">✕</button>
                </div>
                <div class="tpl-add-row">
                  <input v-model="tplNewSkillName" class="tpl-add-input" placeholder="专长名称" />
                  <input v-model.number="tplNewSkillValue" class="tpl-add-input tpl-add-sm" type="number" placeholder="数值" :min="0" :max="80" />
                  <select v-model="tplNewSkillAttr" class="tpl-add-select">
                    <option value="strength">力量</option>
                    <option value="constitution">体质</option>
                    <option value="dexterity">敏捷</option>
                    <option value="intelligence">智力</option>
                    <option value="willpower">意志</option>
                    <option value="charisma">魅力</option>
                  </select>
                  <label class="tpl-checkbox-sm"><input type="checkbox" v-model="tplNewSkillCareer" /> 职业</label>
                  <button type="button" class="tpl-add-btn" :disabled="!tplNewSkillName.trim()" @click="addTplSkill">+</button>
                </div>
              </div>
            </details>

            <!-- Items -->
            <details class="template-section-details" style="margin-top:8px">
              <summary class="template-section-summary">随身物品 ({{ templateItems.length }})</summary>
              <div class="template-section-body">
                <div v-for="(item, i) in templateItems" :key="i" class="tpl-item-row">
                  <span class="tpl-item-icon">{{ item.type === 'weapon' ? '🗡' : item.type === 'tool' ? '🔧' : '📦' }}</span>
                  <span class="tpl-item-name">{{ item.name }}</span>
                  <span v-if="item.detail" class="tpl-item-detail">{{ item.detail }}</span>
                  <button type="button" class="tpl-remove-btn" @click="templateItems.splice(i, 1)">✕</button>
                </div>
                <div class="tpl-add-row">
                  <input v-model="tplNewItemName" class="tpl-add-input" placeholder="物品名称" />
                  <select v-model="tplNewItemType" class="tpl-add-select">
                    <option value="weapon">武器</option>
                    <option value="tool">工具</option>
                    <option value="other">其他</option>
                  </select>
                  <input v-model="tplNewItemDetail" class="tpl-add-input tpl-add-sm" placeholder="详情" />
                  <button type="button" class="tpl-add-btn" :disabled="!tplNewItemName.trim()" @click="addTplItem">+</button>
                </div>
              </div>
            </details>

            <!-- Spells -->
            <details class="template-section-details" style="margin-top:8px">
              <summary class="template-section-summary">法术 ({{ templateSpells.length }})</summary>
              <div class="template-section-body">
                <div v-for="(spell, i) in templateSpells" :key="i" class="tpl-spell-row">
                  <span class="tpl-spell-icon">{{ spell.level === '日常级' ? '✨' : spell.level === '简单级' ? '🔥' : spell.level === '中等级' ? '⚡' : spell.level === '困难级' ? '🔮' : '🌟' }}</span>
                  <span class="tpl-spell-name">{{ spell.name }}</span>
                  <span class="tpl-spell-level">{{ spell.level }}</span>
                  <span class="tpl-spell-cost">{{ spell.mp_cost }}MP</span>
                  <button type="button" class="tpl-remove-btn" @click="templateSpells.splice(i, 1)">✕</button>
                </div>
                <div class="tpl-add-row">
                  <input v-model="tplNewSpellName" class="tpl-add-input" placeholder="法术名称" />
                  <select v-model="tplNewSpellLevel" class="tpl-add-select">
                    <option value="日常级">日常级</option>
                    <option value="简单级">简单级</option>
                    <option value="中等级">中等级</option>
                    <option value="困难级">困难级</option>
                    <option value="传说级">传说级</option>
                  </select>
                  <input v-model.number="tplNewSpellCost" class="tpl-add-input tpl-add-sm" type="number" placeholder="MP" :min="0" />
                  <button type="button" class="tpl-add-btn" :disabled="!tplNewSpellName.trim()" @click="addTplSpell">+</button>
                </div>
              </div>
            </details>
            <div class="form-group">
              <label class="checkbox-label">
                <input type="checkbox" v-model="templateForm.is_enemy" />
                敌方角色
              </label>
            </div>
            <div class="form-actions">
              <AppButton variant="secondary" @click="showTemplateForm = false">取消</AppButton>
              <AppButton type="submit" :loading="loading" :variant="templateForm.name.trim() ? 'primary' : 'secondary'">保存</AppButton>
            </div>
          </form>
        </AppCard>
      </template>

      <!-- ====== 任务板 Tab ====== -->
      <template v-if="activeTab === 'tasks'">
        <AppCard title="任务板">
          <template #header>
            <div class="section-header">
              <h3>任务管理</h3>
              <AppButton size="small" @click="openNewTask">+ 新建任务</AppButton>
            </div>
          </template>
          <p class="tab-hint">任务状态可在房间中由GM手动切换。关键事件时钟在聚光灯推进时自动累积。</p>

          <div class="task-list">
            <div v-for="task in taskList" :key="task.id" class="task-card">
              <div class="task-header">
                <span class="task-status-badge" :class="'status-' + task.status">
                  {{ task.status === 'hidden' ? '🔒 隐藏' : task.status === 'current' ? '🔵 当前' : '✅ 已完成' }}
                </span>
                <span class="task-title">{{ task.title }}</span>
                <span class="task-explore">{{ task.exploration_percent }}%</span>
                <div class="task-actions">
                  <AppButton size="small" variant="ghost" @click="editTask(task)">编辑</AppButton>
                  <AppButton size="small" variant="ghost" @click="deleteTaskItem(task.id)">删除</AppButton>
                </div>
              </div>
              <div v-if="task.clocks && task.clocks.length > 0" class="task-clocks-row">
                <span class="clock-mini" v-for="c in task.clocks" :key="c.id">
                  ⏱ {{ c.current_value }}/{{ c.total }} ({{ c.increment_expr }})
                  <span v-if="c.is_expired" class="clock-expired">超时</span>
                </span>
              </div>
            </div>
            <div v-if="taskList.length === 0" class="empty-state">暂无任务，点击上方按钮创建</div>
          </div>
        </AppCard>

        <!-- 任务编辑弹窗 -->
        <AppModal v-model="showTaskForm" :title="editingTaskId ? '编辑任务' : '新建任务'" size="small">
          <form @submit.prevent="saveTask">
            <AppInput v-model="taskForm.title" label="任务标题" required />
            <div class="form-row">
              <label class="form-label">探索度 %</label>
              <input v-model.number="taskForm.exploration_percent" class="add-input" type="number" min="0" max="100" style="width:80px" />
            </div>
            <div class="form-row">
              <label class="form-label">初始状态</label>
              <select v-model="taskForm.status" class="add-input">
                <option value="hidden">🔒 隐藏</option>
                <option value="current">🔵 当前</option>
                <option value="completed">✅ 已完成</option>
              </select>
            </div>
            <div class="form-row">
              <label class="form-label">排序</label>
              <input v-model.number="taskForm.sort_order" class="add-input" type="number" style="width:80px" />
            </div>

            <!-- 时钟管理 -->
            <div class="clocks-section">
              <div class="clocks-header">
                <span class="form-label">关键事件时钟</span>
                <AppButton size="small" variant="ghost" @click="addClock">+ 添加时钟</AppButton>
              </div>
              <div v-for="(c, i) in taskForm.clocks" :key="i" class="clock-form-row">
                <span>总量</span>
                <input v-model.number="c.total" class="add-input" type="number" min="1" style="width:60px" />
                <span>增量</span>
                <input v-model="c.increment_expr" class="add-input" placeholder="1d3" style="width:80px" />
                <AppButton size="small" variant="ghost" @click="taskForm.clocks.splice(i, 1)">✕</AppButton>
              </div>
            </div>
          </form>
          <template #footer>
            <AppButton variant="secondary" @click="showTaskForm = false">取消</AppButton>
            <AppButton @click="saveTask">保存</AppButton>
          </template>
        </AppModal>
      </template>

      <!-- ====== 章节管理 Tab ====== -->
      <template v-if="activeTab === 'chapters'">
        <AppCard title="章节管理">
          <p class="tab-hint">配置章节和幕的结构。第一条「模组名」默认为模组标题，不可删除。</p>

          <!-- 模组名 (root) -->
          <div class="chapter-root-card">
            <span class="chapter-root-icon">📖</span>
            <span class="chapter-root-label">模组名</span>
            <input :value="module?.title" class="add-input" disabled style="flex:1" />
          </div>

          <!-- 章列表 -->
          <div v-for="(ch, ci) in chaptersList" :key="ci" class="chapter-card">
            <div class="chapter-card-header">
              <span class="chapter-num">第{{ ch.num }}章</span>
              <input v-model="ch.name" class="chapter-name-input" placeholder="章名" />
              <AppButton size="small" variant="ghost" @click="deleteChapter(ci)">🗑</AppButton>
            </div>
            <!-- 幕列表 -->
            <div class="scenes-list">
              <div v-for="(sc, si) in ch.scenes" :key="si" class="scene-row">
                <span class="scene-num">第{{ sc.num }}幕</span>
                <input v-model="sc.name" class="scene-name-input" placeholder="幕名" />
                <AppButton size="small" variant="ghost" @click="deleteScene(ci, si)">✕</AppButton>
              </div>
              <AppButton size="small" variant="ghost" @click="addScene(ci)">+ 添加幕</AppButton>
            </div>
          </div>
          <AppButton @click="addChapter">+ 添加章</AppButton>
          <div style="margin-top:16px">
            <AppButton @click="saveChapters">💾 保存章节配置</AppButton>
          </div>
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
import { ref, reactive, computed, onMounted, onUnmounted, inject } from 'vue'
import { useRoute, useRouter, onBeforeRouteLeave } from 'vue-router'
import { useModulesStore } from '@/stores/modules'
import { resourceService } from '@/services/resourceService'
import mapService from '@/services/mapService'
import { characterTemplateService } from '@/services/characterTemplateService'
import { taskService } from '@/services/taskService'
import AppButton from '@/components/common/AppButton.vue'
import AppCard from '@/components/common/AppCard.vue'
import AppInput from '@/components/common/AppInput.vue'
import AppModal from '@/components/common/AppModal.vue'
import AppSelect from '@/components/common/AppSelect.vue'
import AvatarUploader from '@/components/common/AvatarUploader.vue'
import ResourceEditor from '@/components/editor/ResourceEditor.vue'

const route = useRoute()
const router = useRouter()
const modulesStore = useModulesStore()
const toast = inject('toast')

const module = ref(null)
const resources = ref([])
const maps = ref([])
const characterTemplates = ref([])
const taskList = ref([])
const showTaskForm = ref(false)
const editingTaskId = ref(null)
const taskForm = reactive({
  title: '', exploration_percent: 5, status: 'hidden', sort_order: 0,
  clocks: []
})
const chaptersList = reactive([])
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
  file: null
})

// Document editor state
const editingResourceId = ref(null)
const editingResourceTitle = ref('')
const editingResourceContent = ref('')
let savedResourceContent = ''

const hasUnsavedChanges = computed(() =>
  editingResourceId.value && editingResourceContent.value !== savedResourceContent
)

function beforeUnload(e) {
  if (hasUnsavedChanges.value) {
    e.preventDefault()
    e.returnValue = ''
  }
}

onBeforeRouteLeave((to, from, next) => {
  if (hasUnsavedChanges.value && !confirm('有未保存的修改，确定离开吗？')) {
    next(false)
  } else {
    next()
  }
})

onMounted(() => window.addEventListener('beforeunload', beforeUnload))
onUnmounted(() => window.removeEventListener('beforeunload', beforeUnload))
const showNewDocForm = ref(false)
const newDocTitle = ref('')

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

// Skills/Items/Spells for template form
const templateSkills = ref([])
const templateItems = ref([])
const templateSpells = ref([])
const tplNewSkillName = ref('')
const tplNewSkillValue = ref(10)
const tplNewSkillAttr = ref('strength')
const tplNewSkillCareer = ref(false)
const tplNewItemName = ref('')
const tplNewItemType = ref('weapon')
const tplNewItemDetail = ref('')
const tplNewSpellName = ref('')
const tplNewSpellLevel = ref('简单级')
const tplNewSpellCost = ref(0)

const ATTR_MAP = {
  strength: '力量', constitution: '体质', dexterity: '敏捷',
  intelligence: '智力', willpower: '意志', charisma: '魅力'
}

const typeOptions = [
  { value: 'text', label: '文本' },
  { value: 'image', label: '图片' }
]

onMounted(async () => {
  const moduleId = route.params.id
  try {
    module.value = await modulesStore.fetchModule(moduleId)
    loadChapters()
    await fetchResources()
    await fetchMaps()
    await fetchCharacterTemplates()
    await fetchTasks()
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

function loadChapters() {
  chaptersList.length = 0
  if (module.value?.chapters_config) {
    try {
      const parsed = JSON.parse(module.value.chapters_config)
      if (Array.isArray(parsed)) {
        for (const ch of parsed) {
          chaptersList.push({
            num: ch.num || 1,
            name: ch.name || '',
            scenes: (ch.scenes || []).map(s => ({ num: s.num || 1, name: s.name || '' }))
          })
        }
      }
    } catch {}
  }
}

function addChapter() {
  const nextNum = chaptersList.length > 0 ? Math.max(...chaptersList.map(c => c.num)) + 1 : 1
  chaptersList.push({ num: nextNum, name: '', scenes: [] })
}

function deleteChapter(index) {
  chaptersList.splice(index, 1)
}

function addScene(chapterIndex) {
  const ch = chaptersList[chapterIndex]
  const nextNum = ch.scenes.length > 0 ? Math.max(...ch.scenes.map(s => s.num)) + 1 : 1
  ch.scenes.push({ num: nextNum, name: '' })
}

function deleteScene(chapterIndex, sceneIndex) {
  chaptersList[chapterIndex].scenes.splice(sceneIndex, 1)
}

async function saveChapters() {
  try {
    const config = chaptersList.map(ch => ({
      num: ch.num,
      name: ch.name,
      scenes: ch.scenes.map(s => ({ num: s.num, name: s.name }))
    }))
    await modulesStore.updateModule(module.value.id, {
      chapters_config: JSON.stringify(config)
    })
    if (module.value) module.value.chapters_config = JSON.stringify(config)
    toast.success('章节配置已保存')
  } catch (e) {
    toast.error('保存失败')
  }
}

async function saveTheme(theme) {
  try {
    await modulesStore.updateModule(module.value.id, { theme })
    if (module.value) module.value.theme = theme
    toast.success('推荐主题已更新')
  } catch (e) {
    toast.error('主题更新失败')
  }
}

// ====== Task Board ======

async function fetchTasks() {
  try {
    taskList.value = await taskService.getModuleTasks(route.params.id)
  } catch {}
}

function openNewTask() {
  editingTaskId.value = null
  Object.assign(taskForm, { title: '', exploration_percent: 5, status: 'hidden', sort_order: taskList.value.length, clocks: [] })
  showTaskForm.value = true
}

function editTask(task) {
  editingTaskId.value = task.id
  const clocks = (task.clocks || []).map(c => ({ id: c.id, total: c.total, increment_expr: c.increment_expr, current_value: c.current_value || 0, is_expired: c.is_expired || false }))
  Object.assign(taskForm, { title: task.title, exploration_percent: task.exploration_percent, status: task.status, sort_order: task.sort_order, clocks })
  showTaskForm.value = true
}

function addClock() {
  taskForm.clocks.push({ total: 6, increment_expr: '1d3' })
}

async function saveTask() {
  try {
    const payload = {
      title: taskForm.title, exploration_percent: taskForm.exploration_percent,
      status: taskForm.status, sort_order: taskForm.sort_order
    }
    if (editingTaskId.value) {
      const updated = await taskService.updateTask(editingTaskId.value, payload)
      // Sync clocks: delete removed, create new, update existing
      const savedClockIds = taskForm.clocks.filter(c => c.id).map(c => c.id)
      if (updated.clocks) {
        for (const c of updated.clocks) {
          if (!savedClockIds.includes(c.id)) await taskService.deleteClock(c.id)
        }
      }
      for (const c of taskForm.clocks) {
        if (c.id) {
          await taskService.updateClock(c.id, { total: c.total, increment_expr: c.increment_expr })
        } else {
          await taskService.createClock(editingTaskId.value, { total: c.total, increment_expr: c.increment_expr })
        }
      }
    } else {
      const created = await taskService.createTask(route.params.id, payload)
      for (const c of taskForm.clocks) {
        await taskService.createClock(created.id, { total: c.total, increment_expr: c.increment_expr })
      }
    }
    showTaskForm.value = false
    await fetchTasks()
    toast.success('任务已保存')
  } catch (e) {
    toast.error('保存失败')
  }
}

async function deleteTaskItem(taskId) {
  if (!confirm('确定删除此任务？')) return
  try {
    await taskService.deleteTask(taskId)
    await fetchTasks()
    toast.success('任务已删除')
  } catch (e) {
    toast.error('删除失败')
  }
}

// ====== Resources (Document System) ======

function openNewDocForm() {
  newDocTitle.value = ''
  showNewDocForm.value = true
}

async function handleCreateDoc() {
  if (!newDocTitle.value.trim()) { toast.error('请输入文档标题'); return }

  loading.value = true
  try {
    // Create with empty TipTap JSON document
    const emptyDoc = JSON.stringify({ type: 'doc', content: [{ type: 'paragraph' }] })
    await resourceService.createResource(route.params.id, {
      type: 'text',
      title: newDocTitle.value.trim(),
      content: emptyDoc,
    })
    toast.success('文档已创建')
    showNewDocForm.value = false
    await fetchResources()
  } catch (error) {
    toast.error(error.message || '创建失败')
  } finally {
    loading.value = false
  }
}

function openDocEditor(resource) {
  editingResourceId.value = resource.id
  editingResourceTitle.value = resource.title
  editingResourceContent.value = resource.content || ''
  savedResourceContent = resource.content || ''
}

function closeDocEditor() {
  editingResourceId.value = null
  editingResourceTitle.value = ''
  editingResourceContent.value = ''
  savedResourceContent = ''
}

async function saveDocContent() {
  if (!editingResourceId.value) return
  loading.value = true
  try {
    await resourceService.updateResource(editingResourceId.value, {
      title: editingResourceTitle.value.trim(),
      content: editingResourceContent.value,
    })
    savedResourceContent = editingResourceContent.value
    toast.success('文档已保存')
    await fetchResources()
  } catch (error) {
    toast.error(error.message || '保存失败')
  } finally {
    loading.value = false
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
    try { templateSkills.value = JSON.parse(tpl.skills || '[]') } catch { templateSkills.value = [] }
    try { templateItems.value = JSON.parse(tpl.items || '[]') } catch { templateItems.value = [] }
    try { templateSpells.value = JSON.parse(tpl.spells || '[]') } catch { templateSpells.value = [] }
  } else {
    Object.assign(templateForm, { name: '', avatar: '', profession: '', hp: 10, max_hp: 10, san: 50, mp: 0, max_mp: 0, notes: '', is_enemy: false })
    Object.assign(templateFormAttrs, { strength: 50, constitution: 50, dexterity: 50, intelligence: 50, willpower: 50, charisma: 50 })
    templateSkills.value = []
    templateItems.value = []
    templateSpells.value = []
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
      skills: JSON.stringify(templateSkills.value),
      items: JSON.stringify(templateItems.value),
      spells: JSON.stringify(templateSpells.value)
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

function addTplSkill() {
  if (!tplNewSkillName.value.trim()) return
  templateSkills.value.push({
    name: tplNewSkillName.value.trim(),
    value: tplNewSkillValue.value || 10,
    attribute: tplNewSkillAttr.value,
    is_career: tplNewSkillCareer.value
  })
  tplNewSkillName.value = ''
  tplNewSkillValue.value = 10
  tplNewSkillCareer.value = false
}

function addTplItem() {
  if (!tplNewItemName.value.trim()) return
  templateItems.value.push({
    name: tplNewItemName.value.trim(),
    type: tplNewItemType.value,
    detail: tplNewItemDetail.value.trim()
  })
  tplNewItemName.value = ''
  tplNewItemDetail.value = ''
}

function addTplSpell() {
  if (!tplNewSpellName.value.trim()) return
  templateSpells.value.push({
    name: tplNewSpellName.value.trim(),
    level: tplNewSpellLevel.value,
    mp_cost: tplNewSpellCost.value || 0
  })
  tplNewSpellName.value = ''
  tplNewSpellCost.value = 0
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
.module-edit-header h2 { font-family: var(--font-display); font-size: 22px; color: var(--accent-gold); letter-spacing: 0.04em; flex: 1; }
.header-theme-select { display: flex; align-items: center; gap: 6px; }
.theme-label { font-size: 12px; color: var(--text-muted); white-space: nowrap; }
.header-theme-select select {
  padding: 4px 8px; font-size: 13px; font-family: var(--font-body);
  border: 1px solid var(--border-default); border-radius: var(--radius-sm);
  background: var(--bg-input); color: var(--text-primary); cursor: pointer;
}

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
  cursor: pointer;
  transition: border-color 0.15s;
}
.resource-item:hover { border-color: var(--accent-gold); }

.resource-doc-icon { font-size: 18px; flex-shrink: 0; }
.resource-info { flex: 1; display: flex; flex-direction: column; gap: 2px; }
.resource-title { font-weight: 500; color: var(--text-primary); font-size: 14px; }
.resource-type { color: var(--text-muted); font-size: 14px; }

/* ====== Document Editor ====== */
.doc-editor-view { display: flex; flex-direction: column; gap: 12px; }

.doc-editor-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
}

.doc-title-input { flex: 1; }
.doc-title-input :deep(input) { font-size: 16px; font-weight: 600; font-family: var(--font-display); }

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

/* ====== Template avatar ====== */
.template-avatar-img { width: 100%; height: 100%; object-fit: cover; border-radius: 50%; }

/* ====== Template skills/items/spells sections ====== */
.template-section-details { border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 8px 12px; }
.template-section-summary { font-size: 13px; color: var(--text-muted); cursor: pointer; font-weight: 600; }
.template-section-body { margin-top: 6px; display: flex; flex-direction: column; gap: 4px; }

.tpl-skill-row, .tpl-item-row, .tpl-spell-row { display: flex; align-items: center; gap: 6px; padding: 2px 0; }
.tpl-skill-name, .tpl-item-name, .tpl-spell-name { font-size: 13px; color: var(--text-primary); }
.tpl-skill-value { font-size: 13px; font-weight: 600; color: var(--text-secondary); min-width: 20px; }
.tpl-skill-attr { font-size: 11px; color: var(--text-muted); background: var(--bg-secondary); padding: 0 4px; border-radius: 3px; }
.tpl-skill-career { font-size: 11px; }
.tpl-item-icon, .tpl-spell-icon { font-size: 13px; }
.tpl-item-detail { font-size: 12px; color: var(--text-muted); flex: 1; }
.tpl-spell-level { font-size: 11px; color: var(--text-muted); }
.tpl-spell-cost { font-size: 11px; color: #a855f7; }

.tpl-remove-btn {
  background: none; border: none; color: var(--text-muted); cursor: pointer;
  font-size: 12px; padding: 2px 4px; transition: color 0.15s;
}
.tpl-remove-btn:hover { color: var(--color-danger); }

.tpl-add-row { display: flex; align-items: center; gap: 4px; margin-top: 4px; flex-wrap: wrap; }
.tpl-add-input {
  padding: 4px 8px; font-size: 12px; font-family: var(--font-body);
  border: 1px solid var(--border-default); border-radius: var(--radius-sm);
  background: var(--bg-input); color: var(--text-primary); outline: none;
}
.tpl-add-input:focus { border-color: var(--border-focus); }
.tpl-add-sm { width: 52px; }
.tpl-add-select {
  padding: 4px 6px; font-size: 12px; font-family: var(--font-body);
  border: 1px solid var(--border-default); border-radius: var(--radius-sm);
  background: var(--bg-input); color: var(--text-primary); outline: none;
}
.tpl-add-btn {
  padding: 4px 10px; border: 1px solid var(--border-default); border-radius: var(--radius-sm);
  background: transparent; color: var(--text-secondary); cursor: pointer;
  font-size: 13px; font-family: var(--font-body); transition: all 0.15s;
}
.tpl-add-btn:hover:not(:disabled) { border-color: var(--accent-gold); color: var(--accent-gold); }
.tpl-add-btn:disabled { opacity: 0.4; cursor: default; }
.tpl-checkbox-sm { display: flex; align-items: center; gap: 3px; font-size: 11px; color: var(--text-muted); cursor: pointer; white-space: nowrap; }
.tpl-checkbox-sm input { accent-color: var(--accent-gold); }

/* ====== Task Board ====== */
.task-list { display: flex; flex-direction: column; gap: 8px; }
.task-card { padding: 10px 14px; background: var(--bg-card); border-radius: var(--radius-md); border: 1px solid var(--border-subtle); }
.task-header { display: flex; align-items: center; gap: 10px; }
.task-status-badge { font-size: 11px; padding: 2px 8px; border-radius: 10px; font-weight: 500; }
.task-status-badge.status-hidden { background: rgba(156,163,175,0.15); color: #9ca3af; }
.task-status-badge.status-current { background: var(--color-info-dim); color: var(--color-info); }
.task-status-badge.status-completed { background: var(--color-success-dim); color: var(--color-success); }
.task-title { flex: 1; font-weight: 600; font-size: 14px; color: var(--text-primary); }
.task-chapter { font-size: 11px; color: var(--text-muted); }
.task-explore { font-size: 11px; color: var(--accent-gold); font-weight: 600; }
.task-actions { display: flex; gap: 4px; }
.task-clocks-row { margin-top: 6px; display: flex; gap: 8px; flex-wrap: wrap; }
.clock-mini { font-size: 11px; padding: 2px 8px; border-radius: 8px; background: rgba(0,0,0,0.2); color: var(--text-muted); }
.clock-expired { color: var(--color-danger); font-weight: 600; }
.clocks-section { margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--border-subtle); }
.clocks-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px; }
.clock-form-row { display: flex; align-items: center; gap: 6px; margin-bottom: 4px; font-size: 12px; color: var(--text-muted); }
.form-row { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.form-label { font-size: 12px; color: var(--text-muted); min-width: 80px; }

/* ====== Chapter Management ====== */
.chapter-root-card { display: flex; align-items: center; gap: 10px; padding: 12px; background: var(--bg-card); border: 1px solid var(--accent-gold); border-radius: var(--radius-md); margin-bottom: 12px; }
.chapter-root-icon { font-size: 20px; }
.chapter-root-label { font-size: 12px; color: var(--text-muted); font-weight: 600; white-space: nowrap; }
.chapter-card { margin-bottom: 12px; padding: 12px; background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); }
.chapter-card-header { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.chapter-num { font-size: 14px; font-weight: 700; color: var(--accent-gold); white-space: nowrap; }
.chapter-name-input { flex: 1; padding: 4px 8px; font-size: 14px; border: 1px solid var(--border-default); border-radius: var(--radius-sm); background: var(--bg-input); color: var(--text-primary); }
.scenes-list { margin-left: 24px; display: flex; flex-direction: column; gap: 4px; }
.scene-row { display: flex; align-items: center; gap: 8px; }
.scene-num { font-size: 12px; color: var(--text-muted); white-space: nowrap; min-width: 50px; }
.scene-name-input { flex: 1; padding: 3px 8px; font-size: 13px; border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); background: var(--bg-input); color: var(--text-primary); }
</style>
