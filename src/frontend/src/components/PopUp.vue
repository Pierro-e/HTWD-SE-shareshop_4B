<template>
  <div class="overlay">
    <div class="popup">
      <button @click="$emit('close')" class="button-cancel">Abbrechen</button>
        
      <h2>{{ name }}</h2>
      <slot></slot>
    </div>
  </div>
</template>

<script>
/**
 * Erstellt einen Popup-Dialog über den aktuellen Content.
 * 
 * @vue-prop {string} [name=PopUp] Popuptitel
 */
export default {
  props: {
    name: { type: String, default: "PopUp" },
  },
};
</script>

<style scoped>
.overlay {
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
  padding: 0;
  border: none;
}

.popup {
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
  .popup {
    width: 70%;
  }

  .popup-content {
    max-width: 200px;
  }
}

</style>
