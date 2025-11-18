<template>
  <div class="produkt-card" :class="{ erledigt: produkt.erledigt }">
    <div class="produkt-header">

      <!-- Identische Struktur bei Einkauf und Liste, nur Unterschiede bei z.B Checkbox-Slot für Einkauf.
       dieser wird von List.vue nicht genutzt -->
      <slot name="left"></slot>

      <h3 class="produkt-name" :class="{ erledigt: produkt.erledigt }">
        {{ produkt.name || "Unbekanntes Produkt" }}
      </h3>

      <button @click="onSettings(produkt)" class="button button-product-settings">
        ✏️
      </button>
    </div>

    <div class="produkt-info" v-if="produkt.produkt_menge || produkt.einheit_abk">
      <span>
        <strong>Menge:</strong> {{ produkt.produkt_menge }} {{ produkt.einheit_abk }}
      </span>
    </div>
    <div class="produkt-info" v-else>
      <span style="visibility: hidden">Platzhalter</span>
    </div>

    <div class="produkt-beschreibung" v-if="produkt.beschreibung">
      <p>{{ produkt.beschreibung }}</p>
    </div>
    <div class="produkt-beschreibung" v-else>
      <p style="visibility: hidden">Platzhalter</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProductCard",
  props: {
    produkt: { type: Object, required: true },
    onSettings: { type: Function, required: true }
  }
};
</script>
