<template>
  <div class="popup-overlay">
    <div class="popup-content">
      <header>
        <h3>{{ name }}</h3>
        <button @click="$emit('close')" class="button-delete">
          Abbrechen
        </button>
      </header>
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    name: { type: String, default: "PopUp" },
  },
};
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
  position: relative;
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

h3 {
  width: 50%;
}

button {
  width: 50%;
  height: 50%;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--box-bg-color);
}
</style>
