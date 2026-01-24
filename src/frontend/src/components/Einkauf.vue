<template>
  <AppHeader :title="list_name">
    <template #left>
      <button @click="einkauf_abbrechen" class="button-cancel">
        <font-awesome-icon icon="xmark" />
      </button>
    </template>

    <template #right>
      <button @click="prepare_purchase" class="button button-submit">
        <font-awesome-icon icon="check" />
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
    name="Einkauf abschließen"
    @close="commit_purchase = false"
  >
    <div class="popup-field">
      <label for="totalPrice">Gesamtpreis (€): </label>
      <input
        type="number"
        id="totalPrice"
        v-model.number="totalPrice"
        min="0"
        step="1"
      />
      <button @click="set_price" class="button button-submit">Speichern</button>
    </div>
  </PopUp>

  <BottomBar :highlight-btn="1" />
</template>

<script>
import { api } from "../api/client";
import AppHeader from "./AppHeader.vue";
import ProductCard from "./ProductCard.vue";
import BottomBar from "./BottomBar.vue";
import PopUp from "./PopUp.vue";

/**
 * Komponente zur Anzeige der Einkaufansicht einer Liste
 * @param {string} list_id - ID der Liste, die eingekauft werden soll (prop)
 * @param {object} user - aktueller Nutzer
 * @param {function} getUser - Funktion zum Abrufen der aktuellen Nutzerdaten
 */

export default {
  name: "Einkauf",
  inject: ["user", "getUser"],
  props: ["list_id"],
  components: {
    AppHeader,
    ProductCard,
    BottomBar,
    PopUp,
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
    /**
     * Lädt die Liste mit der gegebenen ID
     * @param id {number} - ID der Liste
     */
    async get_list(id) {
      this.errorMessage = "";
      try {
        const response = await api.get(`/listen/by-id/${id}`);
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

    /**
     * Lädt die Produkte der Liste mit der gegebenen ID
     * @param id {number} - ID der Liste
     */
   async get_products(id) {
      this.errorMessage = "";
      try {
        const response = await api.get(`/listen/${id}/produkte`);
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
    /**
     * Nutzer möchte Einkauf abbrechen
     */
    einkauf_abbrechen() {
      const list_id = this.list_id || this.$route.params.listenId;
      this.$router.push(`/list/${list_id}`);
    },
    /**
     * Nutzer möchte Einkauf abschließen --> Produkte filtern und PopUp öffnen
     */
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
    /**
     * Nutzer hat Gesamtpreis eingegeben und möchte Einkauf abschließen
     */
    set_price() {
      if (
        this.totalPrice === null ||
        isNaN(this.totalPrice) ||
        this.totalPrice < 0
      ) {
        this.errorMessage = "Bitte geben Sie einen gültigen Gesamtpreis ein.";
        return;
      }
      this.commit_purchase = false;
      this.einkauf_abschliessen();
    },
    /**
     * Nutzer möchte Einkauf endgültig abschließen (letzte Funktion --> danach ist der Einkauf vollzogen und gespeichert)
     */
    async einkauf_abschliessen() {
      this.errorMessage = "";
      const list_id = this.list_id || this.$route.params.listenId;
      const price = this.totalPrice;
      const erledigteProdukte = this.listenprodukte.filter((p) => p.erledigt);
      try {
        const response = await api.post(
          `/create/einkaufsarchiv/list/${list_id}`,
          {
            eingekauft_von: this.userData.id,
            gesamtpreis: price,
          },
        );

        const purchase_id = response.data.einkauf_id;

        await Promise.all(
          erledigteProdukte.map((produkt) =>
            api.post(`/create/eingekaufte_produkte/einkauf/${purchase_id}`, {
              produkt_id: produkt.produkt_id,
              produkt_menge: produkt.produkt_menge,
              einheit_id: produkt.einheit_id,
              hinzugefuegt_von: produkt.hinzugefügt_von,
              beschreibung: produkt.beschreibung,
            }),
          ),
        );

        await this.kosten_aufteilen(price, purchase_id);

        await Promise.all(
          erledigteProdukte.map((produkt) =>
            api.post(
              `/bedarfsvorhersage_create/nutzer/${produkt.hinzugefügt_von}`,
              {
                produkt_id: produkt.produkt_id,
              },
            ),
          ),
        );

        await Promise.all(
          erledigteProdukte.map((produkt) =>
            api.delete(`/listen/${list_id}/produkte/${produkt.produkt_id}`, {
              data: {
                hinzugefügt_von: produkt.hinzugefügt_von,
              },
            }),
          ),
        );

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
    /**
     * Ermittelt die Kostenaufteilung für den Einkauf und speichert diese
     * @param price {number} - Gesamtpreis des Einkaufs
     * @param einkauf_id {number} - ID des getätigten Einkaufs
     */
    async kosten_aufteilen(price, einkauf_id){
      /* Kostenaufteilung für alle Mitglider, die etwas zur Liste hinzugefügt haben und
      dieses Produkt eingekauft wurde */
      try {
        // Eingekaufte Produkte laden
        const response = await axios.get(
          `http://141.56.137.83:8000/eingekaufte_produkte/einkauf/${einkauf_id}`
        );

        const produkte = response.data;

        // Eindeutige Nutzer extrahieren, Set speichert jeden Wert nur einmal
        const beteiligteNutzerIds = [
          ...new Set(produkte.map(p => p.hinzugefuegt_von))
        ];
        console.log("Produkte:", produkte);
        console.log("Beteiligte IDs:", beteiligteNutzerIds);
        console.log("Käufer:", this.userData.id);
        // Falls nur der Käufer selbst etwas zur liste hinzugefügt hat → keine Aufteilung
        if (beteiligteNutzerIds.length === 1 &&
            beteiligteNutzerIds[0]===this.userData.id
            ) return;

        const price_per_member = price / beteiligteNutzerIds.length;

        await Promise.all(
          beteiligteNutzerIds
            .filter(nutzerId => nutzerId !== this.userData.id)
            .map(nutzerId =>
              axios.post("http://141.56.137.83:8000/kostenaufteilung", {
                empfaenger_id: this.userData.id,
                schuldner_id: nutzerId,
                betrag: price_per_member
              })
            )
        );

      } catch (error) {
        console.error("Fehler bei kosten_aufteilen:", error);
        throw error;
      }
      /*
      Ansatz für Kostenaufteilung für jedes Mitglied der Liste außer Einkäufer
      try {
        const response = await axios.get (`http://141.56.137.83:8000/listen/${list_id}/mitglieder`);

        const members = response.data;

        if (members.length <= 1) {
          return;
        }

        const price_per_member = price / members.length;

        await Promise.all(
          members
            .filter(m => m.nutzer_id !== this.userData.id)
            .map(m =>
              axios.post("http://141.56.137.83:8000/kostenaufteilung", {
                empfaenger_id: this.userData.id,
                schuldner_id: m.nutzer_id,
                betrag: price_per_member
                }
              )
            )
        );

      } catch (error) {
        console.error("Fehler bei kosten_aufteilen:", error);

        throw error;
      }
      */
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
  z-index: 1100; /* höher als der Header */
}
</style>
