<template>
  <div class="room-list-page">
    <div class="page-header">
      <AppButton variant="ghost" @click="goBack">&larr; 返回</AppButton>
      <h2>房间列表</h2>
    </div>

    <div class="filter-section" v-if="allModules.length > 0">
      <AppSelect v-model="filterModuleId" :options="moduleOptions" label="筛选模组" placeholder="全部模组" @update:model-value="loadRooms"></AppSelect>
    </div>

    <div class="room-cards">
      <div v-for="room in roomsStore.rooms" :key="room.id" class="room-card-item" :class="'status-' + room.status" @click="joinRoom(room)">
        <div class="room-card-header">
          <h3>{{ room.name }}</h3>
          <span class="room-status-badge" :class="'badge-' + room.status">{{ getStatusLabel(room.status) }}</span>
        </div>
        <div class="room-card-body">
          <div class="room-info">
            <span class="info-label">模组:</span>
            <span class="info-value">{{ room.module_title || '未命名模组' }}</span>
          </div>
          <div class="room-info">
            <span class="info-label">主持人:</span>
            <span class="info-value">{{ room.gm_username || '未知' }}</span>
          </div>
          <div class="room-info">
            <span class="info-label">人数:</span>
            <span class="info-value" :class="{ full: room.current_players >= room.max_players }">
              {{ room.current_players || 0 }}/{{ room.max_players || 8 }}
              <span v-if="room.current_players >= room.max_players" class="full-label">已满</span>
            </span>
          </div>
        </div>
        <div class="room-card-footer">
          <AppButton :disabled="room.status === 'ended' || room.current_players >= room.max_players" @click.stop="joinRoom(room)">
            {{ room.status === 'ended' ? '已结束' : (room.current_players >= room.max_players ? '已满' : '进入游戏') }}
          </AppButton>
        </div>
      </div>
      <div v-if="roomsStore.rooms.length === 0" class="empty-state">
        <div class="empty-icon">🏰</div>
        <p>暂无房间</p>
        <p class="empty-hint">请等待 GM 创建房间</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject } from 'vue'
import { useRouter } from 'vue-router'
import { useRoomsStore } from '@/stores/rooms'
import { useModulesStore } from '@/stores/modules'
import { roomService } from '@/services/roomService'
import AppButton from '@/components/common/AppButton.vue'
import AppSelect from '@/components/common/AppSelect.vue'

const router = useRouter()
const roomsStore = useRoomsStore()
const modulesStore = useModulesStore()
const toast = inject('toast')

const filterModuleId = ref('')
const allModules = ref([])
const moduleOptions = computed(() => [{ value: '', label: '全部模组' }, ...allModules.value.map(m => ({ value: m.id, label: m.title }))])

onMounted(async () => {
  try { await modulesStore.fetchMyModules(); allModules.value = modulesStore.modules; await loadRooms() } catch { toast.error('加载失败') }
})

async function loadRooms() { try { await roomsStore.fetchAllRooms(filterModuleId.value || null) } catch { toast.error('加载房间失败') } }
function goBack() { router.push('/dashboard') }
function getStatusLabel(status) { return { waiting: '等待中', active: '进行中', ended: '已结束' }[status] || status }

async function joinRoom(room) {
  if (room.status === 'ended' || room.current_players >= room.max_players) return
  try { await roomService.joinRoom(room.id); router.push(`/rooms/${room.id}/game`) }
  catch (error) { if (error.message?.includes('已在房间')) router.push(`/rooms/${room.id}/game`); else toast.error(error.message || '加入失败') }
}
</script>

<style scoped>
.room-list-page {
  padding: 32px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.page-header h2 {
  font-family: var(--font-display);
  font-size: 22px;
  color: var(--accent-gold);
  letter-spacing: 0.04em;
}

.filter-section {
  margin-bottom: 20px;
  max-width: 300px;
}

.room-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.room-card-item {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.room-card-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-glow);
  border-color: var(--border-focus);
}

.room-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-subtle);
  background: rgba(0, 0, 0, 0.1);
}

.room-card-header h3 {
  font-family: var(--font-display);
  font-size: 17px;
  color: var(--text-primary);
}

.room-status-badge {
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.02em;
}

.badge-waiting { background: var(--color-warning-dim); color: var(--color-warning); }
.badge-active { background: var(--color-success-dim); color: var(--color-success); }
.badge-ended { background: rgba(107, 99, 87, 0.15); color: var(--text-muted); }

.room-card-body { padding: 16px 20px; }

.room-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 13px;
}

.info-label { color: var(--text-muted); }
.info-value { color: var(--text-secondary); font-weight: 500; }
.info-value.full { color: var(--color-danger); }
.full-label { color: var(--color-danger); margin-left: 4px; }

.room-card-footer {
  padding: 14px 20px;
  border-top: 1px solid var(--border-subtle);
  background: rgba(0, 0, 0, 0.08);
}

.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 80px 20px;
  color: var(--text-muted);
}

.empty-icon { font-size: 40px; margin-bottom: 12px; opacity: 0.5; }
.empty-state p { font-size: 15px; }
.empty-hint { font-size: 13px; margin-top: 6px; opacity: 0.7; }
</style>
