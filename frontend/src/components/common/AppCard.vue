<template>
  <div :class="['app-card', { 'card-hoverable': hoverable, 'card-bordered': bordered }]">
    <div v-if="$slots.header || title || $slots['header-extra']" class="card-header">
      <slot name="header">
        <h3 v-if="title">{{ title }}</h3>
      </slot>
      <div v-if="$slots['header-extra']" class="card-header-extra">
        <slot name="header-extra"></slot>
      </div>
    </div>
    <div class="card-body">
      <slot></slot>
    </div>
    <div v-if="$slots.footer" class="card-footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, default: '' },
  hoverable: { type: Boolean, default: false },
  bordered: { type: Boolean, default: true }
})
</script>

<style scoped>
.app-card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.card-bordered {
  border: 1px solid var(--border-subtle);
}

.card-hoverable {
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.card-hoverable:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-glow);
  border-color: var(--border-focus);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 20px;
  border-bottom: 1px solid var(--border-subtle);
  background: rgba(0, 0, 0, 0.15);
}

.card-header h3 {
  margin: 0;
  font-family: var(--font-display);
  font-size: 15px;
  font-weight: 600;
  color: var(--accent-gold);
  letter-spacing: 0.03em;
}

.card-header-extra {
  flex-shrink: 0;
}

.card-body {
  padding: 18px 20px;
}

.card-footer {
  padding: 14px 20px;
  border-top: 1px solid var(--border-subtle);
  background: rgba(0, 0, 0, 0.1);
}
</style>
