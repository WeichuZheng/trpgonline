import api from './api'

export default {
  async getModuleMaps(moduleId) {
    const res = await api.get(`/modules/${moduleId}/maps`)
    return res.data
  },

  async getMap(mapId) {
    const res = await api.get(`/maps/${mapId}`)
    return res.data
  },

  async createMap(moduleId, formData) {
    const res = await api.post(`/modules/${moduleId}/maps`, formData)
    return res.data
  },

  async updateMap(mapId, data) {
    const res = await api.put(`/maps/${mapId}`, data)
    return res.data
  },

  async deleteMap(mapId) {
    const res = await api.delete(`/maps/${mapId}`)
    return res.data
  },

  async getRoomMap(roomId) {
    const res = await api.get(`/rooms/${roomId}/map`)
    return res.data
  },

  async setActiveMap(roomId, mapId) {
    const res = await api.put(`/rooms/${roomId}/active-map`, { map_id: mapId })
    return res.data
  },

  async createUnit(roomId, unitData) {
    const res = await api.post(`/rooms/${roomId}/map/units`, unitData)
    return res.data
  },

  async updateUnit(roomId, unitId, unitData) {
    const res = await api.put(`/rooms/${roomId}/map/units/${unitId}`, unitData)
    return res.data
  },

  async deleteUnit(roomId, unitId) {
    const res = await api.delete(`/rooms/${roomId}/map/units/${unitId}`)
    return res.data
  }
}
