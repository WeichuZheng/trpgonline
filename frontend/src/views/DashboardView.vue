<template>
  <div class="dashboard">
    <div class="page-header">
      <h2>我的模组</h2>
      <div class="page-header-actions">
        <router-link to="/admin" v-if="authStore.isAdmin" class="admin-link">管理面板</router-link>
        <AppButton @click="showCreateModal = true" v-if="authStore.isGM">+ 创建新模组</AppButton>
      </div>
    </div>

    <div class="module-list">
      <AppCard
        v-for="mod in modulesStore.modules"
        :key="mod.id"
        hoverable
        @click="openModule(mod)"
      >
        <h3 class="module-title">{{ mod.title }}</h3>
        <p class="module-description">{{ mod.description || '暂无描述' }}</p>
        <template #footer>
          <div class="module-actions">
            <AppButton size="small" @click.stop="openModule(mod)">管理资源</AppButton>
            <AppButton size="small" variant="primary" @click.stop="createRoom(mod)" v-if="authStore.isGM">创建房间</AppButton>
          </div>
        </template>
      </AppCard>

      <div v-if="modulesStore.modules.length === 0" class="empty-state">
        <div class="empty-icon">📜</div>
        <p>暂无模组</p>
        <p class="empty-hint" v-if="authStore.isGM">点击上方按钮创建</p>
        <p class="empty-hint" v-else>请联系 GM 创建模组</p>
      </div>
    </div>

    <AppModal v-model="showCreateModal" title="创建模组">
      <form @submit.prevent="handleCreateModule">
        <AppInput v-model="newModule.title" label="模组名称" placeholder="请输入模组名称" :error="errors.title" required></AppInput>
        <AppInput v-model="newModule.description" label="描述" placeholder="请输入模组描述"></AppInput>
      </form>
      <template #footer>
        <AppButton variant="secondary" @click="showCreateModal = false">取消</AppButton>
        <AppButton @click="handleCreateModule" :loading="modulesStore.loading">创建</AppButton>
      </template>
    </AppModal>

    <AppModal v-model="showRoomModal" title="创建房间">
      <form @submit.prevent="handleCreateRoom">
        <AppInput v-model="newRoomName" label="房间名称" placeholder="请输入房间名称" required></AppInput>
      </form>
      <template #footer>
        <AppButton variant="secondary" @click="showRoomModal = false">取消</AppButton>
        <AppButton @click="handleCreateRoom" :loading="creatingRoom">创建</AppButton>
      </template>
    </AppModal>
  </div>
</template>

<script setup>
import { ref, reactive, inject, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useModulesStore } from '@/stores/modules'
import { useRoomsStore } from '@/stores/rooms'
import AppButton from '@/components/common/AppButton.vue'
import AppCard from '@/components/common/AppCard.vue'
import AppModal from '@/components/common/AppModal.vue'
import AppInput from '@/components/common/AppInput.vue'

const router = useRouter()
const authStore = useAuthStore()
const modulesStore = useModulesStore()
const roomsStore = useRoomsStore()
const toast = inject('toast')

const showCreateModal = ref(false)
const showRoomModal = ref(false)
const creatingRoom = ref(false)
const selectedModuleId = ref(null)
const newRoomName = ref('')
const newModule = reactive({ title: '', description: '' })
const errors = reactive({ title: '' })

onMounted(async () => {
  try { await modulesStore.fetchMyModules() } catch { toast.error('加载模组失败') }
})

function openModule(mod) {
  modulesStore.setCurrentModule(mod)
  router.push(`/modules/${mod.id}/edit`)
}

function createRoom(mod) {
  selectedModuleId.value = mod.id
  newRoomName.value = ''
  showRoomModal.value = true
}

async function handleCreateModule() {
  if (!newModule.title.trim()) { errors.title = '请输入模组名称'; return }
  try {
    await modulesStore.createModule({ title: newModule.title, description: newModule.description })
    toast.success('模组创建成功')
    showCreateModal.value = false
    newModule.title = ''
    newModule.description = ''
  } catch (error) { toast.error(error.message || '创建失败') }
}

async function handleCreateRoom() {
  if (!newRoomName.value.trim()) return
  creatingRoom.value = true
  try {
    const room = await roomsStore.createRoom(selectedModuleId.value, { name: newRoomName.value })
    toast.success('房间创建成功')
    showRoomModal.value = false
    router.push(`/rooms/${room.id}/game`)
  } catch (error) { toast.error(error.message || '创建失败') } finally { creatingRoom.value = false }
}
</script>

<style scoped>
.dashboard {
  padding: 32px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 28px;
}

.page-header h2 {
  font-family: var(--font-display);
  font-size: 22px;
  color: var(--accent-gold);
  letter-spacing: 0.04em;
}

.page-header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.admin-link {
  color: var(--accent-gold);
  font-size: 13px;
  text-decoration: none;
  transition: color 0.2s;
}

.admin-link:hover {
  color: var(--accent-gold-bright);
}

.module-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.module-title {
  font-family: var(--font-display);
  font-size: 17px;
  color: var(--text-primary);
  margin-bottom: 8px;
  letter-spacing: 0.02em;
}

.module-description {
  color: var(--text-muted);
  font-size: 14px;
  line-height: 1.5;
}

.module-actions {
  display: flex;
  gap: 8px;
}

.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 80px 20px;
  color: var(--text-muted);
}

.empty-icon {
  font-size: 40px;
  margin-bottom: 12px;
  opacity: 0.5;
}

.empty-state p {
  font-size: 15px;
}

.empty-hint {
  font-size: 13px;
  margin-top: 6px;
  opacity: 0.7;
}
</style>
