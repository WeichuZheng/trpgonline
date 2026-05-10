import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useGameStore = defineStore('game', () => {
  const roomId = ref(null)
  const resources = ref([])
  const characters = ref([])
  const gameLogs = ref([])
  const wsConnected = ref(false)
  const ws = ref(null)
  const diceResult = ref(null)
  const attackResult = ref(null)
  const loading = ref(false)
  const activeMap = ref(null)
  const mapUnits = ref([])

  const visibleResources = computed(() => resources.value.filter(r => r.is_shown))
  const hiddenResources = computed(() => resources.value.filter(r => !r.is_shown))

  function setActiveMap(map) {
    activeMap.value = map
  }

  function setMapUnits(units) {
    mapUnits.value = units
  }

  function addMapUnit(unit) {
    const existing = mapUnits.value.findIndex(u => u.id === unit.id)
    if (existing > -1) {
      mapUnits.value[existing] = unit
    } else {
      mapUnits.value.push(unit)
    }
  }

  function updateMapUnit(unitId, updates) {
    const unit = mapUnits.value.find(u => u.id === unitId)
    if (unit) {
      Object.assign(unit, updates)
    }
  }

  function removeMapUnit(unitId) {
    mapUnits.value = mapUnits.value.filter(u => u.id !== unitId)
  }

  function setRoomId(id) {
    roomId.value = id
  }

  function setResources(data) {
    resources.value = data
  }

  function addResource(resource) {
    const existing = resources.value.findIndex(r => r.id === resource.id)
    if (existing > -1) {
      resources.value[existing] = resource
    } else {
      resources.value.push(resource)
    }
  }

  function updateResourceVisibility(resourceId, isShown) {
    const resource = resources.value.find(r => r.id === resourceId)
    if (resource) {
      resource.is_shown = isShown
    }
  }

  function setCharacters(data) {
    characters.value = data
  }

  function addCharacter(character) {
    const existing = characters.value.findIndex(c => c.id === character.id)
    if (existing > -1) {
      characters.value[existing] = character
    } else {
      characters.value.push(character)
    }
  }

  function updateCharacter(characterId, updates) {
    const character = characters.value.find(c => c.id === characterId)
    if (character) {
      Object.assign(character, updates)
    }
  }

  function removeCharacter(characterId) {
    characters.value = characters.value.filter(c => c.id !== characterId)
  }

  function addGameLog(log) {
    gameLogs.value.push({
      id: Date.now(),
      ...log,
      created_at: new Date().toISOString()
    })
  }

  function setGameLogs(logs) {
    gameLogs.value = logs
  }

  function setDiceResult(result) {
    diceResult.value = result
  }

  function setAttackResult(result) {
    attackResult.value = result
  }

  function setWsConnected(connected) {
    wsConnected.value = connected
  }

  function setWs(socket) {
    ws.value = socket
  }

  function clearGame() {
    roomId.value = null
    resources.value = []
    characters.value = []
    gameLogs.value = []
    diceResult.value = null
    attackResult.value = null
    wsConnected.value = false
    ws.value = null
    activeMap.value = null
    mapUnits.value = []
  }

  return {
    roomId,
    resources,
    characters,
    gameLogs,
    wsConnected,
    ws,
    diceResult,
    attackResult,
    loading,
    visibleResources,
    hiddenResources,
    activeMap,
    mapUnits,
    setRoomId,
    setResources,
    addResource,
    updateResourceVisibility,
    setCharacters,
    addCharacter,
    updateCharacter,
    removeCharacter,
    addGameLog,
    setGameLogs,
    setDiceResult,
    setAttackResult,
    setWsConnected,
    setWs,
    setActiveMap,
    setMapUnits,
    addMapUnit,
    updateMapUnit,
    removeMapUnit,
    clearGame
  }
})
