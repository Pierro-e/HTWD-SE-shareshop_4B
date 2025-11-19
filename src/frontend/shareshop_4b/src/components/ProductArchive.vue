<template>
  <div class="list-archive">

    <AppHeader :title="`Einkaufsarchiv für\n${purchase_name}`" class="multiline-title">
      <template #left>
        <button @click="back_to_listArchive" class="button button-cancel back-button">
          Zurück
        </button>
      </template>
    </AppHeader>

    <div v-if="loadingActive" class="loading">Laden...</div>
    <div v-else-if="errorMessage" class="error">{{ errorMessage }}</div>

    <div v-else-if="purchased_products.length === 0" class="info">
      Es wurden noch keine Produkte eingekauft.
    </div>

    <div v-else>
      <ProductCard
        v-for="product in purchased_products"
        :key="product.id"
        :product="product"
      />
    </div>

  </div>
</template>

<script>
import axios from 'axios';
import AppHeader from './AppHeader.vue';
import ProductCard from './ProductCard.vue';

export default {
  name: "ProductArchive",
  props: ["purchase_id"],
  components: { AppHeader, ProductCard },

  data() {
      return{
          list_id: null,
          purchase_name: "",
          purchased_products: [],
          loadingActive: true,
          errorMessage: "",
      }
  },

  methods: {

    async getData(id) {
      try {
        const response = await axios.get(
          `http://141.56.137.83:8000/eingekaufte_produkte/einkauf/${this.purchase_id}`,
        );

        this.purchased_products = response.data;

    } catch (error) {
        this.errorMessage = "Fehler beim Laden der eingekauften Produkte.";
      } finally {
        this.loadingActive = false;
      }
    },

    back_to_listArchive() {
      this.$router.push(`/list/${this.list_id}/archive`);
    }
        

  },

  mounted() {
    this.purchase_name = this.$route.query.purchase_name;
    this.list_id = this.$route.query.list_id;
    this.getData(this.purchase_id);

  }


}
</script>