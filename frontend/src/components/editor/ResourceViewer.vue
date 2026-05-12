<template>
  <div class="resource-viewer" @click="onImageClick" @mouseup="onTextSelect">
    <!-- 摘录浮动按钮 -->
    <Teleport to="body">
      <button
        v-if="clipVisible"
        class="clip-btn"
        :style="{ left: clipPos.x + 'px', top: clipPos.y + 'px' }"
        @click="doClip"
      >摘录 → 笔记本</button>
    </Teleport>
    <template v-for="(segment, idx) in segments" :key="idx">
      <!-- Visible segment: always shown -->
      <div v-if="segment.type === 'visible'" v-html="segment.html" class="segment-content"></div>

      <!-- GM-only segment: only shown to GM -->
      <div v-else-if="segment.type === 'gm-only' && isGm" v-html="segment.html" class="segment-content"></div>

      <!-- Hidden block -->
      <template v-else-if="segment.type === 'hidden'">
        <!-- GM view: show with toggle button -->
        <div v-if="isGm" class="hidden-block" :class="{ revealed: segment.isRevealed }">
          <div class="hidden-block-bar">
            <span class="hidden-block-label">{{ segment.isRevealed ? '🔓 已显示给玩家' : '🔒 隐藏段落' }}</span>
            <button class="toggle-block-btn" @click="emit('toggle-block', segment.blockIndex)">
              {{ segment.isRevealed ? '隐藏' : '显示' }}
            </button>
          </div>
          <div class="hidden-block-content segment-content" v-html="segment.html"></div>
        </div>
        <!-- Player view: only show if block is revealed -->
        <div v-else-if="segment.isRevealed" v-html="segment.html" class="segment-content"></div>
      </template>
    </template>
    <div v-if="segments.length === 0 && content" class="empty-state">无可见内容</div>

    <!-- Lightbox overlay -->
    <Teleport to="body">
      <div v-if="lightboxVisible" class="lightbox-overlay" @click="closeLightbox" @wheel.prevent="onLightboxWheel">
        <div class="lightbox-hint">滚轮缩放 · 拖拽平移 · 点击关闭</div>
        <img
          :src="lightboxSrc"
          class="lightbox-img"
          :style="{ transform: `translate(${panX}px, ${panY}px) scale(${scale})` }"
          @mousedown.prevent="onLightboxMouseDown"
          @click.stop
        />
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted, watch, inject } from 'vue'
import { generateHTML } from '@tiptap/html'
import { useGameStore } from '@/stores/game'
import { roomService } from '@/services/roomService'
import StarterKit from '@tiptap/starter-kit'
import Underline from '@tiptap/extension-underline'
import TextAlign from '@tiptap/extension-text-align'
import Highlight from '@tiptap/extension-highlight'
import { TextStyle } from '@tiptap/extension-text-style'
import { Color } from '@tiptap/extension-color'
import FontFamily from '@tiptap/extension-font-family'
import { CustomImage } from './ImageExtension.js'
import { FontSize } from './FontSizeExtension.js'
import { VisibilityExtension, VISIBILITY_VISIBLE, VISIBILITY_GM_ONLY, VISIBILITY_HIDDEN } from './VisibilityExtension.js'

const props = defineProps({
  content: { type: String, default: '' },
  isGm: { type: Boolean, default: false },
  revealedBlocks: { type: Array, default: () => [] },
  docTitle: { type: String, default: '' }
})

const emit = defineEmits(['toggle-block'])

const extensions = [
  StarterKit.configure({ heading: { levels: [1, 2, 3] } }),
  CustomImage,
  Underline,
  TextAlign.configure({ types: ['heading', 'paragraph', 'image'] }),
  Highlight,
  TextStyle,
  Color,
  FontFamily,
  FontSize,
  VisibilityExtension,
]

// --- Lightbox ---
const lightboxVisible = ref(false)
const lightboxSrc = ref('')
const scale = ref(1)
const panX = ref(0)
const panY = ref(0)
const isPanning = ref(false)
const panStart = ref({ x: 0, y: 0, panX: 0, panY: 0 })

const gameStore = useGameStore()
const toast = inject('toast')
const clipVisible = ref(false)
const clipPos = ref({ x: 0, y: 0 })

function onImageClick(e) {
  if (e.target.tagName === 'IMG') {
    lightboxSrc.value = e.target.src
    scale.value = 1
    panX.value = 0
    panY.value = 0
    lightboxVisible.value = true
  }
}

function closeLightbox() {
  lightboxVisible.value = false
}

function onLightboxWheel(e) {
  const delta = e.deltaY > 0 ? -0.15 : 0.15
  scale.value = Math.min(5, Math.max(0.3, scale.value + delta))
}

function onLightboxMouseDown(e) {
  isPanning.value = true
  panStart.value = { x: e.clientX, y: e.clientY, panX: panX.value, panY: panY.value }
  window.addEventListener('mousemove', onLightboxMouseMove)
  window.addEventListener('mouseup', onLightboxMouseUp)
}

function onLightboxMouseMove(e) {
  if (!isPanning.value) return
  panX.value = panStart.value.panX + (e.clientX - panStart.value.x)
  panY.value = panStart.value.panY + (e.clientY - panStart.value.y)
}

function onLightboxMouseUp() {
  isPanning.value = false
  window.removeEventListener('mousemove', onLightboxMouseMove)
  window.removeEventListener('mouseup', onLightboxMouseUp)
}

function onTextSelect() {
  setTimeout(() => {
    const sel = window.getSelection()
    if (!sel || sel.isCollapsed || !sel.toString().trim()) {
      clipVisible.value = false
      return
    }
    const range = sel.getRangeAt(0)
    const rect = range.getBoundingClientRect()
    clipPos.value = {
      x: rect.left + rect.width / 2 - 60,
      y: rect.bottom + 8 + window.scrollY
    }
    clipVisible.value = true
  }, 10)
}

function onDocClick(e) {
  if (!e.target.closest('.clip-btn')) {
    clipVisible.value = false
  }
}

async function doClip() {
  const sel = window.getSelection()
  const text = sel?.toString().trim()
  if (!text) return
  clipVisible.value = false

  const source = props.docTitle || '未知文档'
  const quoteLine = `[${source}] ${text}`

  // Parse current note content as TipTap JSON, or create new doc
  let doc
  const raw = gameStore.playerNote?.content || ''
  if (raw) {
    try { doc = JSON.parse(raw) } catch { doc = { type: 'doc', content: [] } }
  } else {
    doc = { type: 'doc', content: [] }
  }

  if (!doc.content) doc.content = []

  doc.content.push({
    type: 'blockquote',
    content: [{ type: 'paragraph', content: [{ type: 'text', text: quoteLine }] }]
  })

  const newContent = JSON.stringify(doc)
  try {
    const result = await roomService.updatePlayerNote(gameStore.roomId, newContent)
    gameStore.setPlayerNote(result)
    toast.success('已摘录到笔记本')
  } catch {
    toast.error('摘录失败')
  }
}

function onKeydown(e) {
  if (e.key === 'Escape' && lightboxVisible.value) {
    closeLightbox()
  }
}

onMounted(() => {
  window.addEventListener('keydown', onKeydown)
  document.addEventListener('click', onDocClick)
})
onUnmounted(() => {
  window.removeEventListener('keydown', onKeydown)
  document.removeEventListener('click', onDocClick)
})

watch(() => props.content, () => {
  closeLightbox()
})

// --- Segments ---
const segments = computed(() => {
  if (!props.content) return []
  let doc
  try {
    doc = JSON.parse(props.content)
    if (!doc || typeof doc !== 'object' || !doc.type) {
      return [{ type: 'visible', html: props.content.split('\n').map(l => `<p>${escapeHtml(l)}</p>`).join('') }]
    }
  } catch {
    return [{ type: 'visible', html: props.content.split('\n').map(l => `<p>${escapeHtml(l)}</p>`).join('') }]
  }

  return computeSegments(doc, props.isGm, props.revealedBlocks)
})

function computeSegments(doc, isGm, revealedBlocks) {
  if (!doc || !doc.content) return []

  const result = []
  let currentVisibleNodes = []
  let currentHiddenNodes = []
  let hiddenBlockIndex = 0

  function flushVisible() {
    if (currentVisibleNodes.length > 0) {
      try {
        const html = generateHTML({ type: 'doc', content: currentVisibleNodes }, extensions)
        result.push({ type: 'visible', html })
      } catch {}
      currentVisibleNodes = []
    }
  }

  function flushHidden() {
    if (currentHiddenNodes.length > 0) {
      const blockIndex = hiddenBlockIndex++
      const isRevealed = revealedBlocks.includes(blockIndex)
      try {
        const html = generateHTML({ type: 'doc', content: currentHiddenNodes }, extensions)
        result.push({ type: 'hidden', blockIndex, isRevealed, html })
      } catch {}
      currentHiddenNodes = []
    }
  }

  for (const node of doc.content) {
    const vis = node.attrs?.visibility

    if (vis === VISIBILITY_HIDDEN) {
      flushVisible()
      currentHiddenNodes.push(node)
    } else if (vis === VISIBILITY_GM_ONLY) {
      flushVisible()
      flushHidden()
      if (isGm) {
        try {
          const html = generateHTML({ type: 'doc', content: [node] }, extensions)
          result.push({ type: 'gm-only', html })
        } catch {}
      }
    } else {
      flushHidden()
      currentVisibleNodes.push(node)
    }
  }

  flushVisible()
  flushHidden()
  return result
}

function escapeHtml(text) {
  const div = document.createElement('div')
  div.textContent = text
  return div.innerHTML
}
</script>

<style scoped>
.resource-viewer {
  color: var(--text-primary);
  font-size: 16px;
  line-height: 1.8;
}

.segment-content :deep(h1) { font-size: 28px; font-weight: 700; margin: 0.8em 0 0.4em; color: var(--text-primary); font-family: var(--font-display); }
.segment-content :deep(h2) { font-size: 22px; font-weight: 600; margin: 0.7em 0 0.35em; color: var(--text-primary); font-family: var(--font-display); }
.segment-content :deep(h3) { font-size: 18px; font-weight: 600; margin: 0.6em 0 0.3em; color: var(--text-primary); }
.segment-content :deep(p) { margin: 0 0 0.7em; }
.segment-content :deep(ul) { padding-left: 1.5em; margin: 0.4em 0; }
.segment-content :deep(ol) { padding-left: 1.5em; margin: 0.4em 0; }
.segment-content :deep(li) { margin: 0.15em 0; }
.segment-content :deep(blockquote) { border-left: 3px solid var(--accent-gold); padding-left: 12px; margin: 0.6em 0; color: var(--text-muted); font-style: italic; }
.segment-content :deep(hr) { border: none; border-top: 1px solid var(--border-default); margin: 1em 0; }
.segment-content :deep(mark) { background: rgba(var(--accent-rgb), 0.3); padding: 1px 2px; border-radius: 2px; }

/* Images in document */
.segment-content :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: var(--radius-sm);
  margin: 0.5em 0;
  cursor: zoom-in;
}

.segment-content :deep(div[style*="text-align"] img) {
  display: inline-block;
  margin: 0.5em 0;
}

/* GM-only markers for non-img elements */
.segment-content :deep([data-visibility="gm-only"]:not(img)) {
  border-left: 3px solid #dc3232;
  background: rgba(220, 50, 50, 0.08);
  padding-left: 10px;
  margin-left: -13px;
  border-radius: 0 4px 4px 0;
  position: relative;
}

.segment-content :deep([data-visibility="gm-only"]:not(img)::before) {
  content: '🔒';
  position: absolute;
  left: -2px;
  top: 2px;
  font-size: 10px;
}

/* GM-only marker for img elements */
.segment-content :deep(img[data-visibility="gm-only"]) {
  outline: 3px solid #dc3232;
  outline-offset: 3px;
  opacity: 0.85;
}

/* Hidden block styling (GM view) */
.hidden-block {
  border-left: 3px solid #9ca3af;
  background: rgba(156, 163, 175, 0.06);
  padding-left: 10px;
  margin-left: -13px;
  border-radius: 0 4px 4px 0;
  margin-bottom: 0.6em;
}

.hidden-block.revealed {
  border-left-color: var(--accent-gold);
  background: rgba(var(--accent-rgb), 0.06);
}

.hidden-block-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 8px;
  margin-bottom: 4px;
  background: rgba(0, 0, 0, 0.15);
  border-radius: 4px;
}

.hidden-block-label {
  font-size: 11px;
  color: var(--text-muted);
  font-weight: 500;
}

.hidden-block.revealed .hidden-block-label {
  color: var(--accent-gold);
}

.toggle-block-btn {
  padding: 2px 10px;
  border: 1px solid var(--border-default);
  border-radius: 4px;
  background: var(--bg-secondary);
  color: var(--text-secondary);
  font-size: 11px;
  font-family: var(--font-body);
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
}

.toggle-block-btn:hover {
  border-color: var(--accent-gold);
  color: var(--accent-gold);
  background: rgba(var(--accent-rgb), 0.1);
}

.hidden-block-content {
  padding-right: 4px;
}

.empty-state { text-align: center; padding: 24px; color: var(--text-muted); font-size: 13px; }

/* ===== Clip button ===== */
.clip-btn {
  position: absolute;
  z-index: 1000;
  padding: 4px 12px;
  background: linear-gradient(135deg, var(--accent-gold), var(--accent-ember));
  color: var(--text-inverse);
  border: none;
  border-radius: var(--radius-md);
  font-size: 12px;
  font-family: var(--font-body);
  cursor: pointer;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
  animation: clip-appear 0.15s ease;
  white-space: nowrap;
}

.clip-btn:hover {
  box-shadow: 0 4px 16px rgba(var(--accent-rgb), 0.35);
}

@keyframes clip-appear {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ===== Lightbox ===== */
.lightbox-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: zoom-out;
  animation: lightbox-fade-in 0.15s ease;
}

@keyframes lightbox-fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

.lightbox-hint {
  position: absolute;
  top: 16px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
  pointer-events: none;
  z-index: 1;
}

.lightbox-img {
  max-width: 90vw;
  max-height: 90vh;
  object-fit: contain;
  cursor: grab;
  user-select: none;
  transform-origin: center center;
  transition: transform 0.05s linear;
}

.lightbox-img:active {
  cursor: grabbing;
}
</style>
