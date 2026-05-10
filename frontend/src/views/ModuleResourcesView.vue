<template>
  <div class="resources-view">
    <div class="page-header">
      <AppButton variant="ghost" @click="goBack">← 返回</AppButton>
      <h2>资源管理 - {{ module?.title }}</h2>
    </div>

    <div class="content" v-if="resources.length > 0">
      <AppCard v-for="resource in resources" :key="resource.id" class="resource-card">
        <h3>{{ resource.title }}</h3>
        <span class="resource-type">{{ getTypeLabel(resource.type) }}</span>
        <p v-if="resource.type === 'text'">{{ resource.content }}</p>
        <img v-else-if="resource.type === 'image'" :src="resource.content" :alt="resource.title">
      </AppCard>
    </div>
    <div v-else class="empty-state">
      暂无资源
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useModulesStore } from '@/stores/modules'
import { resourceService } from '@/services/resourceService'
import AppButton from '@/components/common/AppButton.vue'
import AppCard from '@/components/common/AppCard.vue'

const route = useRoute()
const router = useRouter()
const modulesStore = useModulesStore()
const toast = inject('toast')

const module = ref(null)
const resources = ref([])

onMounted(async () => {
  try {
    module.value = await modulesStore.fetchModule(route.params.id)
    const data = await resourceService.getModuleResources(route.params.id)
    resources.value = Array.isArray(data) ? data : []
  } catch (error) {
    toast.error('加载失败')
  }
})

function goBack() {
  router.push('/dashboard')
}

function getTypeLabel(type) {
  const labels = { text: '文本', image: '图片' }
  return labels[type] || type
}
</script>

<style scoped>
.resources-view {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.page-header h2 {
  font-size: 24px;
  color: #111827;
}

.content {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.resource-card h3 {
  margin-bottom: 8px;
}

.resource-type {
  display: inline-block;
  padding: 2px 8px;
  background: #e5e7eb;
  border-radius: 4px;
  font-size: 12px;
  margin-bottom: 12px;
}

.resource-card img {
  max-width: 100%;
  border-radius: 4px;
}

.empty-state {
  text-align: center;
  padding: 60px;
  color: #6b7280;
}
</style>
