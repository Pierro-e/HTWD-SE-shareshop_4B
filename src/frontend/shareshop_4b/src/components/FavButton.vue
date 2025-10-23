<template>
  <!-- The outer <button> gives us native button semantics (focus, keyboard, etc.) -->
  <button
    class="star-button"
    :style="{ '--size': size + 'px', '--color': color }"
    @click="$emit('click')"
  >
    <slot />
  </button>
</template>

<script setup>
/**
 * Props
 *  - size   : Number – side length of the star (default 48 px)
 *  - color  : String – fill colour of the star (default #ffcc00)
 */
defineProps({
  size: { type: Number, default: 48 },
  color: { type: String, default: '#ffcc00' }
})

// Emit a native click event so the parent can listen with @click
defineEmits(['click'])
</script>

<style scoped>
.star-button {
  /* Use CSS variables for easy theming */
  --size: 48px;
  --color: #ffcc00;

  /* Basic button reset */
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  outline: none;

  /* Size the container */
  width: var(--size);
  height: var(--size);

  /* Center the star shape */
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ★ shape made with clip‑path */
.star-button::before {
  content: '';
  width: 100%;
  height: 100%;

  /* Star polygon (10 points – 5 outer, 5 inner) */
  clip-path: polygon(
    50% 0%,
    61% 35%,
    98% 35%,
    68% 57%,
    79% 91%,
    50% 70%,
    21% 91%,
    32% 57%,
    2% 35%,
    39% 35%
  );

  background: var(--color);
  transition: transform 0.15s ease, filter 0.15s ease;
}

/* Hover / active feedback */
.star-button:hover::before {
  filter: brightness(1.2);
}
.star-button:active::before {
  transform: scale(0.92);
}
</style>
