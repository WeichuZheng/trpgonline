<template>
  <div class="app-layout">
    <nav class="navbar">
      <div class="nav-brand">
        <router-link to="/dashboard">跑团在线</router-link>
      </div>
      <div class="nav-links">
        <router-link to="/dashboard">我的模组</router-link>
        <router-link to="/rooms">房间列表</router-link>
        <router-link to="/gm/rooms" v-if="authStore.isGM">房间管理</router-link>
      </div>
      <div class="nav-theme">
        <select :value="activeTheme" @change="changeTheme($event.target.value)">
          <option value="dark">🌙 墨火羊皮卷</option>
          <option value="light">☀️ 象牙墨色</option>
          <option value="sepia">📜 古卷羊皮</option>
          <option value="forest">🌲 深林暗影</option>
          <option value="ocean">🌊 深海湛蓝</option>
        </select>
      </div>
      <div class="nav-user">
        <span class="username">{{ authStore.username }}</span>
        <AppButton size="small" variant="ghost" @click="logout">退出</AppButton>
      </div>
    </nav>

    <main class="main-content">
      <router-view></router-view>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AppButton from '@/components/common/AppButton.vue'

const router = useRouter()
const authStore = useAuthStore()

const STORAGE_KEY = 'trpg-theme-preference'
const activeTheme = ref('dark')

function applyTheme(theme) {
  activeTheme.value = theme
  document.documentElement.setAttribute('data-theme', theme)
}

function changeTheme(theme) {
  applyTheme(theme)
  localStorage.setItem(STORAGE_KEY, theme)
}

onMounted(() => {
  const stored = localStorage.getItem(STORAGE_KEY)
  if (stored) applyTheme(stored)
})

function logout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  display: flex;
  align-items: center;
  padding: 0 28px;
  height: 56px;
  background: var(--bg-primary);
  border-bottom: 1px solid var(--border-subtle);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
}

.nav-brand {
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 700;
  color: var(--accent-gold);
  letter-spacing: 0.05em;
}

.nav-brand a {
  text-decoration: none;
  color: inherit;
}

.nav-links {
  display: flex;
  gap: 28px;
  margin-left: 48px;
}

.nav-links a {
  text-decoration: none;
  color: var(--text-muted);
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 500;
  padding: 8px 0;
  border-bottom: 2px solid transparent;
  transition: color 0.2s ease, border-color 0.2s ease;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  color: var(--accent-gold);
  border-bottom-color: var(--accent-gold);
}

.nav-theme {
  margin-left: auto;
  margin-right: 16px;
}

.nav-theme select {
  padding: 4px 10px;
  font-size: 13px;
  font-family: var(--font-body);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  background: var(--bg-input);
  color: var(--text-primary);
  cursor: pointer;
  transition: border-color 0.2s;
}

.nav-theme select:hover {
  border-color: var(--border-default);
}

.nav-user {
  display: flex;
  align-items: center;
  gap: 12px;
}

.username {
  font-size: 13px;
  color: var(--text-secondary);
}

.main-content {
  flex: 1;
  background: var(--bg-deep);
}
</style>
