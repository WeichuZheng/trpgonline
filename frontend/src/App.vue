<template>
  <div id="trpg-app">
    <router-view></router-view>
    <AppToast ref="toastRef"></AppToast>
  </div>
</template>

<script setup>
import { ref, provide, onMounted } from 'vue'

const toastRef = ref(null)

provide('toast', {
  success: (message, options) => toastRef.value?.success(message, options),
  error: (message, options) => toastRef.value?.error(message, options),
  warning: (message, options) => toastRef.value?.warning(message, options),
  info: (message, options) => toastRef.value?.info(message, options)
})

onMounted(() => {
  const stored = localStorage.getItem('trpg-theme-preference')
  if (stored) {
    document.documentElement.setAttribute('data-theme', stored)
  }
})
</script>

<style>
/* ========== Shared (all themes) ========== */
:root {
  --font-display: 'Cinzel', 'Georgia', serif;
  --font-body: 'Lora', 'Georgia', serif;
  --font-mono: 'Fira Code', 'Consolas', monospace;
  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 10px;
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.5);
}

/* ========== Theme: dark (default) — Inkfire & Parchment ========== */
:root,
[data-theme="dark"] {
  --bg-deep: #0c0c14;
  --bg-primary: #12121e;
  --bg-secondary: #1a1a2c;
  --bg-card: #1e1e30;
  --bg-card-hover: #242440;
  --bg-input: #16162a;
  --bg-elevated: #252542;

  --accent-rgb: 212, 168, 83;
  --border-subtle: rgba(var(--accent-rgb), 0.12);
  --border-default: rgba(var(--accent-rgb), 0.18);
  --border-focus: rgba(var(--accent-rgb), 0.5);

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

  --shadow-glow: 0 0 20px rgba(var(--accent-rgb), 0.1);
}

/* ========== Theme: light — Ivory & Ink ========== */
[data-theme="light"] {
  --bg-deep: #f8f4ec;
  --bg-primary: #fefefe;
  --bg-secondary: #f0ebe0;
  --bg-card: #ffffff;
  --bg-card-hover: #f5f0e8;
  --bg-input: #faf7f0;
  --bg-elevated: #e8e0d4;

  --accent-rgb: 139, 94, 60;
  --border-subtle: rgba(var(--accent-rgb), 0.15);
  --border-default: rgba(var(--accent-rgb), 0.25);
  --border-focus: rgba(var(--accent-rgb), 0.5);

  --accent-gold: #8b5e3c;
  --accent-gold-dim: #6b4430;
  --accent-gold-bright: #a07050;
  --accent-ember: #a0522d;
  --accent-copper: #8b6914;

  --text-primary: #2c2416;
  --text-secondary: #5c5240;
  --text-muted: #8b8070;
  --text-inverse: #fefefe;

  --color-success: #3a8a5e;
  --color-success-dim: rgba(58, 138, 94, 0.12);
  --color-danger: #b84040;
  --color-danger-dim: rgba(184, 64, 64, 0.12);
  --color-warning: #b8942a;
  --color-warning-dim: rgba(184, 148, 42, 0.12);
  --color-info: #4a7aaa;
  --color-info-dim: rgba(74, 122, 170, 0.12);

  --shadow-glow: 0 0 20px rgba(var(--accent-rgb), 0.08);
}

/* ========== Theme: sepia — Old Parchment ========== */
[data-theme="sepia"] {
  --bg-deep: #e8dcc8;
  --bg-primary: #f5f0e0;
  --bg-secondary: #e0d4b8;
  --bg-card: #ede0c8;
  --bg-card-hover: #e5d8c0;
  --bg-input: #faf4ea;
  --bg-elevated: #ddd0b8;

  --accent-rgb: 139, 69, 19;
  --border-subtle: rgba(var(--accent-rgb), 0.15);
  --border-default: rgba(var(--accent-rgb), 0.25);
  --border-focus: rgba(var(--accent-rgb), 0.5);

  --accent-gold: #8b4513;
  --accent-gold-dim: #6b3010;
  --accent-gold-bright: #a06030;
  --accent-ember: #a0522d;
  --accent-copper: #7b5830;

  --text-primary: #3c2816;
  --text-secondary: #5c4230;
  --text-muted: #8b7355;
  --text-inverse: #f5f0e0;

  --color-success: #4a8a5e;
  --color-success-dim: rgba(74, 138, 94, 0.12);
  --color-danger: #b84a3a;
  --color-danger-dim: rgba(184, 74, 58, 0.12);
  --color-warning: #b08a2a;
  --color-warning-dim: rgba(176, 138, 42, 0.12);
  --color-info: #5a7a9a;
  --color-info-dim: rgba(90, 122, 154, 0.12);

  --shadow-glow: 0 0 20px rgba(var(--accent-rgb), 0.08);
}

/* ========== Theme: forest — Deep Woods ========== */
[data-theme="forest"] {
  --bg-deep: #0a1410;
  --bg-primary: #0f1a15;
  --bg-secondary: #152218;
  --bg-card: #1a2a20;
  --bg-card-hover: #1e3025;
  --bg-input: #122018;
  --bg-elevated: #203028;

  --accent-rgb: 90, 154, 106;
  --border-subtle: rgba(var(--accent-rgb), 0.12);
  --border-default: rgba(var(--accent-rgb), 0.18);
  --border-focus: rgba(var(--accent-rgb), 0.5);

  --accent-gold: #5a9a6a;
  --accent-gold-dim: #3a7a4a;
  --accent-gold-bright: #7ab880;
  --accent-ember: #8ab860;
  --accent-copper: #6b8b50;

  --text-primary: #c8dcc8;
  --text-secondary: #9cb89c;
  --text-muted: #5a7a5a;
  --text-inverse: #0a1410;

  --color-success: #4aae6e;
  --color-success-dim: rgba(74, 174, 110, 0.15);
  --color-danger: #b84a4a;
  --color-danger-dim: rgba(184, 74, 74, 0.15);
  --color-warning: #b89a3a;
  --color-warning-dim: rgba(184, 154, 58, 0.15);
  --color-info: #4a8aba;
  --color-info-dim: rgba(74, 138, 186, 0.15);

  --shadow-glow: 0 0 20px rgba(var(--accent-rgb), 0.1);
}

/* ========== Theme: ocean — Deep Blue ========== */
[data-theme="ocean"] {
  --bg-deep: #0a0e1a;
  --bg-primary: #0f1322;
  --bg-secondary: #151a2c;
  --bg-card: #1a1e30;
  --bg-card-hover: #1e2438;
  --bg-input: #121828;
  --bg-elevated: #202438;

  --accent-rgb: 74, 138, 184;
  --border-subtle: rgba(var(--accent-rgb), 0.12);
  --border-default: rgba(var(--accent-rgb), 0.18);
  --border-focus: rgba(var(--accent-rgb), 0.5);

  --accent-gold: #4a8ab8;
  --accent-gold-dim: #3a6a98;
  --accent-gold-bright: #6ab0d0;
  --accent-ember: #5a9ab8;
  --accent-copper: #4a8098;

  --text-primary: #c8d0e0;
  --text-secondary: #9ca8b8;
  --text-muted: #5a6878;
  --text-inverse: #0a0e1a;

  --color-success: #4aa87a;
  --color-success-dim: rgba(74, 168, 122, 0.15);
  --color-danger: #c84a5a;
  --color-danger-dim: rgba(200, 74, 90, 0.15);
  --color-warning: #c4a040;
  --color-warning-dim: rgba(196, 160, 64, 0.15);
  --color-info: #5a8ac8;
  --color-info-dim: rgba(90, 138, 200, 0.15);

  --shadow-glow: 0 0 20px rgba(var(--accent-rgb), 0.1);
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
  background: rgba(var(--accent-rgb), 0.3);
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
  background: rgba(var(--accent-rgb), 0.2);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--accent-rgb), 0.35);
}
</style>
