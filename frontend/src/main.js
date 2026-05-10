import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import { setRouter } from '@/services/api'
import App from './App.vue'
import AppToast from '@/components/common/AppToast.vue'

// Create Vue app
const app = createApp(App)

// Use Pinia for state management
const pinia = createPinia()
app.use(pinia)

// Use Vue Router
app.use(router)

// Provide router to API module for 401 redirects
setRouter(router)

// Global toast component
app.component('AppToast', AppToast)

// Mount app
app.mount('#app')
