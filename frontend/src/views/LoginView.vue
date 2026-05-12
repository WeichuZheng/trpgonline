<template>
  <div class="auth-container">
    <div class="auth-particles"></div>
    <div class="auth-box">
      <div class="auth-emblem">
        <div class="emblem-ring"></div>
        <span class="emblem-text">T</span>
      </div>
      <h1>进入酒馆</h1>
      <p class="auth-subtitle">输入你的身份，开始冒险</p>
      <form @submit.prevent="handleLogin">
        <AppInput v-model="form.username" label="用户名" placeholder="请输入用户名" :error="errors.username" required></AppInput>
        <AppInput v-model="form.password" type="password" label="密码" placeholder="请输入密码" :error="errors.password" required></AppInput>
        <AppButton type="submit" :loading="loading" block>登录</AppButton>
      </form>
      <p class="auth-switch">
        还没有账号？ <router-link to="/register">注册</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, inject } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AppInput from '@/components/common/AppInput.vue'
import AppButton from '@/components/common/AppButton.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const toast = inject('toast')

const form = reactive({ username: '', password: '' })
const errors = reactive({ username: '', password: '' })
const loading = ref(false)

function validate() {
  let valid = true
  errors.username = ''
  errors.password = ''
  if (!form.username.trim()) { errors.username = '请输入用户名'; valid = false }
  if (!form.password) { errors.password = '请输入密码'; valid = false }
  return valid
}

async function handleLogin() {
  if (!validate()) return
  loading.value = true
  try {
    await authStore.login({ username: form.username, password: form.password })
    toast.success('登录成功')
    router.push(route.query.redirect || '/dashboard')
  } catch (error) {
    toast.error(error.message || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-deep);
  position: relative;
  overflow: hidden;
}

.auth-particles {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 20% 50%, rgba(var(--accent-rgb), 0.06) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 20%, rgba(196, 122, 58, 0.04) 0%, transparent 40%),
    radial-gradient(ellipse at 50% 80%, rgba(var(--accent-rgb), 0.03) 0%, transparent 50%);
}

.auth-box {
  width: 100%;
  max-width: 400px;
  padding: 44px 40px;
  background: var(--bg-card);
  border: 1px solid var(--border-default);
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5), 0 0 60px rgba(var(--accent-rgb), 0.04);
  position: relative;
  z-index: 1;
}

.auth-emblem {
  width: 64px;
  height: 64px;
  margin: 0 auto 20px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.emblem-ring {
  position: absolute;
  inset: 0;
  border: 2px solid var(--accent-gold);
  border-radius: 50%;
  opacity: 0.3;
  animation: pulse-ring 3s ease-in-out infinite;
}

.emblem-text {
  font-family: var(--font-display);
  font-size: 28px;
  font-weight: 700;
  color: var(--accent-gold);
}

@keyframes pulse-ring {
  0%, 100% { transform: scale(1); opacity: 0.3; }
  50% { transform: scale(1.08); opacity: 0.5; }
}

.auth-box h1 {
  text-align: center;
  font-family: var(--font-display);
  margin-bottom: 4px;
  font-size: 22px;
  color: var(--text-primary);
  letter-spacing: 0.06em;
}

.auth-subtitle {
  text-align: center;
  color: var(--text-muted);
  font-size: 13px;
  margin-bottom: 28px;
}

.auth-box form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.auth-switch {
  text-align: center;
  margin-top: 20px;
  color: var(--text-muted);
  font-size: 13px;
}

.auth-switch a {
  color: var(--accent-gold);
  text-decoration: none;
}

.auth-switch a:hover {
  color: var(--accent-gold-bright);
}
</style>
