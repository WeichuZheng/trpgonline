<template>
  <div class="game-room">
    <div class="game-header">
      <AppButton variant="ghost" @click="leaveRoom">← 退出房间</AppButton>
      <h2>{{ currentRoom?.name }}</h2>
      <div v-if="onlineUsers.length > 0" class="online-users">
        <span class="online-dot"></span>
        <span v-for="(u, i) in onlineUsers" :key="u.user_id" class="online-name">
          {{ u.username }}<span v-if="i < onlineUsers.length - 1">,</span>
        </span>
      </div>
      <button v-if="isGM" class="mode-toggle" @click="toggleBattleMode" :class="{ active: battleMode }">
        {{ battleMode ? '⚔ 战斗模式' : '📖 叙事模式' }}
        <span class="mode-switch-hint">切换</span>
      </button>
      <span class="room-status" :class="'status-' + currentRoom?.status">{{ getStatusLabel(currentRoom?.status) }}</span>
    </div>

    <!-- ====== 叙事模式：三栏布局 ====== -->
    <div v-if="!battleMode" class="game-content narrative-mode">
      <div class="game-left" :style="{ width: leftPanelWidth + 'px', flexShrink: 0 }">
        <AppCard title="角色">
          <div class="character-list">
            <CharacterSheet
              v-for="char in playerCharacters"
              :key="char.id"
              :char="char"
              :is-g-m="isGM"
              :show-place-on-map="battleMode"
              @update="onCharacterUpdate"
              @edit="editCharacter"
              @delete="deleteCharacter"
              @place-on-map="placeCharOnMap"
            />
            <div v-if="npcCharacters.length > 0" class="char-section-divider">NPC</div>
            <CharacterSheet
              v-for="char in npcCharacters"
              :key="char.id"
              :char="char"
              :is-g-m="isGM"
              :show-place-on-map="battleMode"
              @update="onCharacterUpdate"
              @edit="editCharacter"
              @delete="deleteCharacter"
              @place-on-map="placeCharOnMap"
            />
            <div v-if="gameStore.characters.length === 0" class="empty-state">暂无角色</div>
          </div>

          <!-- GM 添加角色区域 -->
          <div v-if="isGM" class="gm-add-character">
            <div class="add-section-title">添加角色</div>
            <div class="add-source-tabs">
              <button class="add-tab" :class="{ active: addCharSource === 'template' }" @click="addCharSource = 'template'">模板</button>
              <button class="add-tab" :class="{ active: addCharSource === 'custom' }" @click="addCharSource = 'custom'">自定义</button>
            </div>
            <!-- 模板快速添加 -->
            <div v-if="addCharSource === 'template'" class="add-template-list">
              <button v-for="tpl in characterTemplates" :key="tpl.id" class="add-template-btn" @click="addCharFromTemplate(tpl)">
                <span class="tpl-icon">
                  <img v-if="tpl.avatar" :src="tpl.avatar" class="tpl-avatar-img" />
                  <span v-else>{{ tpl.is_enemy ? '&#x1F47E;' : '&#x1F9D1;' }}</span>
                </span>
                <span class="tpl-name">{{ tpl.name }}</span>
                <span v-if="tpl.profession" class="tpl-prof">{{ tpl.profession }}</span>
                <span class="tpl-stats">HP{{ tpl.max_hp }}</span>
              </button>
              <div v-if="characterTemplates.length === 0" class="add-empty">暂无模板，请在模组编辑中创建</div>
            </div>
            <!-- 自定义添加 -->
            <div v-if="addCharSource === 'custom'" class="add-custom-form">
              <input v-model="quickCharName" class="add-input" placeholder="角色名称" />
              <div class="quick-avatar-row">
                <span class="quick-avatar-label">头像</span>
                <AvatarUploader v-model="quickCharAvatar" />
              </div>
              <input v-model="quickCharProfession" class="add-input" placeholder="职业 (可选)" />
              <div class="add-custom-stats">
                <div class="add-stats-row">
                  <label class="add-stats-label">HP</label>
                  <input v-model.number="quickCharHp" class="add-input add-stat" type="number" :min="1" />
                  <span class="add-stats-sep">/</span>
                  <input v-model.number="quickCharMaxHp" class="add-input add-stat" type="number" :min="1" />
                </div>
                <div class="add-stats-row">
                  <label class="add-stats-label">SAN</label>
                  <input v-model.number="quickCharSan" class="add-input add-stat" type="number" :min="0" />
                </div>
                <div class="add-stats-row">
                  <label class="add-stats-label">MP</label>
                  <input v-model.number="quickCharMp" class="add-input add-stat" type="number" :min="0" />
                  <span class="add-stats-sep">/</span>
                  <input v-model.number="quickCharMaxMp" class="add-input add-stat" type="number" :min="0" />
                </div>
              </div>
              <details class="add-attrs-details">
                <summary class="add-attrs-summary">六维属性 (可选)</summary>
                <div class="add-attrs-grid">
                  <div class="add-attrs-row" v-for="(label, key) in ATTR_MAP" :key="key">
                    <label class="add-stats-label">{{ label }}</label>
                    <input v-model.number="quickCharAttrs[key]" class="add-input add-stat" type="number" :min="1" :max="99" />
                  </div>
                </div>
              </details>
              <div class="add-custom-row">
                <label class="add-checkbox"><input type="checkbox" v-model="quickCharIsEnemy" /> NPC / 敌方</label>
              </div>
              <AppButton size="small" @click="addCharCustom" :disabled="!quickCharName.trim()">添加</AppButton>
            </div>
          </div>
        </AppCard>
      </div>

      <div class="resize-handle" @mousedown="startResizeLeft"></div>

      <div class="game-center">
        <AppCard title="资源" class="resource-card-wrap">
          <div class="resource-grid">
            <div v-for="resource in gameStore.resources" :key="resource.id" class="resource-card" :class="{ 'is-hidden': !resource.is_shown }">
              <div v-if="resource.type === 'image'" class="image-resource"><img :src="resource.content" :alt="resource.title"></div>
              <div v-if="resource.type === 'text'" class="text-resource">
                <span class="resource-display-type">{{ getDisplayTypeLabel(resource.display_type) }}</span>
                <h4>{{ resource.title }}</h4>
                <p>{{ resource.content }}</p>
              </div>
              <AppButton v-if="isGM" size="small" variant="secondary" @click="toggleResourceVisibility(resource)">{{ resource.is_shown ? '隐藏' : '显示' }}</AppButton>
            </div>
            <div v-if="gameStore.resources.length === 0" class="empty-state">暂无资源</div>
          </div>
        </AppCard>
      </div>

      <div class="game-right">
        <DicePanel
          :characters="gameStore.characters"
          :selected-character-id="selectedCharacterId"
          @update:selected-character-id="selectedCharacterId = $event"
          :selected-quick-dice="selectedQuickDice"
          @update:selected-quick-dice="selectedQuickDice = $event"
          :dice-expr="diceExpr"
          @update:dice-expr="diceExpr = $event"
          :dice-reason="diceReason"
          @update:dice-reason="diceReason = $event"
          @roll-quick="rollQuickDice"
          @roll-expr="rollExprDice"
        />
        <LogPanel :logs="gameStore.gameLogs" :is-gm="isGM" @clear-logs="clearLogs" @add-log="addCustomLog" />
      </div>
    </div>

    <!-- ====== 战斗模式：地图全屏 + 可折叠侧栏 ====== -->
    <div v-else class="game-content battle-mode">
      <!-- 左侧面板：角色 -->
      <div class="sidebar-left" :class="{ collapsed: leftCollapsed }" :style="!leftCollapsed ? { width: leftPanelWidth + 'px' } : {}">
        <button class="sidebar-toggle" @click="leftCollapsed = !leftCollapsed">
          {{ leftCollapsed ? '→' : '←' }}
        </button>
        <div v-if="!leftCollapsed" class="sidebar-content">
          <AppCard title="角色" class="sidebar-card">
            <div class="character-list compact">
              <CharacterSheet
                v-for="char in playerCharacters"
                :key="char.id"
                :char="char"
                :is-g-m="isGM"
                :show-place-on-map="battleMode"
                @update="onCharacterUpdate"
                @edit="editCharacter"
                @delete="deleteCharacter"
                @place-on-map="placeCharOnMap"
              />
              <div v-if="npcCharacters.length > 0" class="char-section-divider">NPC</div>
              <CharacterSheet
                v-for="char in npcCharacters"
                :key="char.id"
                :char="char"
                :is-g-m="isGM"
                :show-place-on-map="battleMode"
                @update="onCharacterUpdate"
                @edit="editCharacter"
                @delete="deleteCharacter"
                @place-on-map="placeCharOnMap"
              />
            </div>
          </AppCard>
        </div>
        <div v-if="!leftCollapsed" class="resize-handle-vertical" @mousedown="startResizeLeft"></div>
      </div>

      <!-- 中间：地图画布 -->
      <div class="battle-map-area">
        <MapCanvas
          v-if="gameStore.activeMap"
          ref="mapCanvasRef"
          :map-data="gameStore.activeMap"
          :units="gameStore.mapUnits"
          :is-gm="isGM"
          @add-token="openTokenForm"
          @unit-move="onUnitMove"
          @unit-update="onUnitUpdate"
        />
        <div v-else class="no-map-placeholder">
          <div v-if="isGM" class="gm-map-select">
            <div class="no-map-text">请选择激活地图</div>
            <div v-if="moduleMaps.length > 0" class="map-select-list">
              <button v-for="m in moduleMaps" :key="m.id" class="map-select-btn" @click="selectActiveMap(m.id)">
                {{ m.name }}
              </button>
            </div>
            <div v-else class="no-map-text">当前模组没有地图，请先在模组编辑中上传</div>
          </div>
          <div v-else class="no-map-text">等待 GM 选择地图...</div>
        </div>
      </div>

      <!-- 右侧面板：骰子+日志 -->
      <div class="sidebar-right" :class="{ collapsed: rightCollapsed }">
        <button class="sidebar-toggle" @click="rightCollapsed = !rightCollapsed">
          {{ rightCollapsed ? '←' : '→' }}
        </button>
        <div v-if="!rightCollapsed" class="sidebar-content">
          <DicePanel
            :characters="gameStore.characters"
            :selected-character-id="selectedCharacterId"
            @update:selected-character-id="selectedCharacterId = $event"
            :selected-quick-dice="selectedQuickDice"
            @update:selected-quick-dice="selectedQuickDice = $event"
            :dice-expr="diceExpr"
            @update:dice-expr="diceExpr = $event"
            :dice-reason="diceReason"
            @update:dice-reason="diceReason = $event"
            @roll-quick="rollQuickDice"
            @roll-expr="rollExprDice"
            compact
          />
          <LogPanel :logs="gameStore.gameLogs" :is-gm="isGM" compact @clear-logs="clearLogs" @add-log="addCustomLog" />
        </div>
      </div>
    </div>

    <!-- 角色卡创建/编辑弹窗 -->
    <AppModal v-model="showCharacterForm" :title="editingCharacter ? '编辑角色卡' : '创建角色卡'" size="small">
      <form @submit.prevent="saveCharacter">
        <AppInput v-model="characterForm.name" label="角色名称" placeholder="请输入角色名称" required></AppInput>
        <AppInput v-model="characterForm.profession" label="职业" placeholder="职业 (可选)"></AppInput>
        <div class="form-row-label">头像</div>
        <AvatarUploader v-model="characterForm.avatar" />
        <div class="stats-input">
          <AppInput v-model.number="characterForm.hp" type="number" label="当前HP" :min="0"></AppInput>
          <span class="stats-divider">/</span>
          <AppInput v-model.number="characterForm.max_hp" type="number" label="最大HP" :min="1"></AppInput>
        </div>
        <div class="stats-input">
          <AppInput v-model.number="characterForm.san" type="number" label="SAN" :min="0"></AppInput>
        </div>
        <div class="stats-input">
          <AppInput v-model.number="characterForm.mp" type="number" label="当前MP" :min="0"></AppInput>
          <span class="stats-divider">/</span>
          <AppInput v-model.number="characterForm.max_mp" type="number" label="最大MP" :min="0"></AppInput>
        </div>
        <details class="add-attrs-details" style="margin-top:8px">
          <summary class="add-attrs-summary">六维属性</summary>
          <div class="add-attrs-grid">
            <div class="add-attrs-row" v-for="(label, key) in ATTR_MAP" :key="key">
              <label class="add-stats-label">{{ label }}</label>
              <input v-model.number="characterFormAttrs[key]" class="add-input add-stat" type="number" :min="1" :max="99" />
            </div>
          </div>
        </details>
        <div v-if="isGM && !editingCharacter" class="token-form-row">
          <label><input type="checkbox" v-model="characterForm.is_npc" /> NPC角色</label>
        </div>
      </form>
      <template #footer>
        <AppButton variant="secondary" @click="closeCharacterForm">取消</AppButton>
        <AppButton @click="saveCharacter">保存</AppButton>
      </template>
    </AppModal>

    <!-- Token 创建弹窗 -->
    <AppModal v-model="showTokenForm" title="添加 Token" size="small">
      <form @submit.prevent="saveToken">
        <AppInput v-model="tokenForm.name" label="名称" placeholder="Token 名称" required></AppInput>
        <div class="form-row-label">头像</div>
        <AvatarUploader v-model="tokenForm.icon" />
        <div class="stats-input">
          <AppInput v-model.number="tokenForm.hp" type="number" label="HP" :min="0"></AppInput>
          <span class="stats-divider">/</span>
          <AppInput v-model.number="tokenForm.max_hp" type="number" label="最大HP" :min="1"></AppInput>
        </div>
        <div class="token-form-row">
          <label><input type="checkbox" v-model="tokenForm.is_enemy" /> 敌方</label>
        </div>
        <div class="stats-input">
          <AppInput v-model.number="tokenForm.width" type="number" label="宽(格)" :min="0.5" step="0.5"></AppInput>
          <span class="stats-divider">×</span>
          <AppInput v-model.number="tokenForm.height" type="number" label="高(格)" :min="0.5" step="0.5"></AppInput>
        </div>
      </form>
      <template #footer>
        <AppButton variant="secondary" @click="showTokenForm = false">取消</AppButton>
        <AppButton @click="saveToken">放置</AppButton>
      </template>
    </AppModal>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, nextTick, onMounted, onUnmounted, inject } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useRoomsStore } from '@/stores/rooms'
import { useGameStore } from '@/stores/game'
import { roomService } from '@/services/roomService'
import { characterService } from '@/services/characterService'
import { diceService } from '@/services/diceService'
import { characterTemplateService } from '@/services/characterTemplateService'
import mapService from '@/services/mapService'
import AppButton from '@/components/common/AppButton.vue'
import AppCard from '@/components/common/AppCard.vue'
import AppInput from '@/components/common/AppInput.vue'
import AppModal from '@/components/common/AppModal.vue'
import MapCanvas from '@/components/map/MapCanvas.vue'
import DicePanel from '@/components/game/DicePanel.vue'
import LogPanel from '@/components/game/LogPanel.vue'
import CharacterSheet from '@/components/game/CharacterSheet.vue'
import AvatarUploader from '@/components/common/AvatarUploader.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const roomsStore = useRoomsStore()
const gameStore = useGameStore()
const toast = inject('toast')

const currentRoom = ref(null)
const selectedQuickDice = ref(null)
const diceExpr = ref('')
const diceReason = ref('')
const selectedCharacterId = ref(null)
const showCharacterForm = ref(false)
const editingCharacter = ref(null)
const battleMode = ref(false)
const leftCollapsed = ref(false)
const rightCollapsed = ref(false)
const leftPanelWidth = ref(260)
const isResizingLeft = ref(false)
const showTokenForm = ref(false)
const mapCanvasRef = ref(null)
const moduleMaps = ref([])
const characterTemplates = ref([])
const addCharSource = ref('template')
const quickCharName = ref('')
const quickCharProfession = ref('')
const quickCharAvatar = ref('')
const quickCharIsEnemy = ref(false)
const quickCharHp = ref(10)
const quickCharMaxHp = ref(10)
const quickCharSan = ref(50)
const quickCharMp = ref(0)
const quickCharMaxMp = ref(0)
const quickCharAttrs = reactive({
  strength: 50, constitution: 50, dexterity: 50,
  intelligence: 50, willpower: 50, charisma: 50
})

const ATTR_MAP = {
  strength: '力量', constitution: '体质', dexterity: '敏捷',
  intelligence: '智力', willpower: '意志', charisma: '魅力'
}
const isGM = computed(() => currentRoom.value?.gm_id === authStore.user?.id)
const onlineUsers = ref([])

const playerCharacters = computed(() => gameStore.characters.filter(c => !c.is_npc))
const npcCharacters = computed(() => gameStore.characters.filter(c => c.is_npc))

const selectedCharacterName = computed(() => {
  if (!selectedCharacterId.value) return null
  const char = gameStore.characters.find(c => c.id === selectedCharacterId.value)
  return char?.name || null
})

const logContainer = ref(null)

watch(() => gameStore.gameLogs.length, async () => {
  await nextTick()
  if (logContainer.value) {
    logContainer.value.scrollTop = logContainer.value.scrollHeight
  }
})

const characterForm = reactive({
  name: '', avatar: '', profession: '', hp: 10, max_hp: 10, san: 50, mp: 0, max_mp: 0, notes: '', is_npc: false
})

const characterFormAttrs = reactive({
  strength: 50, constitution: 50, dexterity: 50,
  intelligence: 50, willpower: 50, charisma: 50
})

const tokenForm = reactive({
  name: '', icon: '', hp: 10, max_hp: 10, is_enemy: false, width: 1, height: 1
})

let ws = null
let wsReconnectTimer = null
let visibilityHandler = null

async function loadGameState() {
  const roomId = route.params.id
  currentRoom.value = await roomsStore.fetchRoom(roomId)
  gameStore.setRoomId(roomId)

  const resources = await roomService.getRoomResources(roomId)
  gameStore.setResources(Array.isArray(resources) ? resources : [])

  const characters = await characterService.getRoomCharacters(roomId)
  gameStore.setCharacters(Array.isArray(characters) ? characters : [])

  const logs = await diceService.getRoomLogs(roomId)
  gameStore.setGameLogs(Array.isArray(logs) ? logs : [])

  // Load online users
  try {
    onlineUsers.value = await roomService.getOnlineUsers(roomId)
  } catch {}

  // Load character templates for GM quick-add
  if (isGM.value) {
    try {
      characterTemplates.value = await characterTemplateService.getRoomTemplates(roomId)
    } catch {}
  }

  if (currentRoom.value?.active_map_id) {
    await loadActiveMap()
  }
}

async function loadActiveMap() {
  try {
    const mapData = await mapService.getRoomMap(route.params.id)
    gameStore.setActiveMap(mapData)
    gameStore.setMapUnits(mapData.units || [])
  } catch {
    gameStore.setActiveMap(null)
    gameStore.setMapUnits([])
  }
}

onMounted(async () => {
  try {
    await loadGameState()
    connectWebSocket()
    setupVisibilityRestore()
  } catch (error) {
    toast.error('加载房间失败: ' + (error.message || '未知错误'))
  }
})

onUnmounted(() => {
  if (ws) ws.close()
  if (wsReconnectTimer) clearTimeout(wsReconnectTimer)
  if (visibilityHandler) document.removeEventListener('visibilitychange', visibilityHandler)
  gameStore.clearGame()
})

function setupVisibilityRestore() {
  visibilityHandler = async () => {
    if (document.visibilityState === 'visible' && route.params.id) {
      try { await loadGameState() } catch {}
      if (!ws || ws.readyState !== WebSocket.OPEN) {
        connectWebSocket()
      }
    }
  }
  document.addEventListener('visibilitychange', visibilityHandler)
}

function connectWebSocket() {
  if (wsReconnectTimer) {
    clearTimeout(wsReconnectTimer)
    wsReconnectTimer = null
  }

  const roomId = route.params.id
  const userId = authStore.user?.id
  const username = authStore.user?.username || '匿名'
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  const wsUrl = `${protocol}//${window.location.host}/ws/room/${roomId}?user_id=${userId}&username=${encodeURIComponent(username)}`

  ws = new WebSocket(wsUrl)
  ws.onopen = () => { gameStore.setWsConnected(true) }
  ws.onmessage = (event) => {
    try { handleWsMessage(JSON.parse(event.data)) } catch {}
  }
  ws.onclose = () => {
    gameStore.setWsConnected(false)
    wsReconnectTimer = setTimeout(() => {
      if (route.params.id) connectWebSocket()
    }, 3000)
  }
  ws.onerror = () => {}
  gameStore.setWs(ws)
}

function handleWsMessage(data) {
  switch (data.type) {
    case 'user_joined':
    case 'user_left':
      gameStore.addGameLog({ action: 'custom', detail: data.message, username: data.username })
      break
    case 'dice_result':
      gameStore.setDiceResult({ result: data.result, details: data.details, reason: data.reason })
      gameStore.addGameLog({ action: 'dice', detail: data.details, username: data.rolled_by })
      break
    case 'resource_toggled':
      gameStore.updateResourceVisibility(data.resource_id, data.is_visible)
      break
    case 'hp_updated':
      gameStore.addGameLog({ action: data.type, detail: `${data.unit_name}: HP ${data.hp}/${data.max_hp}`, username: data.changed_by })
      break
    case 'unit_moved':
      gameStore.updateMapUnit(data.unit_id, { x: data.x, y: data.y })
      gameStore.addGameLog({ action: 'move', detail: `${data.unit_name} 移动到 (${Math.round(data.x)}, ${Math.round(data.y)})`, username: data.moved_by })
      break
    case 'unit_created':
      if (data.unit) gameStore.addMapUnit(data.unit)
      break
    case 'unit_updated':
      if (data.updates) gameStore.updateMapUnit(data.unit_id, data.updates)
      break
    case 'unit_deleted':
      gameStore.removeMapUnit(data.unit_id)
      break
    case 'active_map_changed':
      loadActiveMap()
      break
    case 'log_added':
      gameStore.addGameLog({ action: data.action, detail: data.detail, username: data.username })
      break
    case 'online_users':
      onlineUsers.value = data.users || []
      break
  }
}

function toggleBattleMode() {
  battleMode.value = !battleMode.value
  if (battleMode.value && currentRoom.value?.active_map_id && !gameStore.activeMap) {
    loadActiveMap()
  }
  if (battleMode.value && isGM.value && moduleMaps.value.length === 0) {
    loadModuleMaps()
  }
}

async function loadModuleMaps() {
  try {
    const moduleId = currentRoom.value?.module_id
    if (moduleId) {
      moduleMaps.value = await mapService.getModuleMaps(moduleId)
    }
  } catch {}
}

async function selectActiveMap(mapId) {
  try {
    await mapService.setActiveMap(route.params.id, mapId)
    await loadActiveMap()
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'active_map_changed', map_id: mapId }))
    }
  } catch (error) {
    toast.error(error.message || '设置地图失败')
  }
}

function getStatusLabel(status) {
  const labels = { waiting: '等待中', active: '进行中', ended: '已结束' }
  return labels[status] || status
}

function getDisplayTypeLabel(type) {
  const labels = { story: '背景故事', rule: '规则说明', clue: '线索卡', character: '角色描述', mission: '任务目标' }
  return labels[type] || type
}

function hpColor(hp, maxHp) {
  const pct = hp / maxHp
  if (pct > 0.5) return 'hp-green'
  if (pct > 0.25) return 'hp-yellow'
  return 'hp-red'
}

function formatTime(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

async function toggleResourceVisibility(resource) {
  const newVisibility = !resource.is_shown
  try {
    await roomService.toggleResourceVisibility(route.params.id, resource.id, newVisibility)
    gameStore.updateResourceVisibility(resource.id, newVisibility)
  } catch {
    toast.error('操作失败')
  }
}

async function clearLogs() {
  try {
    await diceService.clearRoomLogs(route.params.id)
    gameStore.setGameLogs([])
    toast.success('日志已清空')
  } catch (error) {
    toast.error(error.message || '清空失败')
  }
}

async function addCustomLog(text) {
  try {
    const log = await diceService.addCustomLog(route.params.id, text)
    gameStore.addGameLog(log)
  } catch (error) {
    toast.error(error.message || '发送失败')
  }
}

async function doRoll(diceStr, reason = null) {
  try {
    const result = await diceService.rollDice(route.params.id, {
      dice: diceStr, reason: reason || null, character_name: selectedCharacterName.value || null
    })
    gameStore.setDiceResult(result)
    const logs = await diceService.getRoomLogs(route.params.id)
    gameStore.setGameLogs(Array.isArray(logs) ? logs : [])
  } catch (error) {
    toast.error(error.message || '掷骰失败')
  }
}

function rollQuickDice() {
  if (!selectedQuickDice.value) return
  doRoll(`1d${selectedQuickDice.value}`, diceReason.value || null)
}

function rollExprDice() {
  const expr = diceExpr.value.trim().toLowerCase()
  if (!expr) return
  if (!/\d*d\d+/.test(expr)) {
    toast.error('表达式格式错误，请使用 xdy+z 格式（如 2d6+3）')
    return
  }
  doRoll(expr, diceReason.value || null)
}

function openCharacterForm() {
  editingCharacter.value = null
  Object.assign(characterForm, { name: '', avatar: '', profession: '', hp: 10, max_hp: 10, san: 50, mp: 0, max_mp: 0, notes: '', is_npc: false })
  Object.assign(characterFormAttrs, { strength: 50, constitution: 50, dexterity: 50, intelligence: 50, willpower: 50, charisma: 50 })
  showCharacterForm.value = true
}

function editCharacter(character) {
  editingCharacter.value = character
  Object.assign(characterForm, {
    name: character.name,
    avatar: character.avatar || '',
    profession: character.profession || '',
    hp: character.hp,
    max_hp: character.max_hp,
    san: character.san ?? 50,
    mp: character.mp ?? 0,
    max_mp: character.max_mp ?? 0,
    notes: character.notes || '',
    is_npc: character.is_npc || false
  })
  try {
    const attrs = JSON.parse(character.attributes || '{}')
    Object.assign(characterFormAttrs, {
      strength: attrs.strength ?? 50, constitution: attrs.constitution ?? 50,
      dexterity: attrs.dexterity ?? 50, intelligence: attrs.intelligence ?? 50,
      willpower: attrs.willpower ?? 50, charisma: attrs.charisma ?? 50
    })
  } catch { Object.assign(characterFormAttrs, { strength: 50, constitution: 50, dexterity: 50, intelligence: 50, willpower: 50, charisma: 50 }) }
  showCharacterForm.value = true
}

async function saveCharacter() {
  try {
    const payload = {
      ...characterForm,
      attributes: JSON.stringify({ ...characterFormAttrs })
    }
    delete payload.is_npc // can't change npc status after creation for edits
    if (editingCharacter.value) {
      await characterService.updateCharacter(editingCharacter.value.id, payload)
    } else {
      payload.is_npc = characterForm.is_npc
      await characterService.createCharacter(route.params.id, payload)
    }
    await refreshCharacters()
    showCharacterForm.value = false
    closeCharacterForm()
    toast.success('保存成功')
  } catch (error) {
    toast.error(error.message || '保存失败')
  }
}

async function deleteCharacter(char) {
  if (!confirm(`确定删除角色"${char.name}"？`)) return
  try {
    await characterService.deleteCharacter(char.id)
    await refreshCharacters()
    toast.success('角色已删除')
  } catch (error) {
    toast.error(error.message || '删除失败')
  }
}

async function refreshCharacters() {
  const characters = await characterService.getRoomCharacters(route.params.id)
  gameStore.setCharacters(Array.isArray(characters) ? characters : [])
  // Refresh logs to pick up character creation/deletion entries
  const logs = await diceService.getRoomLogs(route.params.id)
  gameStore.setGameLogs(Array.isArray(logs) ? logs : [])
}

async function onCharacterUpdate(charId, data) {
  try {
    await characterService.updateCharacter(charId, data)
    await refreshCharacters()
    // Sync map token HP if character is linked to a token
    if (data.hp !== undefined || data.max_hp !== undefined) {
      const linkedUnit = gameStore.mapUnits.find(u => u.character_id === charId)
      if (linkedUnit) {
        const updates = {}
        if (data.hp !== undefined) updates.hp = data.hp
        if (data.max_hp !== undefined) updates.max_hp = data.max_hp
        await mapService.updateUnit(route.params.id, linkedUnit.id, updates)
        gameStore.updateMapUnit(linkedUnit.id, updates)
        if (ws?.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({ type: 'unit_updated', unit_id: linkedUnit.id, updates }))
        }
      }
    }
  } catch (error) {
    toast.error(error.message || '更新失败')
  }
}

async function placeCharOnMap(char) {
  const alreadyPlaced = gameStore.mapUnits.some(u => u.character_id === char.id)
  if (alreadyPlaced) {
    toast.info(`${char.name} 已在地图上`)
    return
  }
  const viewport = mapCanvasRef.value?.viewport || { x: 0, y: 0 }
  try {
    const unit = await mapService.createUnit(route.params.id, {
      name: char.name,
      character_id: char.id,
      x: viewport.x,
      y: viewport.y,
      width: 1,
      height: 1,
      hp: char.hp,
      max_hp: char.max_hp,
      is_enemy: char.is_npc,
      icon: char.avatar || null
    })
    gameStore.addMapUnit(unit)
    if (ws?.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'unit_created', unit }))
    }
    toast.success(`${char.name} 已放置到地图`)
  } catch (error) {
    toast.error(error.message || '放置失败')
  }
}

async function addCharFromTemplate(tpl) {
  try {
    await characterService.createCharacter(route.params.id, {
      name: tpl.name,
      avatar: tpl.avatar || '',
      profession: tpl.profession || '',
      hp: tpl.hp,
      max_hp: tpl.max_hp,
      san: tpl.san ?? 50,
      mp: tpl.mp ?? 0,
      max_mp: tpl.max_mp ?? 0,
      attributes: tpl.attributes || '{}',
      skills: tpl.skills || '[]',
      items: tpl.items || '[]',
      spells: tpl.spells || '[]',
      notes: tpl.notes || '',
      is_npc: true
    })
    await refreshCharacters()
    toast.success(`${tpl.name} 已加入`)
  } catch (error) {
    toast.error(error.message || '添加失败')
  }
}

async function addCharCustom() {
  if (!quickCharName.value.trim()) return
  try {
    await characterService.createCharacter(route.params.id, {
      name: quickCharName.value.trim(),
      avatar: quickCharAvatar.value || null,
      profession: quickCharProfession.value.trim() || null,
      hp: quickCharHp.value || 10,
      max_hp: quickCharMaxHp.value || 10,
      san: quickCharSan.value ?? 50,
      mp: quickCharMp.value ?? 0,
      max_mp: quickCharMaxMp.value ?? 0,
      attributes: JSON.stringify({ ...quickCharAttrs }),
      skills: '[]',
      items: '[]',
      spells: '[]',
      notes: '',
      is_npc: quickCharIsEnemy.value
    })
    await refreshCharacters()
    quickCharName.value = ''
    quickCharAvatar.value = ''
    quickCharProfession.value = ''
    quickCharHp.value = 10
    quickCharMaxHp.value = 10
    quickCharSan.value = 50
    quickCharMp.value = 0
    quickCharMaxMp.value = 0
    Object.assign(quickCharAttrs, { strength: 50, constitution: 50, dexterity: 50, intelligence: 50, willpower: 50, charisma: 50 })
    quickCharIsEnemy.value = false
    toast.success('角色已添加')
  } catch (error) {
    toast.error(error.message || '添加失败')
  }
}

function closeCharacterForm() {
  showCharacterForm.value = false
  editingCharacter.value = null
  Object.assign(characterForm, { name: '', avatar: '', profession: '', hp: 10, max_hp: 10, san: 50, mp: 0, max_mp: 0, notes: '', is_npc: false })
  Object.assign(characterFormAttrs, { strength: 50, constitution: 50, dexterity: 50, intelligence: 50, willpower: 50, charisma: 50 })
}

function openTokenForm() {
  Object.assign(tokenForm, { name: '', icon: '', hp: 10, max_hp: 10, is_enemy: false, width: 1, height: 1 })
  showTokenForm.value = true
}

async function saveToken() {
  try {
    const gridSize = gameStore.activeMap?.grid_size || 50
    const unit = await mapService.createUnit(route.params.id, {
      name: tokenForm.name,
      icon: tokenForm.icon || null,
      x: gridSize,
      y: gridSize,
      width: tokenForm.width,
      height: tokenForm.height,
      hp: tokenForm.hp,
      max_hp: tokenForm.max_hp,
      is_enemy: tokenForm.is_enemy
    })
    gameStore.addMapUnit(unit)
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'unit_created', unit }))
    }
    showTokenForm.value = false
    toast.success('Token 已放置')
  } catch (error) {
    toast.error(error.message || '放置失败')
  }
}

async function onUnitMove(unitId, updates) {
  try {
    await mapService.updateUnit(route.params.id, unitId, updates)
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'unit_move', unit_id: unitId, unit_name: gameStore.mapUnits.find(u => u.id === unitId)?.name, ...updates }))
    }
  } catch {}
}

async function onUnitUpdate(unitId, updates) {
  try {
    await mapService.updateUnit(route.params.id, unitId, updates)
    gameStore.updateMapUnit(unitId, updates)
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'unit_updated', unit_id: unitId, updates }))
    }
  } catch {}
}

async function leaveRoom() {
  if (!isGM.value) {
    try {
      await roomService.leaveRoom(route.params.id)
    } catch {}
  }
  if (isGM.value) {
    router.push('/gm/rooms')
  } else {
    router.push('/rooms')
  }
}

function startResizeLeft(e) {
  e.preventDefault()
  isResizingLeft.value = true
  const startX = e.clientX
  const startWidth = leftPanelWidth.value
  function onMove(ev) {
    const delta = ev.clientX - startX
    leftPanelWidth.value = Math.max(180, Math.min(600, startWidth + delta))
  }
  function onUp() {
    isResizingLeft.value = false
    document.removeEventListener('mousemove', onMove)
    document.removeEventListener('mouseup', onUp)
  }
  document.addEventListener('mousemove', onMove)
  document.addEventListener('mouseup', onUp)
}
</script>

<style scoped>
.game-room {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: var(--bg-deep);
}

.game-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 8px 24px;
  background: var(--bg-primary);
  border-bottom: 1px solid var(--border-subtle);
  flex-shrink: 0;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
}

.game-header h2 {
  flex: 1;
  font-family: var(--font-display);
  font-size: 17px;
  color: var(--accent-gold);
  letter-spacing: 0.04em;
}

.mode-toggle {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 14px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-default);
  background: var(--bg-secondary);
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  font-family: var(--font-body);
  color: var(--text-secondary);
  transition: all 0.2s;
}

.mode-toggle:hover {
  border-color: var(--accent-gold);
  color: var(--accent-gold);
}

.mode-toggle.active {
  background: linear-gradient(135deg, var(--accent-gold), var(--accent-ember));
  color: var(--text-inverse);
  border-color: var(--accent-gold-dim);
}

.mode-switch-hint {
  font-size: 11px;
  opacity: 0.6;
}

.online-users {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--text-muted);
}

.online-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-success);
  flex-shrink: 0;
}

.online-name {
  white-space: nowrap;
}

.room-status {
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
}

.status-waiting { background: var(--color-warning-dim); color: var(--color-warning); }
.status-active { background: var(--color-success-dim); color: var(--color-success); }
.status-ended { background: rgba(107, 99, 87, 0.15); color: var(--text-muted); }

/* ====== 叙事模式三栏 ====== */
.narrative-mode {
  display: flex;
  gap: 0;
  padding: 12px;
  flex: 1;
  overflow: hidden;
  min-height: 0;
}

/* ====== 战斗模式 ====== */
.battle-mode {
  display: flex;
  flex: 1;
  overflow: hidden;
  min-height: 0;
}

.sidebar-left, .sidebar-right {
  display: flex;
  transition: width 0.25s ease;
  overflow: hidden;
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-subtle);
}

.sidebar-left { width: 220px; flex-shrink: 0; }
.sidebar-left.collapsed { width: 40px; }
.sidebar-right { width: 280px; flex-shrink: 0; border-right: none; border-left: 1px solid var(--border-subtle); }
.sidebar-right.collapsed { width: 40px; }

.sidebar-toggle {
  width: 32px;
  min-width: 32px;
  height: 100%;
  background: var(--bg-primary);
  border: none;
  cursor: pointer;
  font-size: 14px;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s, color 0.15s;
  flex-shrink: 0;
}

.sidebar-toggle:hover {
  background: var(--bg-card);
  color: var(--accent-gold);
}

.sidebar-content {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
  min-width: 0;
}

.sidebar-card { font-size: 13px; }

.battle-map-area {
  flex: 1;
  min-width: 0;
  position: relative;
}

.no-map-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  background: var(--bg-deep);
}

.gm-map-select {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.map-select-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}

.map-select-btn {
  padding: 8px 20px;
  background: linear-gradient(135deg, var(--accent-gold), var(--accent-ember));
  color: var(--text-inverse);
  border: none;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-family: var(--font-body);
  cursor: pointer;
  transition: box-shadow 0.2s;
}

.map-select-btn:hover {
  box-shadow: 0 0 16px rgba(212, 168, 83, 0.25);
}

.no-map-text {
  color: var(--text-muted);
  font-size: 16px;
}

/* ====== 角色列表 ====== */
.game-left { overflow-y: auto; }

.resize-handle {
  width: 6px;
  cursor: col-resize;
  background: transparent;
  flex-shrink: 0;
  transition: background 0.15s;
  margin: 0 4px;
}
.resize-handle:hover { background: var(--accent-gold-dim, rgba(212, 168, 83, 0.3)); }

.resize-handle-vertical {
  width: 6px;
  cursor: col-resize;
  background: transparent;
  flex-shrink: 0;
  transition: background 0.15s;
}
.resize-handle-vertical:hover { background: var(--accent-gold-dim, rgba(212, 168, 83, 0.3)); }

.character-list { display: flex; flex-direction: column; gap: 8px; }
.character-list.compact { gap: 4px; }

.character-card {
  padding: 10px 12px;
  background: var(--bg-card);
  border-radius: var(--radius-md);
  border: 2px solid transparent;
  transition: border-color 0.2s;
}

.character-card.compact { padding: 6px 8px; }
.character-card.npc-card { border-left: 3px solid var(--color-danger); }

.char-header {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 4px;
}

.char-header .character-name { flex: 1; }

.char-icon { font-size: 14px; flex-shrink: 0; }
.char-actions { display: flex; gap: 2px; }

.char-section-divider {
  padding: 4px 0 2px;
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-top: 1px solid var(--border-subtle);
  margin-top: 4px;
}

.character-name { font-weight: 600; font-size: 14px; color: var(--text-primary); }

/* ====== GM 添加角色 ====== */
.gm-add-character {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--border-subtle);
}

.add-section-title {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}

.add-source-tabs { display: flex; gap: 4px; margin-bottom: 8px; }

.add-tab {
  padding: 4px 12px;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--text-muted);
  font-size: 12px;
  font-family: var(--font-body);
  cursor: pointer;
  transition: all 0.15s;
}
.add-tab:hover { border-color: var(--accent-gold); color: var(--accent-gold); }
.add-tab.active { background: var(--accent-gold); color: var(--text-inverse); border-color: var(--accent-gold); }

.add-template-list { display: flex; flex-direction: column; gap: 4px; }

.add-template-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 10px;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  background: var(--bg-card);
  color: var(--text-secondary);
  font-size: 13px;
  font-family: var(--font-body);
  cursor: pointer;
  transition: all 0.15s;
  text-align: left;
}
.add-template-btn:hover { border-color: var(--accent-gold); background: rgba(212, 168, 83, 0.06); }

.tpl-icon { font-size: 14px; width: 20px; height: 20px; display: flex; align-items: center; justify-content: center; border-radius: 50%; overflow: hidden; flex-shrink: 0; }
.tpl-avatar-img { width: 100%; height: 100%; object-fit: cover; }
.tpl-name { flex: 1; font-weight: 500; color: var(--text-primary); }
.tpl-prof { font-size: 11px; color: var(--text-muted); background: var(--bg-secondary); padding: 0 4px; border-radius: 3px; }
.tpl-stats { font-size: 11px; color: var(--text-muted); }

.add-empty { font-size: 12px; color: var(--text-muted); text-align: center; padding: 8px; }

.add-custom-form { display: flex; flex-direction: column; gap: 8px; }

.add-custom-stats { display: flex; flex-direction: column; gap: 6px; }

.add-stats-row { display: flex; align-items: center; gap: 4px; }

.add-stats-label { font-size: 12px; color: var(--text-muted); min-width: 28px; text-align: right; }

.add-attrs-details { border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 4px 8px; }

.add-attrs-summary { font-size: 12px; color: var(--text-muted); cursor: pointer; padding: 2px 0; }

.add-attrs-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 4px 12px; margin-top: 6px; }

.add-attrs-row { display: flex; align-items: center; gap: 4px; }

.add-stats-sep { font-size: 14px; color: var(--text-muted); flex-shrink: 0; }

.add-stat { width: 70px; text-align: center; }

.add-input {
  padding: 6px 10px;
  font-size: 13px;
  font-family: var(--font-body);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  background: var(--bg-input);
  color: var(--text-primary);
  outline: none;
}
.add-input:focus { border-color: var(--border-focus); }
.add-input::placeholder { color: var(--text-muted); }

.add-custom-row { display: flex; align-items: center; }

.add-checkbox {
  display: flex; align-items: center; gap: 6px;
  font-size: 13px; color: var(--text-secondary); cursor: pointer;
}
.add-checkbox input { accent-color: var(--accent-gold); }

.hp-row { display: flex; align-items: center; gap: 8px; }
.hp-text { font-size: 12px; color: var(--text-muted); white-space: nowrap; min-width: 56px; }

.hp-bar { flex: 1; height: 6px; background: rgba(255,255,255,0.06); border-radius: 3px; overflow: hidden; }
.hp-fill { height: 100%; border-radius: 3px; transition: width 0.3s ease; }
.hp-green { background: var(--color-success); }
.hp-yellow { background: var(--color-warning); }
.hp-red { background: var(--color-danger); }

.stat-line { margin-top: 4px; font-size: 12px; color: var(--text-muted); }

/* ====== 资源 ====== */
.game-center { overflow-y: auto; min-width: 0; flex: 1; }
.resource-card-wrap { height: 100%; display: flex; flex-direction: column; }
.resource-card-wrap :deep(.card-body) { flex: 1; overflow-y: auto; }

.resource-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; }

.resource-card {
  padding: 16px;
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  transition: opacity 0.2s;
}

.resource-card.is-hidden { opacity: 0.5; }
.image-resource img { width: 100%; border-radius: 6px; display: block; }

.resource-display-type {
  display: inline-block;
  padding: 2px 8px;
  background: var(--color-info-dim);
  color: var(--color-info);
  border-radius: 4px;
  font-size: 11px;
  font-weight: 500;
  margin-bottom: 8px;
}

.text-resource h4 { font-size: 15px; margin-bottom: 6px; color: var(--text-primary); font-family: var(--font-display); }
.text-resource p { font-size: 13px; color: var(--text-secondary); line-height: 1.5; white-space: pre-wrap; }

/* ====== 右侧：掷骰+日志 ====== */
.game-right { display: flex; flex-direction: column; gap: 16px; min-height: 0; width: 300px; flex-shrink: 0; }

/* ====== Token 表单 ====== */
.token-form-row { margin: 8px 0; }
.token-form-row label { display: flex; align-items: center; gap: 6px; font-size: 13px; cursor: pointer; color: var(--text-secondary); }
.token-form-row input { accent-color: var(--accent-gold); }

/* ====== 角色表单弹窗 ====== */
.stats-input { display: flex; align-items: flex-end; gap: 8px; }
.stats-divider { font-size: 18px; color: var(--text-muted); padding-bottom: 8px; }

.empty-state { text-align: center; padding: 24px; color: var(--text-muted); font-size: 13px; }

/* ====== Avatar ====== */
.form-row-label { font-size: 13px; color: var(--text-muted); margin-bottom: 4px; }
.quick-avatar-row { display: flex; align-items: center; gap: 6px; margin-bottom: 4px; }
.quick-avatar-label { font-size: 12px; color: var(--text-muted); }
</style>
