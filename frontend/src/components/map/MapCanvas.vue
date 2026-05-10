<template>
  <div class="map-canvas-wrapper" ref="wrapperRef">
    <canvas
      ref="canvasRef"
      @wheel.prevent="onWheel"
      @mousedown="onMouseDown"
      @mousemove="onMouseMove"
      @mouseup="onMouseUp"
      @mouseleave="onMouseUp"
      @contextmenu.prevent
    />
    <div v-if="selectedUnit" class="token-detail-panel">
      <div class="detail-header">
        <span>{{ selectedUnit.name }}</span>
        <button class="close-btn" @click="selectedUnit = null">&times;</button>
      </div>
      <div class="detail-body">
        <div v-if="selectedUnit.hp != null" class="detail-row">
          <label>HP</label>
          <input type="number" :value="selectedUnit.hp" @change="onHpChange($event, 'hp')" />
          <span>/ {{ selectedUnit.max_hp }}</span>
        </div>
        <div class="detail-row">
          <label>大小</label>
          <input type="number" :value="selectedUnit.width" step="0.5" min="0.5" @change="onSizeChange($event, 'width')" />
          <span>&times;</span>
          <input type="number" :value="selectedUnit.height" step="0.5" min="0.5" @change="onSizeChange($event, 'height')" />
        </div>
      </div>
    </div>
    <div v-if="isGm" class="map-toolbar">
      <button class="toolbar-btn" @click="$emit('add-token')" title="添加 Token">+ Token</button>
    </div>
    <div class="zoom-indicator">{{ Math.round(scale * 100) }}%</div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'

const props = defineProps({
  mapData: { type: Object, default: null },
  units: { type: Array, default: () => [] },
  isGm: { type: Boolean, default: false }
})

const emit = defineEmits(['add-token', 'unit-move', 'unit-update', 'unit-delete'])

const wrapperRef = ref(null)
const canvasRef = ref(null)
const selectedUnit = ref(null)

let ctx = null
let animId = null
let scale = ref(1)
let viewport = { x: 0, y: 0 }
let mapImage = null
let isDraggingCanvas = false
let isDraggingToken = false
let dragTarget = null
let dragOffset = { x: 0, y: 0 }
let lastMouse = { x: 0, y: 0 }
let isResizing = false
let resizeHandle = null
let resizeStart = { x: 0, y: 0, w: 0, h: 0 }
const avatarCache = new Map() // url -> Image | null (null = loading)

const MIN_SCALE = 0.2
const MAX_SCALE = 5

function mapToScreen(mx, my) {
  return {
    x: (mx - viewport.x) * scale.value + (canvasRef.value?.width || 0) / 2,
    y: (my - viewport.y) * scale.value + (canvasRef.value?.height || 0) / 2
  }
}

function screenToMap(sx, sy) {
  const cw = canvasRef.value?.width || 0
  const ch = canvasRef.value?.height || 0
  return {
    x: (sx - cw / 2) / scale.value + viewport.x,
    y: (sy - ch / 2) / scale.value + viewport.y
  }
}

function loadMapImage() {
  if (!props.mapData?.image_url) {
    mapImage = null
    return
  }
  const img = new Image()
  img.onload = () => {
    mapImage = img
    centerOnMap()
  }
  img.src = props.mapData.image_url
}

function draw() {
  const canvas = canvasRef.value
  if (!canvas || !ctx) return

  const w = canvas.width
  const h = canvas.height
  ctx.clearRect(0, 0, w, h)

  ctx.fillStyle = '#0c0c14'
  ctx.fillRect(0, 0, w, h)

  ctx.save()
  ctx.translate(w / 2, h / 2)
  ctx.scale(scale.value, scale.value)
  ctx.translate(-viewport.x, -viewport.y)

  // Draw map image
  if (mapImage) {
    ctx.drawImage(mapImage, 0, 0)
  }

  // Draw grid
  const gridSize = props.mapData?.grid_size
  if (gridSize && gridSize > 0 && mapImage) {
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.15)'
    ctx.lineWidth = 1 / scale.value
    ctx.beginPath()
    for (let x = 0; x <= mapImage.width; x += gridSize) {
      ctx.moveTo(x, 0)
      ctx.lineTo(x, mapImage.height)
    }
    for (let y = 0; y <= mapImage.height; y += gridSize) {
      ctx.moveTo(0, y)
      ctx.lineTo(mapImage.width, y)
    }
    ctx.stroke()
  }

  // Draw units
  for (const unit of props.units) {
    drawUnit(unit)
  }

  ctx.restore()

  animId = requestAnimationFrame(draw)
}

function getAvatarImage(url) {
  if (avatarCache.has(url)) return avatarCache.get(url)
  const img = new Image()
  img.onload = () => { avatarCache.set(url, img) }
  img.src = url
  avatarCache.set(url, null)
  return null
}

function drawUnit(unit) {
  if (!ctx) return
  const gridSize = props.mapData?.grid_size || 50
  const x = unit.x
  const y = unit.y
  const w = unit.width * gridSize
  const h = unit.height * gridSize
  const cx = x + w / 2
  const cy = y + h / 2
  const r = Math.min(w, h) / 2

  const isSelected = selectedUnit.value?.id === unit.id
  const borderColor = unit.is_enemy ? '#dc3232' : '#3278dc'

  // Name above token
  const nameY = y - 6 / scale.value
  ctx.fillStyle = '#000'
  ctx.font = `bold ${11 / scale.value}px sans-serif`
  ctx.textAlign = 'center'
  ctx.textBaseline = 'bottom'
  // White outline for readability on any background
  ctx.strokeStyle = '#fff'
  ctx.lineWidth = 2.5 / scale.value
  ctx.lineJoin = 'round'
  ctx.strokeText(unit.name, cx, nameY)
  ctx.fillText(unit.name, cx, nameY)

  // Circle clip + avatar
  ctx.save()
  ctx.beginPath()
  ctx.arc(cx, cy, r, 0, Math.PI * 2)
  ctx.clip()

  // Background fill
  ctx.fillStyle = 'rgba(0,0,0,0.5)'
  ctx.fillRect(x, y, w, h)

  // Avatar image
  const avatarUrl = unit.icon
  if (avatarUrl) {
    const avatarImg = getAvatarImage(avatarUrl)
    if (avatarImg) {
      // Draw image centered in square within the circle
      const imgSize = r * 2
      ctx.drawImage(avatarImg, cx - r, cy - r, imgSize, imgSize)
    }
  } else {
    // No avatar: draw first character as fallback
    const fontSize = r * 0.8
    ctx.fillStyle = 'rgba(255,255,255,0.7)'
    ctx.font = `bold ${fontSize / scale.value}px sans-serif`
    ctx.textAlign = 'center'
    ctx.textBaseline = 'middle'
    ctx.fillText(unit.name.charAt(0), cx, cy)
  }
  ctx.restore()

  // Border (outside clip)
  ctx.strokeStyle = borderColor
  ctx.lineWidth = (isSelected ? 3 : 2) / scale.value
  ctx.beginPath()
  ctx.arc(cx, cy, r, 0, Math.PI * 2)
  ctx.stroke()

  // HP bar below token
  if (unit.hp != null && unit.max_hp != null && unit.max_hp > 0) {
    const barW = w * 0.8
    const barH = Math.max(4, r * 0.15)
    const barX = x + (w - barW) / 2
    const barY = y + h + 4 / scale.value
    ctx.fillStyle = 'rgba(0,0,0,0.6)'
    ctx.fillRect(barX, barY, barW, barH)
    const hpRatio = Math.max(0, unit.hp / unit.max_hp)
    ctx.fillStyle = hpRatio > 0.5 ? '#4caf50' : hpRatio > 0.25 ? '#ff9800' : '#f44336'
    ctx.fillRect(barX, barY, barW * hpRatio, barH)
  }

  // Selection highlight
  if (isSelected) {
    ctx.setLineDash([6 / scale.value, 4 / scale.value])
    ctx.strokeStyle = '#ffd700'
    ctx.lineWidth = 2 / scale.value
    ctx.beginPath()
    ctx.arc(cx, cy, r + 4 / scale.value, 0, Math.PI * 2)
    ctx.stroke()
    ctx.setLineDash([])

    // Resize handle (bottom-right)
    if (props.isGm) {
      const handleSize = 8 / scale.value
      const hx = cx + r * 0.7 - handleSize / 2
      const hy = cy + r * 0.7 - handleSize / 2
      ctx.fillStyle = '#ffd700'
      ctx.fillRect(hx, hy, handleSize, handleSize)
    }
  }
}

function hitTestUnit(mx, my) {
  const gridSize = props.mapData?.grid_size || 50
  for (let i = props.units.length - 1; i >= 0; i--) {
    const u = props.units[i]
    const ux = u.x
    const uy = u.y
    const uw = u.width * gridSize
    const uh = u.height * gridSize
    const cx = ux + uw / 2
    const cy = uy + uh / 2
    const r = Math.min(uw, uh) / 2
    if (r > 0) {
      const dx = mx - cx
      const dy = my - cy
      if (dx * dx + dy * dy <= r * r) return u
    }
  }
  return null
}

function hitResizeHandle(mx, my) {
  if (!selectedUnit.value || !props.isGm) return false
  const u = selectedUnit.value
  const gridSize = props.mapData?.grid_size || 50
  const uw = u.width * gridSize
  const uh = u.height * gridSize
  const cx = u.x + uw / 2
  const cy = u.y + uh / 2
  const r = Math.min(uw, uh) / 2
  const handleSize = 12 / scale.value
  const hx = cx + r * 0.7 - handleSize / 2
  const hy = cy + r * 0.7 - handleSize / 2
  return mx >= hx && mx <= hx + handleSize && my >= hy && my <= hy + handleSize
}

function onWheel(e) {
  const canvas = canvasRef.value
  if (!canvas) return
  const rect = canvas.getBoundingClientRect()
  const sx = e.clientX - rect.left
  const sy = e.clientY - rect.top
  const mapPos = screenToMap(sx, sy)

  const delta = e.deltaY > 0 ? 0.9 : 1.1
  const newScale = Math.min(MAX_SCALE, Math.max(MIN_SCALE, scale.value * delta))
  const ratio = newScale / scale.value

  const cw = canvas.width
  const ch = canvas.height
  viewport.x = mapPos.x - (sx - cw / 2) / newScale
  viewport.y = mapPos.y - (sy - ch / 2) / newScale
  scale.value = newScale
}

function onMouseDown(e) {
  const canvas = canvasRef.value
  if (!canvas) return
  const rect = canvas.getBoundingClientRect()
  const sx = e.clientX - rect.left
  const sy = e.clientY - rect.top
  const mapPos = screenToMap(sx, sy)

  lastMouse = { x: e.clientX, y: e.clientY }

  if (e.button === 1 || e.button === 2) {
    isDraggingCanvas = true
    return
  }

  if (e.button === 0) {
    // Check resize handle first
    if (selectedUnit.value && hitResizeHandle(mapPos.x, mapPos.y)) {
      isResizing = true
      resizeStart = {
        x: mapPos.x,
        y: mapPos.y,
        w: selectedUnit.value.width,
        h: selectedUnit.value.height
      }
      return
    }

    const hit = hitTestUnit(mapPos.x, mapPos.y)
    if (hit) {
      selectedUnit.value = hit
      if (props.isGm) {
        isDraggingToken = true
        dragTarget = hit
        const gridSize = props.mapData?.grid_size || 50
        dragOffset = {
          x: mapPos.x - hit.x,
          y: mapPos.y - hit.y
        }
      }
    } else {
      selectedUnit.value = null
    }
  }
}

function onMouseMove(e) {
  const canvas = canvasRef.value
  if (!canvas) return

  if (isDraggingCanvas) {
    const dx = e.clientX - lastMouse.x
    const dy = e.clientY - lastMouse.y
    viewport.x -= dx / scale.value
    viewport.y -= dy / scale.value
    lastMouse = { x: e.clientX, y: e.clientY }
    return
  }

  if (isDraggingToken && dragTarget) {
    const rect = canvas.getBoundingClientRect()
    const sx = e.clientX - rect.left
    const sy = e.clientY - rect.top
    const mapPos = screenToMap(sx, sy)
    dragTarget.x = mapPos.x - dragOffset.x
    dragTarget.y = mapPos.y - dragOffset.y
    return
  }

  if (isResizing && selectedUnit.value) {
    const rect = canvas.getBoundingClientRect()
    const sx = e.clientX - rect.left
    const sy = e.clientY - rect.top
    const mapPos = screenToMap(sx, sy)
    const gridSize = props.mapData?.grid_size || 50
    const dx = mapPos.x - resizeStart.x
    const dy = mapPos.y - resizeStart.y
    selectedUnit.value.width = Math.max(0.5, resizeStart.w + dx / gridSize)
    selectedUnit.value.height = Math.max(0.5, resizeStart.h + dy / gridSize)
    return
  }

  // Cursor style
  const rect = canvas.getBoundingClientRect()
  const sx = e.clientX - rect.left
  const sy = e.clientY - rect.top
  const mapPos = screenToMap(sx, sy)
  if (selectedUnit.value && hitResizeHandle(mapPos.x, mapPos.y)) {
    canvas.style.cursor = 'nwse-resize'
  } else if (hitTestUnit(mapPos.x, mapPos.y)) {
    canvas.style.cursor = props.isGm ? 'grab' : 'pointer'
  } else {
    canvas.style.cursor = 'default'
  }
}

function onMouseUp(e) {
  if (isDraggingToken && dragTarget) {
    emit('unit-update', dragTarget.id, { x: dragTarget.x, y: dragTarget.y })
    isDraggingToken = false
    dragTarget = null
  }

  if (isResizing && selectedUnit.value) {
    emit('unit-update', selectedUnit.value.id, {
      width: selectedUnit.value.width,
      height: selectedUnit.value.height
    })
    isResizing = false
  }

  isDraggingCanvas = false
}

function onHpChange(e, field) {
  if (!selectedUnit.value) return
  const val = parseInt(e.target.value) || 0
  const updates = { [field]: val }
  Object.assign(selectedUnit.value, updates)
  emit('unit-update', selectedUnit.value.id, updates)
}

function onSizeChange(e, field) {
  if (!selectedUnit.value) return
  const val = parseFloat(e.target.value) || 0.5
  const updates = { [field]: Math.max(0.5, val) }
  Object.assign(selectedUnit.value, updates)
  emit('unit-update', selectedUnit.value.id, updates)
}

function resizeCanvas() {
  const canvas = canvasRef.value
  const wrapper = wrapperRef.value
  if (!canvas || !wrapper) return
  canvas.width = wrapper.clientWidth
  canvas.height = wrapper.clientHeight
}

function centerOnMap() {
  if (!mapImage) return
  const canvas = canvasRef.value
  if (!canvas) return
  // Fit map to canvas with 90% margin
  const scaleX = canvas.width / mapImage.width
  const scaleY = canvas.height / mapImage.height
  scale.value = Math.min(scaleX, scaleY) * 0.9
  scale.value = Math.max(MIN_SCALE, Math.min(MAX_SCALE, scale.value))
  // Center viewport on map center
  viewport.x = mapImage.width / 2
  viewport.y = mapImage.height / 2
}

let resizeObserver = null

onMounted(() => {
  const canvas = canvasRef.value
  if (!canvas) return
  ctx = canvas.getContext('2d')
  resizeCanvas()
  loadMapImage()
  draw()

  resizeObserver = new ResizeObserver(() => {
    resizeCanvas()
  })
  resizeObserver.observe(wrapperRef.value)
})

onUnmounted(() => {
  if (animId) cancelAnimationFrame(animId)
  if (resizeObserver) resizeObserver.disconnect()
})

watch(() => props.mapData?.image_url, () => {
  loadMapImage()
  nextTick(centerOnMap)
})

watch(() => props.units, () => {
  // Keep selected unit reference in sync
  if (selectedUnit.value) {
    const updated = props.units.find(u => u.id === selectedUnit.value.id)
    if (updated) selectedUnit.value = updated
  }
}, { deep: true })

defineExpose({ centerOnMap, scale, viewport })
</script>

<style scoped>
.map-canvas-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: var(--bg-deep);
}

canvas {
  display: block;
  width: 100%;
  height: 100%;
}

.token-detail-panel {
  position: absolute;
  top: 12px;
  right: 12px;
  background: var(--bg-card);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  padding: 12px;
  min-width: 180px;
  color: var(--text-secondary);
  z-index: 10;
  box-shadow: var(--shadow-md);
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  font-weight: bold;
  font-size: 14px;
  color: var(--text-primary);
  font-family: var(--font-display);
}

.close-btn {
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: 18px;
  cursor: pointer;
  padding: 0 4px;
  transition: color 0.15s;
}

.close-btn:hover {
  color: var(--text-primary);
}

.detail-body { display: flex; flex-direction: column; gap: 6px; }

.detail-row { display: flex; align-items: center; gap: 6px; font-size: 13px; }

.detail-row label { color: var(--text-muted); min-width: 32px; }

.detail-row input {
  width: 50px;
  background: var(--bg-input);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-sm);
  color: var(--text-primary);
  padding: 2px 6px;
  font-size: 13px;
  font-family: var(--font-body);
}

.map-toolbar { position: absolute; bottom: 12px; left: 12px; z-index: 10; }

.toolbar-btn {
  background: linear-gradient(135deg, var(--accent-gold), var(--accent-ember));
  border: none;
  color: var(--text-inverse);
  padding: 6px 14px;
  border-radius: var(--radius-md);
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  font-family: var(--font-body);
  transition: box-shadow 0.2s;
}

.toolbar-btn:hover {
  box-shadow: 0 0 16px rgba(212, 168, 83, 0.25);
}

.zoom-indicator {
  position: absolute;
  bottom: 12px;
  right: 12px;
  background: rgba(0, 0, 0, 0.5);
  color: var(--text-muted);
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  font-size: 12px;
  z-index: 10;
  font-family: var(--font-mono);
}
</style>
