<template>
  <div class="einkauf">
    <div class="header">
      <button
        @click="einkauf_abbrechen"
        class="button button-cancel back-button"
      >
        Einkauf abbrechen
      </button>
      <h2 class="list-title">{{ list_name }}</h2>
      <button
        @click="einkauf_abschließen"
        class="button button-submit button-submit-header"
      >
        Einkauf abschließen
      </button>
    </div>

    <div v-if="errorMessage" class="error">
      {{ errorMessage }}
    </div>

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
            <strong>Menge:</strong> {{ produkt.produkt_menge }}
          </span>
          <span v-if="produkt.einheit_abk">
            {{ produkt.einheit_abk }}
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
  <div v-if="errorMessage" class="error">
    {{ errorMessage }}
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
    },

    async get_products(id) {
      this.errorMessage = "";
      try {
        const response = await axios.get(
          `http://141.56.137.83:8000/listen/${id}/produkte`,
        );
        this.listenprodukte = response.data;

        for (const produkt of this.listenprodukte) {
          try {
            const res1 = await axios.get(
              `http://141.56.137.83:8000/produkte/by-id/${produkt.produkt_id}`,
            );
            produkt.name = res1.data.name;
          } catch {
            produkt.name = "[Fehler beim Laden]";
          }

          try {
            const res2 = await axios.get(
              `http://141.56.137.83:8000/einheiten/${produkt.einheit_id}`,
            );
            produkt.einheit_abk = res2.data.abkürzung;
          } catch {
            produkt.einheit_abk = "";
          }

          if (
            produkt.produkt_menge !== undefined &&
            produkt.produkt_menge !== null
          ) {
            const menge = Number(produkt.produkt_menge);
            if (Number.isInteger(menge)) {
              produkt.produkt_menge = menge.toString();
            } else {
              produkt.produkt_menge = menge.toFixed(2);
            }
          }
          produkt.erledigt = false;
        }
      } catch (error) {
        if (error.response?.data?.detail) {
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

.header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100px; /* vorher 60px */
  background-color: rgb(6, 32, 12);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}

.list-title {
  color: white;
  font-size: 1.8rem;
  margin: 0;
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

.produkte-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  padding-top: 140px;
}

@media (min-width: 768px) {
  .produkte-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .produkte-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.produkt-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem; /* Abstand zwischen Checkbox und Text */
}

.produkt-card {
  background-color: #c8e2c8;
  border: 1px solid #e5e7eb;
  border-radius: 1rem;
  padding: 1rem;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  transition: box-shadow 0.3s ease;
}

.erledigt {
  opacity: 0.5;
  filter: grayscale(100%);
  transition:
    opacity 0.3s ease,
    filter 0.3s ease;
}

.produkt-card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.produkt-name {
  margin: 0;
  color: #000000;
  font-size: 1.2em;
  font-weight: bold;
  word-break: break-word;
}

.produkt-name.erledigt {
  text-decoration: line-through;
  color: #777;
}

.produkt-info {
  font-size: 1rem; /* 14px */
  color: #000000;
  font-weight: 450;
  display: flex;
  gap: 0.5rem;
  align-items: center; /* Vertikal zentrieren */
}

.produkt-info strong {
  font-weight: 600;
  color: #000000;
  text-align: left;
}

.produkt-beschreibung {
  font-size: 1rem;
  color: #000000;
  font-weight: 450;
  margin-top: 0.5rem;
  white-space: pre-wrap;
  text-align: left; /* Linksbündig explizit gesetzt */
}

.button-product-settings {
  background: none;
  color: rgb(61, 57, 53);
  border: none;
  font-size: 1.2em;
  cursor: pointer;
  padding: 0;
  margin-left: 10px;
  line-height: 1; /* optional, für vertikale Ausrichtung */
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
  position: fixed;
  top: 110px; /* Direkt unter dem Header, der 100px hoch ist */
  left: 50%;
  transform: translateX(-50%);
  background-color: #ffe6e6; /* hellroter Hintergrund */
  padding: 10px 20px;
  border: 1px solid #cc0000;
  border-radius: 6px;
  font-weight: bold;
  z-index: 1100; /* höher als der Header */
  max-width: 90%;
  text-align: center;
  box-shadow: 0 2px 8px rgba(204, 0, 0, 0.3);
}
</style>
