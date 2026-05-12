<template>
  <div class="resource-editor">
    <template v-if="editor">
      <EditorToolbar :editor="editor" :is-gm="isGm" @insert-image="onInsertImage" />
      <EditorContent :editor="editor" class="editor-content" />
    </template>
  </div>
</template>

<script setup>
import { watch, onBeforeUnmount, inject } from 'vue'
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import { CustomImage } from './ImageExtension.js'
import Underline from '@tiptap/extension-underline'
import TextAlign from '@tiptap/extension-text-align'
import Highlight from '@tiptap/extension-highlight'
import { TextStyle } from '@tiptap/extension-text-style'
import { Color } from '@tiptap/extension-color'
import FontFamily from '@tiptap/extension-font-family'
import Placeholder from '@tiptap/extension-placeholder'
import { VisibilityExtension } from './VisibilityExtension.js'
import { FontSize } from './FontSizeExtension.js'
import EditorToolbar from './EditorToolbar.vue'
import api from '@/services/api'

const props = defineProps({
  modelValue: { type: String, default: '' },
  isGm: { type: Boolean, default: false },
  placeholder: { type: String, default: '开始编写...' }
})

const emit = defineEmits(['update:modelValue'])
const toast = inject('toast')

const editor = useEditor({
  content: parseContent(props.modelValue),
  extensions: [
    StarterKit.configure({ heading: { levels: [1, 2, 3] } }),
    CustomImage.configure({ inline: false, allowBase64: false }),
    Underline,
    TextAlign.configure({ types: ['heading', 'paragraph', 'image'] }),
    Highlight.configure({ multicolor: false }),
    TextStyle,
    Color,
    FontFamily,
    FontSize,
    Placeholder.configure({ placeholder: props.placeholder }),
    VisibilityExtension,
  ],
  onUpdate: ({ editor }) => {
    const json = editor.getJSON()
    emit('update:modelValue', JSON.stringify(json))
  },
})

function parseContent(val) {
  if (!val) return ''
  try {
    const parsed = JSON.parse(val)
    if (parsed && typeof parsed === 'object' && parsed.type) return parsed
    return val
  } catch {
    // Legacy plain text: wrap in paragraphs
    return {
      type: 'doc',
      content: val.split('\n').filter(l => l.trim()).map(line => ({
        type: 'paragraph',
        content: [{ type: 'text', text: line }]
      }))
    }
  }
}

watch(() => props.modelValue, (val) => {
  if (!editor.value) return
  const current = JSON.stringify(editor.value.getJSON())
  if (JSON.stringify(parseContent(val)) !== current) {
    editor.value.commands.setContent(parseContent(val), false)
  }
})

onBeforeUnmount(() => {
  editor.value?.destroy()
})

async function onInsertImage(file) {
  try {
    const formData = new FormData()
    formData.append('file', file)
    const res = await api.post('/upload/image', formData)
    editor.value?.chain().focus().setImage({ src: res.data.url }).run()
  } catch (error) {
    toast.error(error.response?.data?.detail || '图片上传失败')
  }
}
</script>

<style scoped>
.resource-editor {
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  overflow: hidden;
  background: var(--bg-input);
}

.editor-content {
  padding: 16px;
  min-height: 300px;
  max-height: 70vh;
  overflow-y: auto;
}

/* TipTap content styles */
.editor-content :deep(.tiptap) {
  outline: none;
  min-height: 200px;
  color: var(--text-primary);
  font-size: 16px;
  line-height: 1.8;
}

.editor-content :deep(.tiptap p) { margin: 0 0 0.7em; }
.editor-content :deep(.tiptap h1) { font-size: 28px; font-weight: 700; margin: 0.8em 0 0.4em; color: var(--text-primary); font-family: var(--font-display); }
.editor-content :deep(.tiptap h2) { font-size: 22px; font-weight: 600; margin: 0.7em 0 0.35em; color: var(--text-primary); font-family: var(--font-display); }
.editor-content :deep(.tiptap h3) { font-size: 18px; font-weight: 600; margin: 0.6em 0 0.3em; color: var(--text-primary); }
.editor-content :deep(.tiptap ul) { padding-left: 1.5em; margin: 0.4em 0; }
.editor-content :deep(.tiptap ol) { padding-left: 1.5em; margin: 0.4em 0; }
.editor-content :deep(.tiptap li) { margin: 0.15em 0; }
.editor-content :deep(.tiptap blockquote) { border-left: 3px solid var(--accent-gold); padding-left: 12px; margin: 0.6em 0; color: var(--text-muted); font-style: italic; }
.editor-content :deep(.tiptap hr) { border: none; border-top: 1px solid var(--border-default); margin: 1em 0; }
.editor-content :deep(.tiptap img) { max-width: 100%; border-radius: var(--radius-sm); margin: 0.5em 0; }
.editor-content :deep(.tiptap div[style*="text-align"] img) { display: inline-block; margin: 0.5em 0; }
.editor-content :deep(.tiptap mark) { background: rgba(var(--accent-rgb), 0.3); padding: 1px 2px; border-radius: 2px; }

/* Visibility visual styles (editor mode) — block elements */
.editor-content :deep(.tiptap [data-visibility="gm-only"]:not(img)) {
  border-left: 3px solid #dc3232;
  background: rgba(220, 50, 50, 0.08);
  padding-left: 10px;
  margin-left: -13px;
  border-radius: 0 4px 4px 0;
  position: relative;
}

.editor-content :deep(.tiptap [data-visibility="gm-only"]:not(img)::before) {
  content: '🔒';
  position: absolute;
  left: -2px;
  top: 2px;
  font-size: 10px;
}

.editor-content :deep(.tiptap [data-visibility="hidden"]:not(img)) {
  border-left: 3px solid #9ca3af;
  background: rgba(156, 163, 175, 0.06);
  padding-left: 10px;
  margin-left: -13px;
  border-radius: 0 4px 4px 0;
  position: relative;
}

.editor-content :deep(.tiptap [data-visibility="hidden"]:not(img)::before) {
  content: '👁';
  position: absolute;
  left: -2px;
  top: 2px;
  font-size: 10px;
}

/* Visibility visual styles — img elements (use outline, not border-left/padding) */
.editor-content :deep(.tiptap img[data-visibility="gm-only"]) {
  outline: 3px solid #dc3232;
  outline-offset: 3px;
  opacity: 0.85;
}

.editor-content :deep(.tiptap img[data-visibility="hidden"]) {
  outline: 3px solid #9ca3af;
  outline-offset: 3px;
  opacity: 0.85;
}

.editor-content :deep(.tiptap p.is-editor-empty:first-child::before) {
  content: attr(data-placeholder);
  float: left;
  color: var(--text-muted);
  pointer-events: none;
  height: 0;
}
</style>
