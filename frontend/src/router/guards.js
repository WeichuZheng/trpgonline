import { useAuthStore } from '@/stores/auth'

export function createRouterGuard(router) {
  router.beforeEach(async (to, from, next) => {
    const authStore = useAuthStore()

    // Wait for initial auth check if token exists
    if (authStore.token && !authStore.user) {
      try {
        await authStore.fetchCurrentUser()
      } catch (e) {
        // Token invalid, will redirect to login
      }
    }

    if (to.meta.requiresAuth) {
      if (!authStore.isAuthenticated) {
        return next({ name: 'login', query: { redirect: to.fullPath } })
      }
    }

    if ((to.name === 'login' || to.name === 'register') && authStore.isAuthenticated) {
      return next({ name: 'dashboard' })
    }

    next()
  })

  return router
}
