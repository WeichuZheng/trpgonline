<template>
  <button
    :class="['app-button', `btn-${variant}`, `btn-${size}`, { 'btn-loading': loading, 'btn-block': block }]"
    :disabled="disabled || loading"
    :type="type"
    @click="$emit('click', $event)"
  >
    <span v-if="loading" class="btn-spinner"></span>
    <slot></slot>
  </button>
</template>

<script setup>
defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (v) => ['primary', 'secondary', 'danger', 'success', 'ghost'].includes(v)
  },
  size: {
    type: String,
    default: 'medium',
    validator: (v) => ['small', 'medium', 'large'].includes(v)
  },
  type: {
    type: String,
    default: 'button'
  },
  disabled: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  block: {
    type: Boolean,
    default: false
  }
})

defineEmits(['click'])
</script>

<style scoped>
.app-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: 1px solid transparent;
  border-radius: var(--radius-md);
  cursor: pointer;
  font-family: var(--font-body);
  font-weight: 500;
  transition: all 0.2s ease;
  letter-spacing: 0.01em;
}

.app-button:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.btn-small {
  padding: 5px 12px;
  font-size: 12px;
}

.btn-medium {
  padding: 9px 20px;
  font-size: 14px;
}

.btn-large {
  padding: 13px 28px;
  font-size: 16px;
}

.btn-primary {
  background: linear-gradient(135deg, var(--accent-gold), var(--accent-ember));
  color: var(--text-inverse);
  border-color: var(--accent-gold-dim);
}

.btn-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, var(--accent-gold-bright), var(--accent-gold));
  box-shadow: 0 0 16px rgba(var(--accent-rgb), 0.25);
}

.btn-secondary {
  background: var(--bg-elevated);
  color: var(--text-secondary);
  border-color: var(--border-default);
}

.btn-secondary:hover:not(:disabled) {
  background: var(--bg-card-hover);
  color: var(--text-primary);
  border-color: var(--border-focus);
}

.btn-danger {
  background: var(--color-danger);
  color: var(--text-primary);
  border-color: #943030;
}

.btn-danger:hover:not(:disabled) {
  background: #cc4444;
  box-shadow: 0 0 12px rgba(184, 64, 64, 0.3);
}

.btn-success {
  background: var(--color-success);
  color: var(--text-primary);
  border-color: #3a7e56;
}

.btn-success:hover:not(:disabled) {
  background: #55b07e;
}

.btn-ghost {
  background: transparent;
  color: var(--text-secondary);
  border-color: transparent;
}

.btn-ghost:hover:not(:disabled) {
  background: rgba(var(--accent-rgb), 0.08);
  color: var(--text-primary);
}

.btn-block {
  width: 100%;
}

.btn-loading {
  position: relative;
  color: transparent;
}

.btn-spinner {
  position: absolute;
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top-color: currentColor;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
