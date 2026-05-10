import { defineStore } from 'pinia'
import { ref } from 'vue'
import { moduleService } from '@/services/moduleService'

export const useModulesStore = defineStore('modules', () => {
  const modules = ref([])
  const currentModule = ref(null)
  const loading = ref(false)
  const error = ref(null)

  async function fetchMyModules() {
    loading.value = true
    error.value = null
    try {
      // Backend returns array directly
      const data = await moduleService.getMyModules()
      modules.value = Array.isArray(data) ? data : []
      return modules.value
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchModule(id) {
    loading.value = true
    error.value = null
    try {
      const data = await moduleService.getModule(id)
      currentModule.value = data
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createModule(moduleData) {
    loading.value = true
    error.value = null
    try {
      // Backend returns ModuleResponse directly
      const data = await moduleService.createModule(moduleData)
      modules.value.unshift(data)
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateModule(id, moduleData) {
    loading.value = true
    error.value = null
    try {
      const data = await moduleService.updateModule(id, moduleData)
      const index = modules.value.findIndex(m => m.id === id)
      if (index > -1) {
        modules.value[index] = data
      }
      if (currentModule.value?.id === id) {
        currentModule.value = data
      }
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteModule(id) {
    loading.value = true
    error.value = null
    try {
      await moduleService.deleteModule(id)
      modules.value = modules.value.filter(m => m.id !== id)
      if (currentModule.value?.id === id) {
        currentModule.value = null
      }
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  function setCurrentModule(module) {
    currentModule.value = module
  }

  return {
    modules,
    currentModule,
    loading,
    error,
    fetchMyModules,
    fetchModule,
    createModule,
    updateModule,
    deleteModule,
    setCurrentModule
  }
})
