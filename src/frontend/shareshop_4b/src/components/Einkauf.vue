<template>
  <div class="einkauf">
    <div class="header">
      <button
        @click="einkauf_abbrechen"
        class="button button-cancel back-button"
      >
        Einkauf abbrechen
      </button>
      <h2>{{ list_name }}</h2>
      <button
        @click="einkauf_abschließen"
        class="button button-submit button-submit-header"
      >
        Einkauf abschließen
      </button>
    </div>

    <div v-if="loadingActive" class="loading">Laden...</div>
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>

    <div class="produkte-grid">
      <div
        v-for="(produkt, index) in listenprodukte"
        :key="index"
        class="produkt-card"
        :class="{ erledigt: produkt.erledigt }"
      >
        <div class="produkt-header">
          <input
            type="checkbox"
            :id="`check-${index}`"
            class="produkt-checkbox"
            @change="toggle_Erledigt(produkt, $event)"
          />
          <h3 class="produkt-name" :class="{ erledigt: produkt.erledigt }">
            {{ produkt.name || "Unbekanntes Produkt" }}
          </h3>
          <button
            @click="product_details(produkt)"
            class="button button-product-settings"
          >
            ✏️
          </button>
        </div>

        <div
          class="produkt-info"
          v-if="produkt.produkt_menge || produkt.einheit_abk"
        >
          <span v-if="produkt.produkt_menge">
            <strong>Menge:</strong> {{ produkt.produkt_menge }} {{ produkt.einheit_abk }}
          </span>
        </div>
        <div class="produkt-info" v-else>
          <span style="visibility: hidden">Platzhalter</span>
        </div>

        <div class="produkt-beschreibung" v-if="produkt.beschreibung">
          <p v-if="produkt.beschreibung">
            {{ produkt.beschreibung }}
          </p>
        </div>
        <div class="produkt-beschreibung" v-else>
          <p style="visibility: hidden">Platzhalter</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { inject } from "vue";

export default {
  name: "Einkauf",
  inject: ["user", "getUser"],
  props: ["list_id"],
  data() {
    return {
      list_name: "",
      errorMessage: "",
      loadingActive: true,
      listenprodukte: [],
      userData: null,
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
      loadingActive = false;
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
          // Produktname holen
          //console.log(produkt.produkt_name);
          produkt.name = produkt.produkt_name;

          // Einheit holen
          produkt.einheit_abk = produkt.einheit_abk;

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

    async einkauf_abschließen() {
      this.errorMessage = "";
      const list_id = this.list_id || this.$route.params.listenId;
      try {
        const erledigteProdukte = this.listenprodukte.filter((p) => p.erledigt);

        if (erledigteProdukte.length === 0) {
          this.errorMessage = "Es sind keine Produkte abgehakt!";
          return;
        }

        for (const produkt of erledigteProdukte) {
          await axios.delete(
            `http://141.56.137.83:8000/listen/${list_id}/produkte/${produkt.produkt_id}`,
            {
              data: {
                hinzugefügt_von: produkt.hinzugefügt_von,
              },
            },
          );
        }

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
  z-index: 1100; /* höher als der Header */
}
</style>
