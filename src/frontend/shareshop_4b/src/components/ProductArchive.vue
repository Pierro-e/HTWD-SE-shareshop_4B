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
      Es wurden noch keine Produkte eingekauft.    <!-- eigentlich unnötig, da ein Einkauf nur existiert, wenn Produkte gekauft wurden -->
    </div> 

    <div v-else>
      <ProductCard
        v-for="product in purchased_products"
        :key="product.produkt_id"
        :product="product"
        :onSettings="product_settings"
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

         for (const product of this.purchased_products) {
          // produkt_menge formatieren: Wenn Nachkommastellen == 0, als Integer anzeigen
          if (
            product.produkt_menge !== undefined &&
            product.produkt_menge !== null
          ) {
            const menge = Number(product.produkt_menge);
            // Prüfen ob die Zahl eine ganze Zahl ist
            if (Number.isInteger(menge)) {
              product.produkt_menge = menge.toString(); // z.B. 5 statt 5.00
            } else {
              // andernfalls auf 2 Nachkommastellen runden (falls notwendig)
              product.produkt_menge = menge.toFixed(2);
            }
          }
        }
      } catch (error) {
        this.errorMessage = "Fehler beim Laden der eingekauften Produkte.";
      } finally {
        this.loadingActive = false;
      }
    },

    back_to_listArchive() {
      this.$router.push(`/list/${this.list_id}/archive`);
    },

    product_settings(product) {
      this.errorMessage = "";
      const id = this.purchase_id;
      const product_id = product.produkt_id;
      const nutzer_id = product.hinzugefuegt_von;

      this.$router.push({
        name: "ProductDetail",    // geht anscheinden auch so, anstatt den kompletten Pfad anzugeben
        params: {                 // muss nur in router.js so definiert werden 
          id: id,
          produktId: product_id,
          nutzerId: nutzer_id
        },
        query: {
          readonly: true      // wenn readonly = true, dann sind die Felder im ProductDetail nicht editierbar
        }
      });

    },
        

  },

  mounted() {
    this.purchase_name = this.$route.query.purchase_name;
    this.list_id = this.$route.query.list_id;
    this.getData(this.purchase_id);
  }


}
</script>