<template>
  <div class="einkauf">
    
    <AppHeader :title="list_name">
      
      <template #left>
        <button @click="einkauf_abbrechen" class="button button-cancel">
          <font-awesome-icon icon='xmark'/>
        </button>
      </template>

      <template #right>
        <button @click="einkauf_abschließen" class="button button-submit">
          <font-awesome-icon icon='check'/>
        </button>
      </template>
    </AppHeader>

    <div v-if="loadingActive" class="loading">Laden...</div>
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
    
    <div :style="{ paddingTop: errorMessage ? '0' : '80px' }"></div>
    <div class="produkte-grid">
      <ProductCard
        v-for="(produkt, index) in listenprodukte"
        :key="index"
        :produkt="produkt"
        @toggle="produkt.erledigt = !produkt.erledigt"
      >
        <template #left>
          <input
            type="checkbox"
            class="produkt-checkbox"
            :checked="produkt.erledigt"
            @change="produkt.erledigt = $event.target.checked"
          />
        </template>
      </ProductCard>
    </div>

  </div>
</template>

<script>
import axios from "axios";
import AppHeader from "./AppHeader.vue";
import ProductCard from "./ProductCard.vue";


export default {
  name: "Einkauf",
  inject: ["user", "getUser"],
  props: ["list_id"],
  components: { AppHeader , ProductCard},
  
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
      this.loadingActive = false;
    },

    einkauf_abbrechen() {
      const list_id = this.list_id || this.$route.params.listenId;
      this.$router.push(`/list/${list_id}`);
    },

    product_details(produkt) {
      // anzeigen der Produktdetails: von wem hinzugefügt,
    },

    async einkauf_abschließen() {
      this.errorMessage = "";
      const list_id = this.list_id || this.$route.params.listenId;
      try {


        if (!this.listenprodukte || this.listenprodukte.length === 0) {
          this.errorMessage = "Keine Produkte vorhanden!";
          return;
        }
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
  margin-top: 4em;
  z-index: 1100;
  /* höher als der Header */
}
</style>
