import api from './api'

export const diceService = {
  async rollDice(roomId, diceData) {
    const payload = {
      dice: diceData.dice || '1d20',
      reason: diceData.reason || null
    }
    if (diceData.character_name) {
      payload.character_name = diceData.character_name
    }
    const response = await api.post(`/rooms/${roomId}/dice`, payload)
    return response.data
  },

  async getRoomLogs(roomId) {
    const response = await api.get(`/rooms/${roomId}/logs`)
    return response.data
  },

  async addCustomLog(roomId, content, action = 'custom') {
    const response = await api.post(`/rooms/${roomId}/logs`, { content, action })
    return response.data
  },

  async clearRoomLogs(roomId) {
    const response = await api.delete(`/rooms/${roomId}/logs`)
    return response.data
  }
}
