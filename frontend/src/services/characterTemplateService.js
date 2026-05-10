import api from './api'

export const characterTemplateService = {
  async getModuleTemplates(moduleId) {
    const response = await api.get(`/modules/${moduleId}/character-templates`)
    return response.data
  },

  async createTemplate(moduleId, data) {
    const response = await api.post(`/modules/${moduleId}/character-templates`, data)
    return response.data
  },

  async updateTemplate(templateId, data) {
    const response = await api.put(`/modules/character-templates/${templateId}`, data)
    return response.data
  },

  async deleteTemplate(templateId) {
    const response = await api.delete(`/modules/character-templates/${templateId}`)
    return response.data
  },

  async getRoomTemplates(roomId) {
    const response = await api.get(`/rooms/${roomId}/character-templates`)
    return response.data
  }
}
