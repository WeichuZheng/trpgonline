<template>
  <AppCard title="游戏日志" class="log-card" :class="{ compact }">
    <template #header-extra>
      <div class="log-actions">
        <button v-if="isGm" class="log-action-btn danger" @click="confirmClear" title="清空日志">
          <span class="btn-icon">&#x2715;</span>
        </button>
      </div>
    </template>
    <div class="log-search-row">
      <input v-model="searchQuery" class="log-search-input" placeholder="搜索日志..." />
    </div>
    <div class="log-messages" ref="logContainer">
      <div v-for="log in filteredLogs" :key="log.id" class="log-entry" :class="log.action">
        <span class="log-time">{{ formatTime(log.created_at) }}</span>
        <span class="log-content">{{ formatLogDetail(log) }}</span>
      </div>
      <div v-if="filteredLogs.length === 0 && logs.length > 0" class="empty-state">没有匹配的日志</div>
      <div v-else-if="logs.length === 0" class="empty-state">暂无游戏记录</div>
    </div>
    <div class="log-input-row">
      <input
        v-model="customLogText"
        class="log-input"
        placeholder="输入日志..."
        @keyup.enter="submitCustomLog"
      />
      <button class="log-send-btn" @click="submitCustomLog" :disabled="!customLogText.trim()">
        &#x279C;
      </button>
    </div>
  </AppCard>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  logs: { type: Array, default: () => [] },
  compact: { type: Boolean, default: false },
  isGm: { type: Boolean, default: false }
})

const searchQuery = ref('')

const filteredLogs = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return props.logs
  return props.logs.filter(log => {
    const detail = log.detail || ''
    return detail.toLowerCase().includes(q)
  })
})

const emit = defineEmits(['clear-logs', 'add-log'])

const customLogText = ref('')
const logContainer = ref(null)

function formatLogDetail(log) {
  if (!log.detail) return ''
  try {
    const parsed = JSON.parse(log.detail)
    if (log.action === 'dice' && parsed.details) {
      let text = `🎲 ${parsed.details}`
      if (parsed.reason) text += ` (${parsed.reason})`
      return text
    }
    if (log.action === 'attack' && parsed.character_name) {
      return `⚔️ ${parsed.character_name} 攻击 ${parsed.target} | 命中: ${parsed.attack_roll} 伤害: ${parsed.damage_roll}`
    }
    return parsed.details || parsed.message || log.detail
  } catch {
    return log.detail
  }
}

function formatTime(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

function confirmClear() {
  if (confirm('确定清空所有日志？此操作不可撤销。')) {
    emit('clear-logs')
  }
}

function submitCustomLog() {
  const text = customLogText.value.trim()
  if (!text) return
  emit('add-log', text)
  customLogText.value = ''
}
</script>

<style scoped>
.log-card { flex: 1; min-height: 0; display: flex; flex-direction: column; }
.log-card :deep(.card-body) { flex: 1; overflow: hidden; display: flex; flex-direction: column; }

.log-actions { display: flex; gap: 4px; }

.log-action-btn {
  width: 24px; height: 24px;
  border: none; border-radius: 4px;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  font-size: 12px;
  background: transparent;
  color: var(--text-muted);
  transition: all 0.15s;
}
.log-action-btn:hover { background: rgba(244,67,54,0.15); color: var(--color-danger); }
.log-action-btn .btn-icon { font-size: 11px; }

.log-search-row { padding: 0 0 6px; flex-shrink: 0; }

.log-search-input {
  width: 100%;
  padding: 4px 8px;
  font-size: 12px;
  font-family: var(--font-body);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  background: var(--bg-input);
  color: var(--text-primary);
  outline: none;
}
.log-search-input:focus { border-color: var(--border-focus); }
.log-search-input::placeholder { color: var(--text-muted); }

.log-messages { flex: 1; overflow-y: auto; min-height: 0; }

.log-entry {
  padding: 5px 0;
  border-bottom: 1px solid var(--border-subtle);
  font-size: 13px;
  line-height: 1.4;
}

.log-time { color: var(--text-muted); margin-right: 6px; font-size: 11px; }
.log-content { color: var(--text-secondary); }

.log-input-row {
  display: flex;
  gap: 6px;
  padding-top: 8px;
  border-top: 1px solid var(--border-subtle);
  margin-top: 4px;
  flex-shrink: 0;
}

.log-input {
  flex: 1;
  padding: 5px 10px;
  font-size: 13px;
  font-family: var(--font-body);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  background: var(--bg-input);
  color: var(--text-primary);
  outline: none;
  transition: border-color 0.2s;
}
.log-input:focus { border-color: var(--border-focus); }
.log-input::placeholder { color: var(--text-muted); }

.log-send-btn {
  width: 32px; height: 32px;
  border: none;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--accent-gold), var(--accent-ember));
  color: var(--text-inverse);
  cursor: pointer;
  font-size: 14px;
  display: flex; align-items: center; justify-content: center;
  transition: opacity 0.15s;
  flex-shrink: 0;
}
.log-send-btn:disabled { opacity: 0.4; cursor: default; }
.log-send-btn:not(:disabled):hover { opacity: 0.9; }

.empty-state { text-align: center; padding: 24px; color: var(--text-muted); font-size: 13px; }
</style>
