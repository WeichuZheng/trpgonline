<template>
  <div class="room-manage-page">
    <div class="page-header">
      <AppButton variant="ghost" @click="goBack">&larr; 返回</AppButton>
      <h2>房间管理</h2>
      <AppButton @click="openCreateDialog" v-if="modulesStore.modules.length > 0">+ 新建房间</AppButton>
    </div>

    <div class="room-cards">
      <div v-for="room in roomsStore.gmRooms" :key="room.id" class="room-card-item" :class="'status-' + room.status">
        <div class="room-card-header">
          <h3>{{ room.name }}</h3>
          <span class="room-status-badge" :class="'badge-' + room.status">{{ getStatusLabel(room.status) }}</span>
        </div>
        <div class="room-card-body">
          <div class="room-info"><span class="info-label">模组:</span><span class="info-value">{{ room.module_title || '未命名模组' }}</span></div>
          <div class="room-info"><span class="info-label">人数:</span><span class="info-value">{{ room.current_players || 0 }}/{{ room.max_players || 8 }}</span></div>
        </div>
        <div class="room-card-footer">
          <AppButton size="small" variant="primary" @click="enterRoom(room)">进入房间</AppButton>
          <AppButton size="small" variant="secondary" @click="editRoomName(room)">编辑</AppButton>
          <AppButton size="small" v-if="room.status === 'waiting'" @click="startGame(room)">开始游戏</AppButton>
          <AppButton size="small" variant="danger" v-if="room.status === 'active'" @click="endGame(room)">结束游戏</AppButton>
          <AppButton size="small" variant="ghost" @click="confirmDeleteRoom(room)">删除</AppButton>
        </div>
      </div>
      <div v-if="roomsStore.gmRooms.length === 0" class="empty-state">
        <div class="empty-icon">⚔</div>
        <p>暂无房间</p>
        <p class="empty-hint">点击"新建房间"按钮创建房间</p>
      </div>
    </div>

    <AppModal v-model="showCreateDialog" title="创建房间">
      <form @submit.prevent="handleCreateRoom">
        <AppSelect v-model="newRoom.module_id" :options="moduleOptions" label="选择模组" placeholder="请选择模组" required></AppSelect>
        <AppInput v-model="newRoom.name" label="房间名称" placeholder="请输入房间名称" required></AppInput>
      </form>
      <template #footer>
        <AppButton variant="secondary" @click="showCreateDialog = false">取消</AppButton>
        <AppButton @click="handleCreateRoom" :loading="roomsStore.loading" :disabled="!newRoom.module_id || !newRoom.name">创建</AppButton>
      </template>
    </AppModal>

    <AppModal v-model="showEditDialog" title="编辑房间">
      <form @submit.prevent="handleUpdateRoom">
        <AppInput v-model="editRoomData.name" label="房间名称" placeholder="请输入房间名称" required></AppInput>
      </form>
      <template #footer>
        <AppButton variant="secondary" @click="showEditDialog = false">取消</AppButton>
        <AppButton @click="handleUpdateRoom" :loading="roomsStore.loading">保存</AppButton>
      </template>
    </AppModal>

    <AppModal v-model="showDeleteDialog" title="确认删除" size="small">
      <p>确定要删除房间"{{ deletingRoom?.name }}"吗？此操作不可撤销。</p>
      <template #footer>
        <AppButton variant="secondary" @click="showDeleteDialog = false">取消</AppButton>
        <AppButton variant="danger" @click="handleDeleteRoom" :loading="roomsStore.loading">删除</AppButton>
      </template>
    </AppModal>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, inject } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useRoomsStore } from '@/stores/rooms'
import { useModulesStore } from '@/stores/modules'
import AppButton from '@/components/common/AppButton.vue'
import AppModal from '@/components/common/AppModal.vue'
import AppInput from '@/components/common/AppInput.vue'
import AppSelect from '@/components/common/AppSelect.vue'

const router = useRouter()
const route = useRoute()
const roomsStore = useRoomsStore()
const modulesStore = useModulesStore()
const toast = inject('toast')

const showCreateDialog = ref(false)
const showEditDialog = ref(false)
const showDeleteDialog = ref(false)
const editingRoom = ref(null)
const deletingRoom = ref(null)
const newRoom = reactive({ module_id: '', name: '' })
const editRoomData = reactive({ name: '' })
const moduleOptions = computed(() => modulesStore.modules.map(m => ({ value: m.id, label: m.title })))

onMounted(async () => {
  try {
    await modulesStore.fetchMyModules()
    await roomsStore.fetchGmRooms()
    const moduleId = route.query.module
    if (moduleId) { newRoom.module_id = Number(moduleId); showCreateDialog.value = true }
  } catch { toast.error('加载失败') }
})

function goBack() { router.push('/dashboard') }
function openCreateDialog() { newRoom.module_id = ''; newRoom.name = ''; showCreateDialog.value = true }
function getStatusLabel(status) { return { waiting: '等待中', active: '进行中', ended: '已结束' }[status] || status }
function enterRoom(room) { router.push(`/rooms/${room.id}/game`) }

async function handleCreateRoom() {
  if (!newRoom.module_id || !newRoom.name) return
  try { await roomsStore.createRoom(newRoom.module_id, { name: newRoom.name }); toast.success('房间创建成功'); showCreateDialog.value = false; newRoom.module_id = ''; newRoom.name = '' }
  catch (error) { toast.error(error.message || '创建失败') }
}

function editRoomName(room) { editingRoom.value = room; editRoomData.name = room.name; showEditDialog.value = true }

async function handleUpdateRoom() {
  try { await roomsStore.updateRoom(editingRoom.value.id, { name: editRoomData.name }); toast.success('更新成功'); showEditDialog.value = false; await roomsStore.fetchGmRooms() }
  catch (error) { toast.error(error.message || '更新失败') }
}

function confirmDeleteRoom(room) { deletingRoom.value = room; showDeleteDialog.value = true }

async function handleDeleteRoom() {
  try { await roomsStore.deleteRoom(deletingRoom.value.id); toast.success('删除成功'); showDeleteDialog.value = false }
  catch (error) { toast.error(error.message || '删除失败') }
}

async function startGame(room) {
  try { await roomsStore.startGame(room.id); toast.success('游戏开始'); await roomsStore.fetchGmRooms() }
  catch (error) { toast.error(error.message || '操作失败') }
}

async function endGame(room) {
  try { await roomsStore.endGame(room.id); toast.success('游戏已结束'); await roomsStore.fetchGmRooms() }
  catch (error) { toast.error(error.message || '操作失败') }
}
</script>

<style scoped>
.room-manage-page { padding: 32px; max-width: 1200px; margin: 0 auto; }

.page-header { display: flex; align-items: center; gap: 16px; margin-bottom: 24px; }
.page-header h2 { flex: 1; font-family: var(--font-display); font-size: 22px; color: var(--accent-gold); letter-spacing: 0.04em; }

.room-cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; }

.room-card-item { background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); overflow: hidden; }

.room-card-header { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; border-bottom: 1px solid var(--border-subtle); background: rgba(0,0,0,0.1); }
.room-card-header h3 { font-family: var(--font-display); font-size: 17px; color: var(--text-primary); }

.room-status-badge { padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }
.badge-waiting { background: var(--color-warning-dim); color: var(--color-warning); }
.badge-active { background: var(--color-success-dim); color: var(--color-success); }
.badge-ended { background: rgba(107,99,87,0.15); color: var(--text-muted); }

.room-card-body { padding: 16px 20px; }
.room-info { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 13px; }
.info-label { color: var(--text-muted); }
.info-value { color: var(--text-secondary); font-weight: 500; }

.room-card-footer { padding: 14px 20px; border-top: 1px solid var(--border-subtle); background: rgba(0,0,0,0.08); display: flex; gap: 8px; flex-wrap: wrap; }

.empty-state { grid-column: 1 / -1; text-align: center; padding: 80px 20px; color: var(--text-muted); }
.empty-icon { font-size: 40px; margin-bottom: 12px; opacity: 0.5; }
.empty-state p { font-size: 15px; }
.empty-hint { font-size: 13px; margin-top: 6px; opacity: 0.7; }

p { color: var(--text-secondary); }
</style>
