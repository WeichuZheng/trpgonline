<template>
  <div id="trpg-app">
    <router-view></router-view>
    <AppToast ref="toastRef"></AppToast>
  </div>
</template>

<script setup>
import { ref, provide } from 'vue'

const toastRef = ref(null)

provide('toast', {
  success: (message, options) => toastRef.value?.success(message, options),
  error: (message, options) => toastRef.value?.error(message, options),
  warning: (message, options) => toastRef.value?.warning(message, options),
  info: (message, options) => toastRef.value?.info(message, options)
})
</script>

<style>
:root {
  /* === Inkfire & Parchment === */
  --bg-deep: #0c0c14;
  --bg-primary: #12121e;
  --bg-secondary: #1a1a2c;
  --bg-card: #1e1e30;
  --bg-card-hover: #242440;
  --bg-input: #16162a;
  --bg-elevated: #252542;

  --border-subtle: rgba(212, 168, 83, 0.12);
  --border-default: rgba(212, 168, 83, 0.18);
  --border-focus: rgba(212, 168, 83, 0.5);

  --accent-gold: #d4a853;
  --accent-gold-dim: #b8923f;
  --accent-gold-bright: #e8c06a;
  --accent-ember: #c47a3a;
  --accent-copper: #b87333;

  --text-primary: #e8dcc8;
  --text-secondary: #a89e8c;
  --text-muted: #6b6357;
  --text-inverse: #0c0c14;

  --color-success: #4a9e6e;
  --color-success-dim: rgba(74, 158, 110, 0.15);
  --color-danger: #b84040;
  --color-danger-dim: rgba(184, 64, 64, 0.15);
  --color-warning: #c49a3a;
  --color-warning-dim: rgba(196, 154, 58, 0.15);
  --color-info: #5a8ab8;
  --color-info-dim: rgba(90, 138, 184, 0.15);

  --font-display: 'Cinzel', 'Georgia', serif;
  --font-body: 'Lora', 'Georgia', serif;
  --font-mono: 'Fira Code', 'Consolas', monospace;

  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 10px;

  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.5);
  --shadow-glow: 0 0 20px rgba(212, 168, 83, 0.1);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: var(--font-body);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: var(--bg-deep);
  color: var(--text-primary);
  line-height: 1.6;
}

#trpg-app {
  min-height: 100vh;
}

h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-display);
  font-weight: 600;
  letter-spacing: 0.02em;
  color: var(--text-primary);
}

a {
  color: var(--accent-gold);
  text-decoration: none;
  transition: color 0.2s ease;
}

a:hover {
  color: var(--accent-gold-bright);
}

::selection {
  background: rgba(212, 168, 83, 0.3);
  color: var(--text-primary);
}

::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: var(--bg-deep);
}

::-webkit-scrollbar-thumb {
  background: rgba(212, 168, 83, 0.2);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(212, 168, 83, 0.35);
}
</style>
