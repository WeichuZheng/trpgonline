<template>
  <div class="editor-toolbar">
    <div class="toolbar-group">
      <select :value="headingLevel" @change="setHeading($event.target.value)" class="toolbar-select" title="标题">
        <option value="0">正文</option>
        <option value="1">标题 1</option>
        <option value="2">标题 2</option>
        <option value="3">标题 3</option>
      </select>
    </div>

    <div class="toolbar-divider"></div>

    <div class="toolbar-group">
      <select :value="currentFontFamily" @change="setFontFamily($event.target.value)" class="toolbar-select toolbar-select-font" title="字体">
        <option value="">默认</option>
        <option v-for="font in fontList" :key="font.value" :value="font.value">{{ font.label }}</option>
      </select>
    </div>

    <div class="toolbar-group">
      <select :value="currentFontSize" @change="setFontSize($event.target.value)" class="toolbar-select toolbar-select-size" title="字号">
        <option value="">默认</option>
        <option v-for="size in fontSizeList" :key="size.value" :value="size.value">{{ size.label }}</option>
      </select>
    </div>

    <div class="toolbar-divider"></div>

    <div class="toolbar-group">
      <button type="button" class="toolbar-btn" :class="{ active: editor.isActive('bold') }" @click="editor.chain().focus().toggleBold().run()" title="粗体"><b>B</b></button>
      <button type="button" class="toolbar-btn" :class="{ active: editor.isActive('italic') }" @click="editor.chain().focus().toggleItalic().run()" title="斜体"><i>I</i></button>
      <button type="button" class="toolbar-btn" :class="{ active: editor.isActive('underline') }" @click="editor.chain().focus().toggleUnderline().run()" title="下划线"><u>U</u></button>
    </div>

    <div class="toolbar-divider"></div>

    <div class="toolbar-group">
      <label class="toolbar-color" title="文字颜色">
        <span class="toolbar-btn color-btn" :style="{ '--dot-color': currentTextColor || '#e0e0e0' }">A</span>
        <input type="color" :value="currentTextColor || '#e0e0e0'" @input="setTextColor($event.target.value)" />
      </label>
      <label class="toolbar-color" title="背景高亮色">
        <span class="toolbar-btn color-btn highlight-btn" :style="{ '--dot-color': currentHighlightColor || '#d4a853' }">H</span>
        <input type="color" :value="currentHighlightColor || '#d4a853'" @input="setHighlightColor($event.target.value)" />
      </label>
    </div>

    <div class="toolbar-divider"></div>

    <div class="toolbar-group">
      <button type="button" class="toolbar-btn" :class="{ active: editor.isActive('bulletList') }" @click="editor.chain().focus().toggleBulletList().run()" title="无序列表">• 列表</button>
      <button type="button" class="toolbar-btn" :class="{ active: editor.isActive('orderedList') }" @click="editor.chain().focus().toggleOrderedList().run()" title="有序列表">1. 列表</button>
      <button type="button" class="toolbar-btn" :class="{ active: editor.isActive('blockquote') }" @click="editor.chain().focus().toggleBlockquote().run()" title="引用">❝</button>
      <button type="button" class="toolbar-btn" @click="editor.chain().focus().setHorizontalRule().run()" title="分割线">—</button>
    </div>

    <div class="toolbar-divider"></div>

    <div class="toolbar-group">
      <button type="button" class="toolbar-btn" :class="{ active: editor.isActive({ textAlign: 'left' }) }" @click="editor.chain().focus().setTextAlign('left').run()" title="左对齐">⇐</button>
      <button type="button" class="toolbar-btn" :class="{ active: editor.isActive({ textAlign: 'center' }) }" @click="editor.chain().focus().setTextAlign('center').run()" title="居中">⇔</button>
      <button type="button" class="toolbar-btn" :class="{ active: editor.isActive({ textAlign: 'right' }) }" @click="editor.chain().focus().setTextAlign('right').run()" title="右对齐">⇒</button>
    </div>

    <div class="toolbar-divider"></div>

    <div class="toolbar-group">
      <button type="button" class="toolbar-btn" @click="insertImage" title="插入图片">🖼</button>
    </div>

    <div class="toolbar-divider" v-if="isImageSelected"></div>

    <div class="toolbar-group" v-if="isImageSelected">
      <span class="toolbar-label">图片宽度</span>
      <button type="button" class="toolbar-btn" :class="{ active: currentImageWidth === '25%' }" @click="setImageWidth('25%')" title="25%">25%</button>
      <button type="button" class="toolbar-btn" :class="{ active: currentImageWidth === '50%' }" @click="setImageWidth('50%')" title="50%">50%</button>
      <button type="button" class="toolbar-btn" :class="{ active: currentImageWidth === '75%' }" @click="setImageWidth('75%')" title="75%">75%</button>
      <button type="button" class="toolbar-btn" :class="{ active: !currentImageWidth || currentImageWidth === '100%' }" @click="setImageWidth('100%')" title="100%">100%</button>
    </div>

    <div class="toolbar-divider" v-if="isImageSelected && isGm"></div>

    <div class="toolbar-group" v-if="isGm">
      <button type="button" class="toolbar-btn visibility-btn gm-only-btn" :class="{ active: currentVisibility === 'gm-only' }" @click="setVisibility('gm-only')" title="GM备注（仅GM可见）">🔒 GM</button>
      <button type="button" class="toolbar-btn visibility-btn hidden-btn" :class="{ active: currentVisibility === 'hidden' }" @click="setVisibility('hidden')" title="暂时隐藏（可一键显示）">👁 隐藏</button>
    </div>
  </div>

  <input type="file" accept="image/*" @change="onImageSelect" ref="imageInput" hidden />
</template>

<script setup>
import { computed, ref } from 'vue'
import { VISIBILITY_VISIBLE, VISIBILITY_GM_ONLY, VISIBILITY_HIDDEN } from './VisibilityExtension.js'

const props = defineProps({
  editor: { type: Object, required: true },
  isGm: { type: Boolean, default: false }
})

const emit = defineEmits(['insert-image'])
const imageInput = ref(null)

const fontList = [
  { label: '宋体', value: 'SimSun, STSong, serif' },
  { label: '黑体', value: 'SimHei, STHeiti, sans-serif' },
  { label: '楷体', value: 'KaiTi, STKaiti, serif' },
  { label: '仿宋', value: 'FangSong, STFangsong, serif' },
  { label: '微软雅黑', value: 'Microsoft YaHei, sans-serif' },
  { label: '等线', value: 'DengXian, sans-serif' },
  { label: '华文中宋', value: 'STZhongsong, serif' },
  { label: '华文楷体', value: 'STKaiti, serif' },
  { label: 'Arial', value: 'Arial, sans-serif' },
  { label: 'Times New Roman', value: 'Times New Roman, serif' },
  { label: 'Georgia', value: 'Georgia, serif' },
  { label: 'Courier New', value: 'Courier New, monospace' },
]

const fontSizeList = [
  { label: '12', value: '12px' },
  { label: '14', value: '14px' },
  { label: '16', value: '16px' },
  { label: '18', value: '18px' },
  { label: '20', value: '20px' },
  { label: '24', value: '24px' },
  { label: '28', value: '28px' },
  { label: '32', value: '32px' },
  { label: '36', value: '36px' },
  { label: '48', value: '48px' },
]

const headingLevel = computed(() => {
  for (let i = 1; i <= 3; i++) {
    if (props.editor.isActive('heading', { level: i })) return String(i)
  }
  return '0'
})

const currentFontFamily = computed(() => {
  return props.editor.getAttributes('textStyle').fontFamily || ''
})

const currentFontSize = computed(() => {
  return props.editor.getAttributes('textStyle').fontSize || ''
})

const currentTextColor = computed(() => {
  return props.editor.getAttributes('textStyle').color || ''
})

const currentHighlightColor = computed(() => {
  return props.editor.getAttributes('highlight').color || ''
})

const currentVisibility = computed(() => {
  for (const type of ['image', 'heading', 'paragraph', 'blockquote', 'bulletList', 'orderedList', 'horizontalRule']) {
    const attrs = props.editor.getAttributes(type)
    if (attrs && attrs.visibility && attrs.visibility !== VISIBILITY_VISIBLE) {
      return attrs.visibility
    }
  }
  return VISIBILITY_VISIBLE
})

function setHeading(level) {
  const chain = props.editor.chain().focus()
  if (level === '0') {
    chain.setParagraph().run()
  } else {
    chain.setHeading({ level: parseInt(level) }).run()
  }
}

function setFontFamily(value) {
  if (value) {
    props.editor.chain().focus().setFontFamily(value).run()
  } else {
    props.editor.chain().focus().unsetFontFamily().run()
  }
}

function setFontSize(value) {
  if (value) {
    props.editor.chain().focus().setFontSize(value).run()
  } else {
    props.editor.chain().focus().unsetFontSize().run()
  }
}

function setTextColor(color) {
  props.editor.chain().focus().setColor(color).run()
}

function setHighlightColor(color) {
  props.editor.chain().focus().toggleHighlight({ color }).run()
}

function setVisibility(vis) {
  const current = currentVisibility.value
  props.editor.chain().focus().setVisibility(vis === current ? VISIBILITY_VISIBLE : vis).run()
}

const isImageSelected = computed(() => props.editor.isActive('image'))

const currentImageWidth = computed(() => {
  const attrs = props.editor.getAttributes('image')
  return attrs?.width || null
})

function setImageWidth(width) {
  const finalWidth = currentImageWidth.value === width ? null : width
  props.editor.chain().focus().updateAttributes('image', { width: finalWidth }).run()
}

function insertImage() {
  imageInput.value?.click()
}

function onImageSelect(event) {
  const file = event.target.files[0]
  if (!file) return
  emit('insert-image', file)
  if (imageInput.value) imageInput.value.value = ''
}
</script>

<style scoped>
.editor-toolbar {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 8px;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-subtle);
  border-radius: var(--radius-md) var(--radius-md) 0 0;
  flex-wrap: wrap;
}

.toolbar-group { display: flex; align-items: center; gap: 2px; }

.toolbar-divider {
  width: 1px;
  height: 20px;
  background: var(--border-default);
  margin: 0 4px;
}

.toolbar-btn {
  padding: 4px 8px;
  border: 1px solid transparent;
  border-radius: 4px;
  background: transparent;
  color: var(--text-secondary);
  font-size: 12px;
  font-family: var(--font-body);
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
}

.toolbar-btn:hover { background: var(--bg-card); border-color: var(--border-default); }
.toolbar-btn.active { background: rgba(var(--accent-rgb), 0.2); color: var(--accent-gold); border-color: var(--accent-gold); }

.toolbar-select {
  padding: 4px 6px;
  font-size: 12px;
  font-family: var(--font-body);
  border: 1px solid var(--border-default);
  border-radius: 4px;
  background: var(--bg-input);
  color: var(--text-primary);
  outline: none;
  cursor: pointer;
}

.toolbar-select-font { max-width: 100px; }
.toolbar-select-size { max-width: 60px; }

/* Color picker buttons */
.toolbar-color {
  position: relative;
  cursor: pointer;
}

.toolbar-color input[type="color"] {
  position: absolute;
  width: 0;
  height: 0;
  opacity: 0;
  pointer-events: none;
}

.color-btn {
  position: relative;
  padding-bottom: 8px;
}

.color-btn::after {
  content: '';
  position: absolute;
  bottom: 3px;
  left: 4px;
  right: 4px;
  height: 3px;
  border-radius: 1px;
  background: var(--dot-color);
}

.highlight-btn {
  position: relative;
  padding-bottom: 8px;
}

.gm-only-btn.active { background: rgba(220, 50, 50, 0.15); color: #dc3232; border-color: #dc3232; }
.hidden-btn.active { background: rgba(156, 163, 175, 0.15); color: #9ca3af; border-color: #9ca3af; }

.toolbar-label {
  font-size: 11px;
  color: var(--text-muted);
  margin-right: 2px;
  white-space: nowrap;
}
</style>
