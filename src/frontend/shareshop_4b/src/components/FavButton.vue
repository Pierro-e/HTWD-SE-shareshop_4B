<template>
  <button :class="fav_flag && 'fav'"/>
</template>

<script setup>
const props = defineProps({
  fav_flag: { type: Boolean, default: false}, // true := product is a favorite
});
</script>

<style scoped>
/* general styling */
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

/* color ★ if product is a favorite */
.fav::before{
  background: #ffcc00;
}
</style>
