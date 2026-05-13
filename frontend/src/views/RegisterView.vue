<template>
  <div class="auth-container">
    <div class="auth-particles"></div>
    <div class="auth-box">
      <h1>注册冒险者</h1>
      <p class="auth-subtitle">创建你的身份，踏入未知</p>
      <form @submit.prevent="handleRegister">
        <AppInput v-model="form.username" label="用户名" placeholder="请输入用户名" :error="errors.username" required></AppInput>
        <AppInput v-model="form.password" type="password" label="密码" placeholder="请输入密码" :error="errors.password" required></AppInput>
        <div class="checkbox-label">
          <input v-model="form.can_create_module" type="checkbox" id="gm-check">
          <label for="gm-check">申请成为 GM（可创建模组）</label>
        </div>
        <AppButton type="submit" :loading="loading" block>注册</AppButton>
      </form>
      <p class="auth-switch">
        已有账号？ <router-link to="/login">登录</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, inject } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AppInput from '@/components/common/AppInput.vue'
import AppButton from '@/components/common/AppButton.vue'

const router = useRouter()
const authStore = useAuthStore()
const toast = inject('toast')

const form = reactive({ username: '', password: '', can_create_module: false })
const errors = reactive({ username: '', password: '' })
const loading = ref(false)

function validate() {
  let valid = true
  errors.username = ''
  errors.password = ''
  if (!form.username.trim()) { errors.username = '请输入用户名'; valid = false }
  else if (form.username.length < 3) { errors.username = '用户名至少3个字符'; valid = false }
  if (!form.password) { errors.password = '请输入密码'; valid = false }
  else if (form.password.length < 6) { errors.password = '密码至少6个字符'; valid = false }
  return valid
}

async function handleRegister() {
  if (!validate()) return
  loading.value = true
  try {
    await authStore.register({ username: form.username, password: form.password, requested_gm: form.can_create_module })
    toast.success('注册成功，请登录')
    router.push('/login')
  } catch (error) {
    toast.error(error.message || '注册失败')
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
    radial-gradient(ellipse at 30% 40%, rgba(var(--accent-rgb), 0.05) 0%, transparent 50%),
    radial-gradient(ellipse at 70% 70%, rgba(196, 122, 58, 0.04) 0%, transparent 40%);
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

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-secondary);
  font-size: 13px;
}

.checkbox-label input {
  width: 16px;
  height: 16px;
  accent-color: var(--accent-gold);
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
