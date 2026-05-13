import api from './api'

export const taskService = {
  async getModuleTasks(moduleId) {
    const response = await api.get(`/modules/${moduleId}/tasks`)
    return response.data
  },

  async createTask(moduleId, data) {
    const response = await api.post(`/modules/${moduleId}/tasks`, data)
    return response.data
  },

  async updateTask(taskId, data) {
    const response = await api.put(`/tasks/${taskId}`, data)
    return response.data
  },

  async deleteTask(taskId) {
    const response = await api.delete(`/tasks/${taskId}`)
    return response.data
  },

  async createClock(taskId, data) {
    const response = await api.post(`/tasks/${taskId}/clocks`, data)
    return response.data
  },

  async updateClock(clockId, data) {
    const response = await api.put(`/clocks/${clockId}`, data)
    return response.data
  },

  async deleteClock(clockId) {
    const response = await api.delete(`/clocks/${clockId}`)
    return response.data
  },

  async advanceClocks(roomId) {
    const response = await api.post(`/rooms/${roomId}/advance-clocks`)
    return response.data
  }
}
