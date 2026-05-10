import api from './api'

export const characterService = {
  async getRoomCharacters(roomId) {
    const response = await api.get(`/rooms/${roomId}/characters`)
    return response.data
  },

  async createCharacter(roomId, characterData) {
    const response = await api.post(`/rooms/${roomId}/characters`, characterData)
    return response.data
  },

  async updateCharacter(characterId, characterData) {
    const response = await api.put(`/characters/${characterId}`, characterData)
    return response.data
  },

  async deleteCharacter(characterId) {
    const response = await api.delete(`/characters/${characterId}`)
    return response.data
  },

  async attack(characterId, targetName = null) {
    const data = { character_id: characterId }
    if (targetName) data.target_name = targetName
    const response = await api.post(`/characters/${characterId}/attack`, data)
    return response.data
  }
}
