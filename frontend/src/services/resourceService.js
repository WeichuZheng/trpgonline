import api from './api'

export const resourceService = {
  async getModuleResources(moduleId) {
    const response = await api.get(`/modules/${moduleId}/resources`)
    return response.data
  },

  async createResource(moduleId, resourceData) {
    const formData = new FormData()
    formData.append('type', resourceData.type)
    formData.append('title', resourceData.title)
    formData.append('display_type', resourceData.display_type || 'story')

    if (resourceData.type === 'image' && resourceData.file) {
      formData.append('file', resourceData.file)
    } else if (resourceData.type === 'text') {
      formData.append('content', resourceData.content || '')
    }

    const response = await api.post(`/modules/${moduleId}/resources`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return response.data
  },

  async updateResource(resourceId, resourceData) {
    const response = await api.put(`/resources/${resourceId}`, resourceData)
    return response.data
  },

  async deleteResource(resourceId) {
    const response = await api.delete(`/resources/${resourceId}`)
    return response.data
  },

  async toggleDefaultVisible(resourceId, visible) {
    const response = await api.post(`/resources/${resourceId}/toggle-visible`, {
      default_visible: visible
    })
    return response.data
  }
}
