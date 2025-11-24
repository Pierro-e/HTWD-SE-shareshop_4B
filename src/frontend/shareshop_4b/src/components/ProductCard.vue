<template>
  <div class="produkt-card" :class="{ erledigt: product.erledigt }">
    <div class="produkt-header">

      <!-- Identische Struktur bei Einkauf und Liste, nur Unterschiede bei z.B Checkbox-Slot für Einkauf.
       dieser wird von List.vue nicht genutzt -->
      <slot name="left"></slot>

      <h3 class="produkt-name" :class="{ erledigt: product.erledigt }">
        {{ product.produkt_name || "Unbekanntes Produkt" }}
      </h3>

      <button v-if="!hideSettings" @click="onSettings(product)" class="button button-product-settings">
        ✏️
      </button>
    </div>

    <div class="produkt-info" v-if="product.produkt_menge || product.einheit_abk">
      <span>
        <strong>Menge:</strong> {{ product.produkt_menge }} {{ product.einheit_abk }}
      </span>
    </div>
    <div class="produkt-info" v-else>
      <span style="visibility: hidden">Platzhalter</span>
    </div>

    <div class="produkt-beschreibung" v-if="product.beschreibung">
      <p class="beschreibung">{{ product.beschreibung }}</p>
    </div>
    <div class="produkt-beschreibung" v-else>
      <p style="visibility: hidden">Platzhalter</p>
    </div>

    <!-- Slot für extra Infos -->
    <slot name="extra"></slot>


  </div>
</template>

<script>
export default {
  name: "ProductCard",
  props: {
    product: { type: Object, required: true },
    onSettings: { type: Function, required: true },
    hideSettings: { type: Boolean, default: false } //true, wenn es ein Archivprodukt ist
  }
};
</script>

