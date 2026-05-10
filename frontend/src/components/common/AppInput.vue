<template>
  <div :class="['app-input', { 'input-group': $slots.append || $slots.prepend, 'input-error': error, 'input-disabled': disabled }]">
    <label v-if="label" :for="inputId" class="input-label">
      {{ label }}
      <span v-if="required" class="required-mark">*</span>
    </label>
    <div class="input-wrapper">
      <span v-if="$slots.prepend" class="input-prepend">
        <slot name="prepend"></slot>
      </span>
      <input
        :id="inputId"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :maxlength="maxlength"
        :class="['input-field', { 'has-error': error }]"
        @input="$emit('update:modelValue', $event.target.value)"
        @blur="$emit('blur', $event)"
        @focus="$emit('focus', $event)"
      >
      <span v-if="$slots.append" class="input-append">
        <slot name="append"></slot>
      </span>
    </div>
    <div v-if="error" class="input-error-message">{{ error }}</div>
    <div v-else-if="hint" class="input-hint">{{ hint }}</div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: { type: [String, Number], default: '' },
  type: { type: String, default: 'text' },
  label: { type: String, default: '' },
  placeholder: { type: String, default: '' },
  disabled: { type: Boolean, default: false },
  readonly: { type: Boolean, default: false },
  required: { type: Boolean, default: false },
  error: { type: String, default: '' },
  hint: { type: String, default: '' },
  maxlength: { type: Number, default: null },
  id: { type: String, default: '' }
})

defineEmits(['update:modelValue', 'blur', 'focus'])

const inputId = computed(() => props.id || `input-${Math.random().toString(36).substr(2, 9)}`)
</script>

<style scoped>
.app-input {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.input-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  font-family: var(--font-body);
}

.required-mark {
  color: var(--color-danger);
  margin-left: 2px;
}

.input-wrapper {
  display: flex;
  align-items: center;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  overflow: hidden;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  background: var(--bg-input);
}

.input-wrapper:focus-within {
  border-color: var(--border-focus);
  box-shadow: 0 0 0 3px rgba(212, 168, 83, 0.08);
}

.input-field {
  flex: 1;
  border: none;
  padding: 10px 14px;
  font-size: 14px;
  font-family: var(--font-body);
  outline: none;
  background: transparent;
  color: var(--text-primary);
}

.input-field::placeholder {
  color: var(--text-muted);
}

.input-field:disabled {
  background: rgba(0, 0, 0, 0.2);
  cursor: not-allowed;
  opacity: 0.6;
}

.input-prepend,
.input-append {
  display: flex;
  align-items: center;
  padding: 0 12px;
  background: rgba(0, 0, 0, 0.15);
  color: var(--text-muted);
  font-size: 14px;
}

.input-prepend {
  border-right: 1px solid var(--border-subtle);
}

.input-append {
  border-left: 1px solid var(--border-subtle);
}

.has-error + .input-append,
.input-wrapper:has(.has-error) {
  border-color: var(--color-danger);
}

.input-error-message {
  font-size: 12px;
  color: var(--color-danger);
}

.input-hint {
  font-size: 12px;
  color: var(--text-muted);
}

.input-disabled .input-wrapper {
  background: rgba(0, 0, 0, 0.2);
  cursor: not-allowed;
}
</style>
