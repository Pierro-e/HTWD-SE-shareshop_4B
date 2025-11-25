<template>
  <div class="list-archive">
    <AppHeader :title="`${purchase_name}`">
      <template #left>
        <button @click="back_to_Archive" class="button-cancel back-button">
          Zurück
        </button>
      </template>
    </AppHeader>

    <div>
      <strong>Gesamtpreis:</strong> {{ this.price || "Nicht angegeben" }} €
    </div>

    <div v-if="loadingActive" class="loading">Laden...</div>
    <div v-else-if="errorMessage" class="error">{{ errorMessage }}</div>

    <div v-else-if="purchased_products.length === 0" class="info">
      Es wurden noch keine Produkte eingekauft.    <!-- eigentlich unnötig, da ein Einkauf nur existiert, wenn Produkte gekauft wurden -->
    </div> 

    <div v-else>
      <div class=card-grid>
        <ProductCard
          v-for="product in purchased_products"
          :key="product.produkt_id"
          :product="product"
          :onSettings="product_settings"
          :hideSettings="true"
        >
          <template #extra>
            <div class="produkt-beschreibung" v-if="product.hinzufueger_name">    <!-- class und css Code muss noch gemacht werden -->
              <p>{{ product.hinzufueger_name }}</p>
            </div>
          </template>
        </ProductCard>
      </div>
    </div>

  </div>
  <BottomBar />
</template>

<script>
import axios from 'axios';
import AppHeader from './AppHeader.vue';
import ProductCard from './ProductCard.vue';
import BottomBar from './BottomBar.vue';

export default {
  name: "ProductArchive",
  props: ["purchase_id"],
  components: { 
    AppHeader,
    ProductCard,
    BottomBar 
  },
  data() {
      return{
          list_id: null,
          purchase_name: "",
          price: null,
          isUserArchive: false,
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

    back_to_Archive() {
      if (this.isUserArchive == 'true')
        this.$router.push(`/userArchive`);
      else
      this.$router.push(`/list/${this.list_id}/archive`);
    },

    product_settings(product) {
      // nichts machen
    },
        

  },

  mounted() {
    this.purchase_name = this.$route.query.purchase_name;
    this.list_id = this.$route.query.list_id;
    this.price = this.$route.query.price;
    this.isUserArchive = this.$route.query.isUserArchive;
    this.getData(this.purchase_id);
  }


}
</script>