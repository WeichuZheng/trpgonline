<template>
  <div class="admin-view">
    <div class="page-header">
      <h2>管理面板</h2>
      <router-link to="/dashboard" class="back-link">返回仪表盘</router-link>
    </div>

    <div v-if="loading" class="loading">加载中...</div>

    <div v-else class="admin-content">
      <div class="section">
        <h3>用户管理</h3>
        <table class="user-table">
          <thead>
            <tr>
              <th>用户名</th>
              <th>注册时间</th>
              <th>申请 GM</th>
              <th>GM 权限</th>
              <th>管理员</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in users" :key="u.id" :class="{ 'is-self': u.id === currentUserId }">
              <td>{{ u.username }}</td>
              <td>{{ formatDate(u.created_at) }}</td>
              <td>
                <span v-if="u.requested_gm" class="badge badge-request">已申请</span>
                <span v-else class="badge badge-none">-</span>
              </td>
              <td>
                <span :class="['badge', u.can_create_module ? 'badge-active' : 'badge-inactive']">
                  {{ u.can_create_module ? '是' : '否' }}
                </span>
              </td>
              <td>
                <span :class="['badge', u.is_admin ? 'badge-active' : 'badge-inactive']">
                  {{ u.is_admin ? '是' : '否' }}
                </span>
              </td>
              <td class="actions-cell">
                <button
                  class="action-btn"
                  @click="toggleGM(u)"
                  :disabled="u.id === currentUserId && !u.can_create_module"
                >
                  {{ u.can_create_module ? '取消 GM' : '设为 GM' }}
                </button>
                <button
                  v-if="!u.is_admin"
                  class="action-btn action-admin"
                  @click="promoteAdmin(u)"
                >
                  设为管理员
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="section">
        <h3>日志清理</h3>
        <div class="cleanup-row">
          <span>删除 {{ cleanupDays }} 天前的游戏日志</span>
          <button class="action-btn action-cleanup" @click="handleCleanup" :disabled="cleaningUp">
            {{ cleaningUp ? '清理中...' : '执行清理' }}
          </button>
        </div>
        <p v-if="cleanupResult" class="cleanup-result">{{ cleanupResult }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { adminService } from '@/services/adminService'

const authStore = useAuthStore()
const toast = inject('toast')

const users = ref([])
const loading = ref(true)
const cleaningUp = ref(false)
const cleanupDays = ref(30)
const cleanupResult = ref('')

const currentUserId = authStore.user?.id

function formatDate(d) {
  if (!d) return '-'
  return new Date(d).toLocaleDateString('zh-CN')
}

async function loadUsers() {
  loading.value = true
  try {
    users.value = await adminService.getUsers()
  } catch (e) {
    toast.error('加载用户列表失败')
  } finally {
    loading.value = false
  }
}

async function toggleGM(u) {
  try {
    const updated = await adminService.updateUser(u.id, { can_create_module: !u.can_create_module })
    Object.assign(u, updated)
    toast.success(`${u.username}: GM 权限已${u.can_create_module ? '启用' : '禁用'}`)
  } catch (e) {
    toast.error('操作失败: ' + (e.message || '未知错误'))
  }
}

async function promoteAdmin(u) {
  if (!confirm(`确认将 ${u.username} 设为管理员？`)) return
  try {
    const updated = await adminService.updateUser(u.id, { is_admin: true })
    Object.assign(u, updated)
    toast.success(`${u.username} 已设为管理员`)
  } catch (e) {
    toast.error('操作失败: ' + (e.message || '未知错误'))
  }
}

async function handleCleanup() {
  if (!confirm(`确认删除 ${cleanupDays.value} 天前的所有游戏日志？此操作不可撤销。`)) return
  cleaningUp.value = true
  cleanupResult.value = ''
  try {
    const result = await adminService.cleanupLogs(cleanupDays.value)
    cleanupResult.value = result.message
    toast.success(result.message)
  } catch (e) {
    cleanupResult.value = '清理失败: ' + (e.message || '未知错误')
  } finally {
    cleaningUp.value = false
  }
}

onMounted(loadUsers)
</script>

<style scoped>
.admin-view {
  padding: 32px;
  max-width: 1100px;
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

.back-link {
  color: var(--text-muted);
  font-size: 13px;
  text-decoration: none;
}
.back-link:hover { color: var(--accent-gold); }

.section {
  background: var(--bg-card);
  border: 1px solid var(--border-default);
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 20px;
}

.section h3 {
  font-family: var(--font-display);
  font-size: 16px;
  color: var(--text-primary);
  margin-bottom: 16px;
}

.user-table {
  width: 100%;
  border-collapse: collapse;
}

.user-table th,
.user-table td {
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid var(--border-default);
  font-size: 13px;
  color: var(--text-primary);
}

.user-table th {
  color: var(--text-muted);
  font-weight: 600;
  font-size: 12px;
  text-transform: uppercase;
}

.user-table tr.is-self {
  background: rgba(var(--accent-rgb), 0.04);
}

.badge {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.badge-active { background: rgba(76, 175, 80, 0.15); color: #4caf50; }
.badge-inactive { background: rgba(255, 255, 255, 0.05); color: var(--text-muted); }
.badge-request { background: rgba(255, 193, 7, 0.15); color: #ffc107; }
.badge-none { color: var(--text-muted); }

.actions-cell {
  display: flex;
  gap: 6px;
}

.action-btn {
  padding: 4px 10px;
  border-radius: 4px;
  border: 1px solid var(--border-default);
  background: var(--bg-deep);
  color: var(--text-primary);
  font-size: 12px;
  cursor: pointer;
  transition: all 0.15s;
}

.action-btn:hover:not(:disabled) {
  border-color: var(--accent-gold);
  color: var(--accent-gold);
}

.action-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.action-admin {
  border-color: rgba(76, 175, 80, 0.3);
  color: #4caf50;
}

.action-admin:hover {
  border-color: #4caf50;
  background: rgba(76, 175, 80, 0.08);
}

.cleanup-row {
  display: flex;
  align-items: center;
  gap: 16px;
  color: var(--text-secondary);
  font-size: 14px;
}

.action-cleanup {
  border-color: rgba(244, 67, 54, 0.3);
  color: #f44336;
}

.action-cleanup:hover:not(:disabled) {
  border-color: #f44336;
  background: rgba(244, 67, 54, 0.08);
}

.cleanup-result {
  margin-top: 8px;
  color: var(--text-muted);
  font-size: 13px;
}

.loading {
  text-align: center;
  padding: 60px;
  color: var(--text-muted);
}
</style>
