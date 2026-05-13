import api from './api'

export const adminService = {
  async getUsers() {
    const response = await api.get('/admin/users')
    return response.data
  },

  async updateUser(userId, data) {
    const response = await api.put(`/admin/users/${userId}`, data)
    return response.data
  },

  async cleanupLogs(days = 30) {
    const response = await api.delete(`/admin/cleanup-logs?days=${days}`)
    return response.data
  }
}
