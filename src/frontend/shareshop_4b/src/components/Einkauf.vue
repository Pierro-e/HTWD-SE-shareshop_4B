<template>
  <div class="einkauf">
    
    <AppHeader :title="list_name">
      <template #left>
        <button @click="einkauf_abbrechen" class="button button-cancel back-button">
          Einkauf abbrechen
        </button>
      </template>

      <template #right>
        <button @click="prepare_purchase" class="button button-submit button-submit-header">
          Einkauf abschließen
        </button>
      </template>
    </AppHeader>

    <div v-if="loadingActive" class="loading">Laden...</div>
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
    
    <div class="produkte-grid">
      <ProductCard
        v-for="(product, index) in listenprodukte"
        :key="index"
        :product="product"
        :onSettings="product_settings"
      >
        <template #left>
          <input
            type="checkbox"
            :id="`check-${index}`"
            class="produkt-checkbox"
            @change="toggle_Erledigt(product, $event)"
          />
        </template>
      </ProductCard>
    </div>

    <PopUp
      v-if="commit_purchase"
      @confirm="set_price"
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
      </div>
    </PopUp>

  </div>
</template>

<script>
import axios from "axios";
import { inject } from "vue";
import AppHeader from "./AppHeader.vue";
import ProductCard from "./ProductCard.vue";
import PopUp from "./PopUp.vue";


export default {
  name: "Einkauf",
  inject: ["user", "getUser"],
  props: ["list_id"],
  components: { AppHeader , ProductCard, PopUp},
  
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

    product_details(produkt) {
      // anzeigen der Produktdetails: von wem hinzugefügt,
    },

    toggle_Erledigt(produkt, event) {
      produkt.erledigt = event.target.checked;
    },

    prepare_purchase() {
      if (!this.listenprodukte || this.listenprodukte.length === 0) {
        this.errorMessage = "Keine Produkte vorhanden!";
        return;
      }
      const erledigteProdukte = this.listenprodukte.filter((p) => p.erledigt);

      if (erledigteProdukte.length === 0) {
        this.errorMessage = "Es sind keine Produkte abgehakt!";
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
.einkauf {
  padding-top: 50px;
}

.back-button {
  position: absolute;
  left: 20px;
  top: 25px;
}

.button-submit-header {
  position: absolute;
  right: 20px;
  top: 25px;
}

.erledigt {
  opacity: 0.5;
  filter: grayscale(100%);
  transition:
    opacity 0.3s ease,
    filter 0.3s ease;
}

.produkt-name.erledigt {
  text-decoration: line-through;
  color: #777;
}

.produkt-checkbox {
  width: 1.2rem;
  height: 1.2rem;
  cursor: pointer;
}

/* Optional: wenn erledigt, z.B. durch Linie durch den Text */
.produkt-name.erledigt {
  text-decoration: line-through;
  color: #777;
}

.error {
  margin-top: 2em;
  z-index: 1100;
  /* höher als der Header */
}
</style>
