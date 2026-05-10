import api from './api'

export const moduleService = {
  async getMyModules() {
    const response = await api.get('/modules')
    return response.data
  },

  async getModule(id) {
    const response = await api.get(`/modules/${id}`)
    return response.data
  },

  async createModule(moduleData) {
    const response = await api.post('/modules', moduleData)
    return response.data
  },

  async updateModule(id, moduleData) {
    const response = await api.put(`/modules/${id}`, moduleData)
    return response.data
  },

  async deleteModule(id) {
    const response = await api.delete(`/modules/${id}`)
    return response.data
  }
}
