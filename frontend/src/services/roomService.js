import api from './api'

export const roomService = {
  async getAllRooms(moduleId = null) {
    const params = moduleId ? { module_id: moduleId } : {}
    const response = await api.get('/rooms', { params })
    return response.data
  },

  async getGmRooms() {
    const response = await api.get('/rooms/gm')
    return response.data
  },

  async getModuleRooms(moduleId) {
    const response = await api.get(`/modules/${moduleId}/rooms`)
    return response.data
  },

  async getRoom(id) {
    const response = await api.get(`/rooms/${id}`)
    return response.data
  },

  async createRoom(moduleId, roomData) {
    const response = await api.post(`/modules/${moduleId}/rooms`, roomData)
    return response.data
  },

  async updateRoom(id, roomData) {
    const response = await api.put(`/rooms/${id}`, roomData)
    return response.data
  },

  async deleteRoom(id) {
    const response = await api.delete(`/rooms/${id}`)
    return response.data
  },

  async startGame(id) {
    const response = await api.post(`/rooms/${id}/start`)
    return response.data
  },

  async endGame(id) {
    const response = await api.post(`/rooms/${id}/end`)
    return response.data
  },

  async joinRoom(id, characterName = null) {
    const params = characterName ? { character_name: characterName } : {}
    const response = await api.post(`/rooms/${id}/join`, null, { params })
    return response.data
  },

  async leaveRoom(id) {
    const response = await api.post(`/rooms/${id}/leave`)
    return response.data
  },

  async getRoomResources(roomId) {
    const response = await api.get(`/rooms/${roomId}/resources`)
    return response.data
  },

  async toggleResourceVisibility(roomId, resourceId, isShown) {
    const response = await api.post(`/rooms/${roomId}/resources/${resourceId}/toggle`, {
      is_shown: isShown
    })
    return response.data
  },

  async toggleBlockVisibility(roomId, resourceId, blockIndex, isRevealed) {
    const response = await api.post(`/rooms/${roomId}/resources/${resourceId}/toggle-block`, {
      block_index: blockIndex,
      is_revealed: isRevealed
    })
    return response.data
  },

  async getOnlineUsers(roomId) {
    const response = await api.get(`/rooms/${roomId}/online-users`)
    return response.data
  },

  async getPlayerNote(roomId) {
    const response = await api.get(`/rooms/${roomId}/my-note`)
    return response.data
  },

  async updatePlayerNote(roomId, content) {
    const response = await api.put(`/rooms/${roomId}/my-note`, { content })
    return response.data
  }
}
