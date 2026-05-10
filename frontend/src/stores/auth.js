import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authService } from '@/services/authService'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)
  const loading = ref(false)
  let fetchPromise = null

  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const isGM = computed(() => user.value?.can_create_module === true)
  const username = computed(() => user.value?.username || '')

  async function login(credentials) {
    loading.value = true
    try {
      const data = await authService.login(credentials)
      token.value = data.access_token
      localStorage.setItem('token', data.access_token)

      const userData = await authService.getCurrentUser()
      user.value = userData

      return userData
    } catch (error) {
      throw error
    } finally {
      loading.value = false
    }
  }

  async function register(userData) {
    loading.value = true
    try {
      const data = await authService.register(userData)
      return data
    } catch (error) {
      throw error
    } finally {
      loading.value = false
    }
  }

  async function fetchCurrentUser() {
    if (!token.value) return null

    // Deduplicate concurrent calls
    if (fetchPromise) return fetchPromise

    loading.value = true
    fetchPromise = authService.getCurrentUser()
      .then(data => {
        user.value = data
        return data
      })
      .catch(error => {
        logout()
        throw error
      })
      .finally(() => {
        loading.value = false
        fetchPromise = null
      })

    return fetchPromise
  }

  function logout() {
    user.value = null
    token.value = null
    fetchPromise = null
    localStorage.removeItem('token')
  }

  // Initialize user if token exists
  if (token.value) {
    fetchCurrentUser().catch(() => {})
  }

  return {
    user,
    token,
    loading,
    isAuthenticated,
    isGM,
    username,
    login,
    register,
    fetchCurrentUser,
    logout
  }
})
