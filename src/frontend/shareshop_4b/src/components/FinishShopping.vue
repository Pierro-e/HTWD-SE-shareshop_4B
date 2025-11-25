<template>
  <label for="totalPrice">Gesamtpreis (€):</label>
  <input
    type="number"
    id="totalPrice"
    v-model.number="totalPrice"
    min="0"
    step="1"
  />
</template>

<script>
export default {
  methods: {
    set_price() {
      if (
        this.totalPrice === null ||
        isNaN(this.totalPrice) ||
        this.totalPrice < 0
      ) {
        this.errorMessage = "Bitte geben Sie einen gültigen Gesamtpreis ein.";
        return;
      }
      this.commit_purchase = false;
      this.einkauf_abschließen();
    },
  },
};
</script>
