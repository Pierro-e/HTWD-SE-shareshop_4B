<template>
  <button
    class="active"
    @click="$emit('click')"
  >
    <slot />
  </button>
</template>

<script setup>
const props = defineProps({
  fav_flag: { type: Boolean, default: true},
  color: { type: String, default: '#ffcc00' }
});

// Emit a native click event so the parent can listen with @click
defineEmits(['click'])
</script>

<style scoped>
/* General Styling of the FavButton */
button{
  background: none;
  outline: none;
  padding: 0;
  width: 48px; /* TODO: make it dynamic */
  height: 48px; /* TODO: make it dynamic */
  display: flex;
}

/* add ★ */
button::before {
  content: '';
  width: 100%;
  height: 100%;
  background: #242424;

/* draw ★ */
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
}

button:active::before {
  background: #ffcc00;
}
</style>
