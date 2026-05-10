<template>
  <div :class="['app-select', { 'select-error': error, 'select-disabled': disabled }]">
    <label v-if="label" :for="selectId" class="select-label">
      {{ label }}
      <span v-if="required" class="required-mark">*</span>
    </label>
    <div class="select-wrapper">
      <select
        :id="selectId"
        :value="modelValue"
        :disabled="disabled"
        :class="['select-field', { 'has-error': error }]"
        @change="handleChange"
        @blur="$emit('blur', $event)"
        @focus="$emit('focus', $event)"
      >
        <option v-if="placeholder" value="" disabled>{{ placeholder }}</option>
        <option
          v-for="option in normalizedOptions"
          :key="option.value"
          :value="option.value"
        >
          {{ option.label }}
        </option>
      </select>
      <span class="select-arrow">
        <svg width="12" height="12" viewBox="0 0 12 12" fill="currentColor">
          <path d="M2.5 4.5L6 8L9.5 4.5" stroke="currentColor" stroke-width="1.5" fill="none"/>
        </svg>
      </span>
    </div>
    <div v-if="error" class="select-error-message">{{ error }}</div>
    <div v-else-if="hint" class="select-hint">{{ hint }}</div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: { type: [String, Number], default: '' },
  options: { type: Array, required: true },
  label: { type: String, default: '' },
  placeholder: { type: String, default: '' },
  disabled: { type: Boolean, default: false },
  required: { type: Boolean, default: false },
  error: { type: String, default: '' },
  hint: { type: String, default: '' },
  id: { type: String, default: '' },
  optionsType: { type: String, default: 'auto' }
})

const emit = defineEmits(['update:modelValue', 'blur', 'focus'])

const selectId = computed(() => props.id || `select-${Math.random().toString(36).substr(2, 9)}`)

function handleChange(event) {
  const rawValue = event.target.value
  const selectedOption = normalizedOptions.value.find(o => String(o.value) === rawValue)
  if (selectedOption && typeof selectedOption.value === 'number') {
    emit('update:modelValue', Number(rawValue))
  } else {
    emit('update:modelValue', rawValue)
  }
}

const normalizedOptions = computed(() => {
  if (!props.options || props.options.length === 0) return []
  const first = props.options[0]
  if (typeof first === 'object' && first !== null && 'value' in first && 'label' in first) return props.options
  if (typeof first === 'object' && first !== null) return Object.entries(props.options).map(([value, label]) => ({ value, label }))
  return props.options.map(value => ({ value, label: String(value) }))
})
</script>

<style scoped>
.app-select {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.select-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
}

.required-mark {
  color: var(--color-danger);
  margin-left: 2px;
}

.select-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.select-field {
  width: 100%;
  padding: 10px 36px 10px 14px;
  font-size: 14px;
  font-family: var(--font-body);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  background: var(--bg-input);
  color: var(--text-primary);
  cursor: pointer;
  appearance: none;
  outline: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.select-field:focus {
  border-color: var(--border-focus);
  box-shadow: 0 0 0 3px rgba(212, 168, 83, 0.08);
}

.select-field:disabled {
  background: rgba(0, 0, 0, 0.2);
  cursor: not-allowed;
  opacity: 0.6;
}

.select-field option {
  background: var(--bg-card);
  color: var(--text-primary);
}

.select-arrow {
  position: absolute;
  right: 14px;
  color: var(--text-muted);
  pointer-events: none;
}

.has-error {
  border-color: var(--color-danger);
}

.select-error-message {
  font-size: 12px;
  color: var(--color-danger);
}

.select-hint {
  font-size: 12px;
  color: var(--text-muted);
}

.select-disabled .select-wrapper {
  background: rgba(0, 0, 0, 0.2);
  cursor: not-allowed;
}
</style>
