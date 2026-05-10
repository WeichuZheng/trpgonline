import { createRouter, createWebHistory } from 'vue-router'
import routes from './routes'
import { createRouterGuard } from './guards'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 应用路由守卫
createRouterGuard(router)

export default router
