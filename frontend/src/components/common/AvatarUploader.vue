<template>
  <div class="avatar-uploader">
    <div class="avatar-preview" @click="triggerUpload">
      <img v-if="modelValue" :src="modelValue" class="avatar-img" />
      <span v-else class="avatar-placeholder">+</span>
    </div>
    <input type="file" accept="image/*" @change="onFileSelect" ref="fileInput" hidden />
    <button v-if="modelValue" type="button" class="avatar-remove" @click="removeAvatar">移除</button>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue'
import api from '@/services/api'

const props = defineProps({
  modelValue: { type: String, default: '' }
})

const emit = defineEmits(['update:modelValue'])
const toast = inject('toast')
const fileInput = ref(null)
const uploading = ref(false)

function triggerUpload() {
  fileInput.value?.click()
}

async function onFileSelect(event) {
  const file = event.target.files[0]
  if (!file) return

  if (file.size > 10 * 1024 * 1024) {
    toast.error('图片大小不能超过 10MB')
    return
  }

  uploading.value = true
  try {
    const formData = new FormData()
    formData.append('file', file)
    const res = await api.post('/upload/avatar', formData)
    emit('update:modelValue', res.data.url)
  } catch (error) {
    toast.error(error.response?.data?.detail || '上传失败')
  } finally {
    uploading.value = false
    // Reset input so same file can be re-selected
    if (fileInput.value) fileInput.value.value = ''
  }
}

function removeAvatar() {
  emit('update:modelValue', '')
}
</script>

<style scoped>
.avatar-uploader {
  display: flex;
  align-items: center;
  gap: 8px;
}

.avatar-preview {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid var(--border-default);
  background: var(--bg-input);
  cursor: pointer;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: border-color 0.15s;
  flex-shrink: 0;
}

.avatar-preview:hover {
  border-color: var(--accent-gold);
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  font-size: 20px;
  color: var(--text-muted);
  line-height: 1;
}

.avatar-remove {
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: 11px;
  cursor: pointer;
  font-family: var(--font-body);
  transition: color 0.15s;
}

.avatar-remove:hover {
  color: var(--color-danger);
}
</style>
