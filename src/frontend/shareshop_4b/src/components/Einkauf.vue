<template>
  <AppHeader :title="list_name">

    <template #left>
      <button @click="einkauf_abbrechen" class="button-cancel">
        <font-awesome-icon icon='xmark'/>
      </button>
    </template>

    <template #right>
      <button @click="prepare_purchase" class="button button-submit">
        <font-awesome-icon icon='check'/>
      </button>
    </template>
  </AppHeader>

  <div v-if="loadingActive" class="loading">Laden...</div>
  <div v-if="errorMessage" class="error">{{ errorMessage }}</div>

  <div :style="{ paddingTop: errorMessage ? '0' : '80px' }"></div>
  <div class="card-grid">
    <ProductCard
      v-for="(product, index) in listenprodukte"
      :key="index"
      :product="product"
      :onSettings="product_settings"
      :hideSettings=true
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
  >
    <div class="popup-field">
      <label for="totalPrice">Gesamtpreis (€):</label>
      <input
        type="number"
        id="totalPrice"
        v-model.number="totalPrice"
        min="0"
        step="1"
      />
      <button @click="set_price" class="button button-submit"> </button>
    </div>
  </PopUp>

  <BottomBar />
</template>

<script>
import axios from "axios";
import AppHeader from "./AppHeader.vue";
import ProductCard from "./ProductCard.vue";
import BottomBar from "./BottomBar.vue";
import PopUp from "./PopUp.vue";

export default {
  name: "Einkauf",
  inject: ["user", "getUser"],
  props: ["list_id"],
  components: {
    AppHeader,
    ProductCard,
    BottomBar,
    PopUp
  },
  data() {
    return {
      list_name: "",
      errorMessage: "",
      loadingActive: true,
      listenprodukte: [],
      userData: null,
      commit_purchase: false,
      totalPrice: 0,
    };
  },
  methods: {
    async get_list(id) {
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

   async get_products(id) {
      this.errorMessage = "";
      try {
        const response = await axios.get(
          `http://141.56.137.83:8000/listen/${id}/produkte`,
        );
        this.listenprodukte = response.data;
        //console.log(JSON.stringify(response.data, null, 2));

        for (const produkt of this.listenprodukte) {
          // produkt_menge formatieren: Wenn Nachkommastellen == 0, als Integer anzeigen
          if (
            produkt.produkt_menge !== undefined &&
            produkt.produkt_menge !== null
          ) {
            const menge = Number(produkt.produkt_menge);
            // Prüfen ob die Zahl eine ganze Zahl ist
            if (Number.isInteger(menge)) {
              produkt.produkt_menge = menge.toString(); // z.B. 5 statt 5.00
            } else {
              // andernfalls auf 2 Nachkommastellen runden (falls notwendig)
              produkt.produkt_menge = menge.toFixed(2);
            }
          }
        }
      } catch (error) {
        if (
          error.response &&
          error.response.data &&
          error.response.data.detail
        ) {
          this.errorMessage = error.response.data.detail;
        } else {
          this.errorMessage = "Fehler beim Laden der Produkte";
        }
      }
      this.loadingActive = false;
    },

    einkauf_abbrechen() {
      const list_id = this.list_id || this.$route.params.listenId;
      this.$router.push(`/list/${list_id}`);
    },

    prepare_purchase() {
      if (!this.listenprodukte || this.listenprodukte.length === 0) {
        this.errorMessage = "Keine Produkte vorhanden!";
        return;
      }
      const erledigteProdukte = this.listenprodukte.filter((p) => p.erledigt);

      if (erledigteProdukte.length === 0) {
          alert("Es sind keine Produkte abgehakt!");
          return;
      }

      this.totalPrice = 0;

      this.errorMessage = "";
      this.commit_purchase = true;
    },

    set_price() {
      if (this.totalPrice === null || isNaN(this.totalPrice) || this.totalPrice < 0) {
        this.errorMessage = "Bitte geben Sie einen gültigen Gesamtpreis ein.";
        return;
      }
      this.commit_purchase = false;
      this.einkauf_abschließen();
    },

    async einkauf_abschließen() {
      this.errorMessage = "";
      const list_id = this.list_id || this.$route.params.listenId;
      const price = this.totalPrice;
      const erledigteProdukte = this.listenprodukte.filter((p) => p.erledigt);
      try {
        const response = await axios.post(
          `http://141.56.137.83:8000/create/einkaufsarchiv/list/${list_id}`,
          {
            eingekauft_von: this.userData.id,
            gesamtpreis: price,
          }
        );

        const purchase_id = response.data.einkauf_id;

        await Promise.all(erledigteProdukte.map(produkt =>
          axios.post(
            `http://141.56.137.83:8000/create/eingekaufte_produkte/einkauf/${purchase_id}`,
            {
              produkt_id: produkt.produkt_id,
              produkt_menge: produkt.produkt_menge,
              einheit_id: produkt.einheit_id,
              hinzugefuegt_von: produkt.hinzugefügt_von,
              beschreibung: produkt.beschreibung,
            }
          )
        ));

        await Promise.all(erledigteProdukte.map(produkt =>
          axios.post(
            `http://141.56.137.83:8000/bedarfsvorhersage_create/nutzer/${produkt.hinzugefügt_von}`,
            {
              produkt_id: produkt.produkt_id,
            }
          )
        ));

        await Promise.all(erledigteProdukte.map(produkt =>
          axios.delete(
            `http://141.56.137.83:8000/listen/${list_id}/produkte/${produkt.produkt_id}`,
            {
              data: {
                hinzugefügt_von: produkt.hinzugefügt_von,
              }
            }
          )
        ));

        this.$router.push(`/list/${list_id}`);

      } catch (error) {
        if (
          error.response &&
          error.response.data &&
          error.response.data.detail
        ) {
          this.errorMessage = error.response.data.detail;
        } else {
          this.errorMessage = "Fehler beim Abschließen des Einkaufs.";
        }
      }
      this.totalPrice = 0;
    },
    product_settings(produkt) {
      // nichts machen
    },
  },

  mounted() {
    this.errorMessage = "";
    const id = this.list_id || this.$route.params.listenId;
    this.userData = this.user;
    this.get_list(id);
    this.get_products(id);
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
  z-index: 1100;   /* höher als der Header */
}
</style>
