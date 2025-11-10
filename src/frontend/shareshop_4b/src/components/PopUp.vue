<template>
  <div class="popup-overlay">
    <div class="popup-content">
      <slot></slot>
      <button @click="$emit('close')" class="button button-cancel">X</button>
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style scoped>
.popup-overlay {
  position: fixed;
  z-index: 1000;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
.popup-content {
  background: var(--box-bg-color);
  padding: 1em 2em;
  border-radius: 0.5em;
  width: 100%;
  min-width: 250px;
  max-width: 300px;
  text-align: center;
  box-shadow: 0 4px 12px var(--box-shadow-color);
}
@media (max-width: 480px) {
  .popup-content {
    max-width: 260px;
  }
}
</style>
