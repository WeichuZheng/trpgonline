import { defineStore } from 'pinia'
import { ref } from 'vue'
import { roomService } from '@/services/roomService'

export const useRoomsStore = defineStore('rooms', () => {
  const rooms = ref([])
  const gmRooms = ref([])
  const currentRoom = ref(null)
  const loading = ref(false)
  const error = ref(null)

  async function fetchAllRooms(moduleId = null) {
    loading.value = true
    error.value = null
    try {
      // Backend returns array directly
      let data
      if (moduleId) {
        data = await roomService.getModuleRooms(moduleId)
      } else {
        data = await roomService.getAllRooms()
      }
      rooms.value = Array.isArray(data) ? data : []
      return rooms.value
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchGmRooms() {
    loading.value = true
    error.value = null
    try {
      // Backend returns array directly
      const data = await roomService.getGmRooms()
      gmRooms.value = Array.isArray(data) ? data : []
      return gmRooms.value
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchRoom(id) {
    loading.value = true
    error.value = null
    try {
      // Backend returns RoomWithDetails directly
      const data = await roomService.getRoom(id)
      currentRoom.value = data
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createRoom(moduleId, roomData) {
    loading.value = true
    error.value = null
    try {
      // Backend returns RoomResponse directly
      const data = await roomService.createRoom(moduleId, roomData)
      gmRooms.value.unshift(data)
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateRoom(id, roomData) {
    loading.value = true
    error.value = null
    try {
      const data = await roomService.updateRoom(id, roomData)
      const index = gmRooms.value.findIndex(r => r.id === id)
      if (index > -1) {
        gmRooms.value[index] = data
      }
      if (currentRoom.value?.id === id) {
        currentRoom.value = data
      }
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteRoom(id) {
    loading.value = true
    error.value = null
    try {
      await roomService.deleteRoom(id)
      gmRooms.value = gmRooms.value.filter(r => r.id !== id)
      rooms.value = rooms.value.filter(r => r.id !== id)
      if (currentRoom.value?.id === id) {
        currentRoom.value = null
      }
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function startGame(roomId) {
    loading.value = true
    error.value = null
    try {
      const data = await roomService.startGame(roomId)
      // Update local room status
      if (currentRoom.value?.id === roomId) {
        currentRoom.value = { ...currentRoom.value, status: 'active' }
      }
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function endGame(roomId) {
    loading.value = true
    error.value = null
    try {
      const data = await roomService.endGame(roomId)
      if (currentRoom.value?.id === roomId) {
        currentRoom.value = { ...currentRoom.value, status: 'ended' }
      }
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  function setCurrentRoom(room) {
    currentRoom.value = room
  }

  return {
    rooms,
    gmRooms,
    currentRoom,
    loading,
    error,
    fetchAllRooms,
    fetchGmRooms,
    fetchRoom,
    createRoom,
    updateRoom,
    deleteRoom,
    startGame,
    endGame,
    setCurrentRoom
  }
})
