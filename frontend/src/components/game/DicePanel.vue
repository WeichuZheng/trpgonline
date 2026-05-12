<template>
  <AppCard title="掷骰子" class="dice-card">
    <div class="dice-section">
      <div class="dice-label">角色</div>
      <div class="char-select-row">
        <button
          v-for="char in characters"
          :key="char.id"
          :class="['char-chip', { active: selectedCharacterId === char.id }]"
          @click="$emit('update:selectedCharacterId', selectedCharacterId === char.id ? null : char.id)"
        >{{ char.name }}</button>
        <button
          :class="['char-chip', { active: selectedCharacterId === null }]"
          @click="$emit('update:selectedCharacterId', null)"
        >无</button>
      </div>
    </div>

    <div class="dice-section">
      <div class="dice-label">快速掷骰</div>
      <div class="dice-buttons">
        <AppButton v-for="d in [4, 6, 8, 10, 12, 20]" :key="d" :variant="selectedQuickDice === d ? 'primary' : 'secondary'" size="small" @click="$emit('update:selectedQuickDice', d)">
          d{{ d }}
        </AppButton>
      </div>
      <AppInput :model-value="diceReason" @update:model-value="$emit('update:diceReason', $event)" placeholder="原因（可选）"></AppInput>
      <AppButton @click="$emit('roll-quick')" :disabled="!selectedQuickDice" block size="small">掷 d{{ selectedQuickDice || '?' }}</AppButton>
    </div>

    <div class="dice-section">
      <div class="dice-label">常用预设</div>
      <div class="preset-buttons">
        <button v-for="p in presets" :key="p" class="preset-btn" @click="$emit('roll-preset', p)">{{ p }}</button>
      </div>
    </div>

    <div class="dice-section">
      <div class="dice-label">表达式掷骰</div>
      <div class="expr-row">
        <input
          :value="diceExpr"
          @input="$emit('update:diceExpr', $event.target.value)"
          class="expr-input"
          placeholder="如 2d6+3"
          @keyup.enter="$emit('roll-expr')"
        />
        <AppButton size="small" @click="$emit('roll-expr')" :disabled="!diceExpr.trim()">掷</AppButton>
      </div>
    </div>

    <div v-if="diceResult" class="dice-result">
      <div class="result-main">{{ diceResult.result }}</div>
      <div class="result-detail">{{ diceResult.details }}</div>
      <div class="result-reason" v-if="diceResult.reason">{{ diceResult.reason }}</div>
    </div>
  </AppCard>
</template>

<script setup>
import { computed } from 'vue'
import { useGameStore } from '@/stores/game'
import AppButton from '@/components/common/AppButton.vue'
import AppCard from '@/components/common/AppCard.vue'
import AppInput from '@/components/common/AppInput.vue'

const props = defineProps({
  characters: { type: Array, default: () => [] },
  selectedCharacterId: { type: [Number, null], default: null },
  selectedQuickDice: { type: [Number, null], default: null },
  diceExpr: { type: String, default: '' },
  diceReason: { type: String, default: '' },
  compact: { type: Boolean, default: false }
})

defineEmits(['update:selectedCharacterId', 'update:selectedQuickDice', 'update:diceExpr', 'update:diceReason', 'roll-quick', 'roll-expr', 'roll-preset'])

const presets = ['1d20', '1d100', '1d6', '2d6', '1d8', '1d10']

const gameStore = useGameStore()
const diceResult = computed(() => gameStore.diceResult)
</script>

<style scoped>
.dice-card { flex-shrink: 0; }
.dice-card :deep(.card-body) { padding: 12px 16px; }

.dice-section { margin-bottom: 10px; }
.dice-section:last-of-type { margin-bottom: 0; }

.dice-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 6px;
}

.char-select-row { display: flex; flex-wrap: wrap; gap: 4px; }

.char-chip {
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 12px;
  border: 1px solid var(--border-default);
  background: var(--bg-input);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.15s;
  font-family: var(--font-body);
}

.char-chip:hover { border-color: var(--accent-gold); color: var(--accent-gold); }

.char-chip.active {
  background: var(--accent-gold);
  color: var(--text-inverse);
  border-color: var(--accent-gold);
}

.dice-buttons { display: grid; grid-template-columns: repeat(3, 1fr); gap: 4px; margin-bottom: 6px; }

.preset-buttons { display: flex; flex-wrap: wrap; gap: 4px; }

.preset-btn {
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-family: var(--font-mono);
  border: 1px solid var(--border-default);
  background: var(--bg-input);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.15s;
}

.preset-btn:hover {
  border-color: var(--accent-gold);
  color: var(--accent-gold);
  background: rgba(var(--accent-rgb), 0.08);
}

.expr-row { display: flex; gap: 6px; }

.expr-input {
  flex: 1;
  padding: 6px 10px;
  font-size: 13px;
  font-family: var(--font-mono);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  background: var(--bg-input);
  color: var(--text-primary);
  outline: none;
  transition: border-color 0.2s;
}

.expr-input:focus {
  border-color: var(--border-focus);
  box-shadow: 0 0 0 3px rgba(var(--accent-rgb), 0.08);
}

.dice-result {
  margin-top: 10px;
  padding: 10px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  text-align: center;
}

.result-main { font-size: 28px; font-weight: 700; color: var(--accent-gold); font-family: var(--font-display); }
.result-detail { font-size: 12px; color: var(--text-muted); margin-top: 2px; word-break: break-all; }
.result-reason { font-size: 12px; color: var(--text-muted); margin-top: 2px; opacity: 0.7; }
</style>
