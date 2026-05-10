import { createPinia } from 'pinia'

export const pinia = createPinia()

// Export stores
export { useAuthStore } from './auth'
export { useModulesStore } from './modules'
export { useRoomsStore } from './rooms'
export { useGameStore } from './game'
