<template>
  <div class="card" :class="{ erledigt: produkt.erledigt }">
    <div class="card-header">
      <!-- Identische Struktur bei Einkauf und Liste, nur Unterschiede bei z.B Checkbox-Slot für Einkauf.
       dieser wird von List.vue nicht genutzt -->
      <slot name="left"></slot>

      <h3 class="card-name" :class="{ erledigt: produkt.erledigt }">
        {{ produkt.name || "Unbekanntes Produkt" }}
      </h3>

      <button @click="onSettings(produkt)" class="button button-product-settings">
        ✏️
      </button>
    </div>

    <div class="card-info" v-if="produkt.produkt_menge || produkt.einheit_abk">
      <span>
        <strong>Menge:</strong> {{ produkt.produkt_menge }} {{ produkt.einheit_abk }}
      </span>
    </div>
    <div class="card-info" v-else>
      <span style="visibility: hidden">Platzhalter</span>
    </div>

    <div class="card-beschreibung" v-if="produkt.beschreibung">
      <div>{{ produkt.beschreibung }}</div>
    </div>
    <div class="card-beschreibung" v-else>
      <div style="visibility: hidden">Platzhalter</div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProductCard",
  props: {
    produkt: { type: Object, required: true },
    onSettings: { type: Function, required: false }
  }
};
</script>