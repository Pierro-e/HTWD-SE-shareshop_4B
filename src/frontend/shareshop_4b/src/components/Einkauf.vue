<template>
  <div class="einkauf">
    <AppHeader title="list_name">
      <template #left>
        <BackButton />
      </template>
      <template #right>
        <button @click="commit_purchase = true" class="button button-submit">
          <font-awesome-icon icon="check" />
        </button>
      </template>
    </AppHeader>

    <div v-if="loadingActive" class="loading">Laden...</div>
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>

    <div :style="{ paddingTop: errorMessage ? '0' : '80px' }"></div>
    <div class="card-grid">
      <ProductCard
        v-for="(product, index) in products"
        :key="index"
        :product="product"
        :onSettings="product_settings"
        :hideSettings="true"
        @click="product.erledigt = !product.erledigt"
      >
        <template #left>
          <input
            type="checkbox"
            class="produkt-checkbox"
            :checked="product.erledigt"
            @change="product.erledigt = $event.target.checked"
          />
        </template>
      </ProductCard>
    </div>

    <PopUp
      v-if="commit_purchase"
      @close="commit_purchase = false"
      name="Einkauf abschließen"
    >
      <FinishShopping />
    </PopUp>
  </div>
</template>

<script>
import axios from "axios";
import { ref, provide } from "vue";
import AppHeader from "./AppHeader.vue";
import ProductCard from "./ProductCard.vue";
import PopUp from "./PopUp.vue";
import FinishShopping from "./FinishShopping.vue";
import BackButton from "./navigation/BackButton.vue";

export default {
  name: "Einkauf",
  inject: ["user", "getUser", "products", "updateProducts"],
  props: ["list_id"],
  components: { AppHeader, ProductCard, PopUp, FinishShopping, BackButton },
  data() {
    return {
      list_name: "",
      errorMessage: "",
      loadingActive: true,
      listenprodukte: [],
      commit_purchase: false,
      totalPrice: 0,
    };
  },
  methods: {
    async setListName(id) {
      this.errorMessage = "";
      try {
        const response = await axios.get(
          `http://141.56.137.83:8000/listen/by-id/${id}`,
        );
        this.list_name = response.data.name;
      } catch (error) {
        if (error.response?.data?.detail) {
          this.errorMessage = error.response.data.detail;
        } else {
          this.errorMessage = "Fehler beim Laden der Liste";
        }
      }
      this.loadingActive = false;
    },

    product_settings(produkt) {
      // nichts machen
    },
  },
  mounted() {
    this.updateProducts();
    this.setListName(this.$route.params.listenId);
  },
};
</script>

<style scoped>
.erledigt {
  opacity: 0.5;
  filter: grayscale(100%);
  transition:
    opacity 0.3s ease,
    filter 0.3s ease;
}

.produkt-checkbox {
  width: 1.2rem;
  height: 1.2rem;
  cursor: pointer;
}

.error {
  margin-top: 4em;
  z-index: 1100; /* höher als der Header */
}
</style>
