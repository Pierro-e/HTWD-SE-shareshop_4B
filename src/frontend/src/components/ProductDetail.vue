<template>
  <div class="wrapper">
    <div class="product-detail">
      <AppHeader :title="this.$route.query.list_name">
        <template #left>
          <button class="button-cancel" @click="$router.push(`/list/${listenId}`)">
            <font-awesome-icon icon='xmark'/>
          </button>
        </template>

      </AppHeader>
      <form @submit.prevent="saveProduct">
        <div class="product-name">{{ name }}</div>

        <label for="einheit">Hinzugefügt von: </label>
        <div class="form-group">{{ hinzufueger_name }}</div>

        <div class="form-group">
          <label for="beschreibung">Beschreibung:</label>
          <textarea id="beschreibung" v-model="beschreibung"></textarea>
        </div>

        <div class="form-group">
          <label for="einheit">Einheit:</label>
          <select id="einheit" v-model="einheit">
            <option value="">Keine Angabe</option>
            <option v-for="e in einheiten" :key="e.id" :value="e.id">{{ e.name }}</option>
          </select>
        </div>

        <div class="form-group">
          <label for="menge">Menge:</label>
          <input id="menge" type="number" step="0.01" min="0" v-model.number="menge" />
        </div>

        <div class="button-row">
          <button type="button" class="button-delete" @click="deleteProduct">Löschen</button>
          <button type="submit" class="button-submit">Speichern</button>
        </div>
      </form>

      <div v-if="message" class="success">{{ message }}</div>
      <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
    </div>
  </div>

  <BottomBar 
    :highlight-btn="1"
  />
</template>

<script>
import axios from "axios";
import BottomBar from "./BottomBar.vue";
import AppHeader from "./AppHeader.vue";

/**
 * Anzeigen/Bearbeiten der Details eines Produktes.
 * 
 * @vue-prop {number} produktId ID des Produkts
 * @vue-prop {number} listenId ID der Liste, in der sich das Produkt befindet
 * @vue-prop {number} nutzerId ID des Nutzers, welcher Produkt hinzugefügt hat
 */
export default {
  components: { 
    AppHeader,
    BottomBar
  },
  props: ["produktId", "listenId", "nutzerId"],
  data() {
    return {
      produkt_id: null,
      name: "",
      beschreibung: "",
      menge: "",
      einheit: 0,
      hinzugefügt_von: null,
      hinzufueger_name: "",
      einheiten: [],
      errorMessage: "",
      message: "",
    };
  },
  async mounted() {
    this.hinzugefügt_von = this.nutzerId;
    await this.fetchEinheiten();
    await this.fetchProduct();
  },
  methods: {
    /**
     * Lädt Eigenschaften des Produkts von API und setzt lokale Variablen.
     */
    async fetchProduct() {
      try {
        const response = await axios.get(
          `http://141.56.137.83:8000/listen/${this.listenId}/produkte`
        );
        const produkte = response.data;
        const produkt = produkte.find(
          (p) =>
            p.produkt_id === parseInt(this.produktId) &&
            p.hinzugefügt_von === parseInt(this.nutzerId)
        );
        if (!produkt) {
          this.errorMessage = "Produkt in dieser Liste nicht gefunden.";
          return;
        }

        this.produkt_id = produkt.produkt_id;
        this.name = produkt.produkt_name || "";
        this.menge = produkt.produkt_menge || "";
        this.einheit = produkt.einheit_id || "";
        this.beschreibung = produkt.beschreibung || "";
        this.hinzufueger_name = produkt.hinzufueger_name || "";
      } catch (error) {
        this.errorMessage = error.response?.data?.detail || "Fehler beim Laden des Produkts.";
      }
    },
    /**
     * Lädt Einheiten von API und setzt lokale Variable.
     */
    async fetchEinheiten() {
      try {
        const response = await axios.get(`http://141.56.137.83:8000/einheiten`);
        this.einheiten = response.data;
      } catch {
        this.errorMessage = "Einheiten konnten nicht geladen werden.";
      }
    },
    /**
     * Validiert und sendet Eigenschaften des Produkts an API. 
     */
    async saveProduct() {
      this.message = "";
      this.errorMessage = "";
      // 1. zuerst die menge als zahl behandeln
      // '0' setzen, wenn null, leer oder nicht nummerisch
      const mengeAlsZahl = Number(this.menge);
      this.menge = mengeAlsZahl; // konvertiere zu Zahl
      // Validierung: Menge > 0 aber keine Einheit ausgewählt
      // prüft, ob this.einheit null, 0 oder undefined ist
      if (this.menge > 0 && (!this.einheit || this.einheit === 0)) {
        this.errorMessage = "Bitte wählen Sie eine Einheit aus, wenn eine Menge angegeben ist.";
        return; // abbrechen
      }

      // Validierung: Menge = 0 aber Einheit ausgewählt
      if (this.einheit && (!this.menge || this.menge === 0)) {
        this.errorMessage = "Bitte geben Sie eine Menge an, wenn eine Einheit ausgewählt ist.";
        return; 
      } 
      
     // Validierung: Einheit stück, Menge= Dezimalzahl
      if (this.einheit && this.einheit !== 0) {
        const selectedEinheit = this.einheiten.find(e => e.id === this.einheit);
        if (selectedEinheit && selectedEinheit.name.toLowerCase() === "stück") {
          if (this.menge && !Number.isInteger(this.menge)) {
            this.errorMessage = "Für die Einheit 'Stück' muss die Menge eine ganze Zahl sein.";
            return; 
          }
        }
      }

      let menge = this.menge == null || this.menge == 0 ? 0 : this.menge;
      let einheit_id = menge === 0 ? 0 : this.einheit;

      const daten = {
        produkt_menge: menge,
        einheit_id: einheit_id,
        beschreibung: this.beschreibung,
      };

      try {
        await axios.put(
          `http://141.56.137.83:8000/listen/${this.listenId}/produkte/${this.produkt_id}/nutzer/${this.hinzugefügt_von}`,
          daten
        );
        this.message = "Produkt erfolgreich aktualisiert.";
        this.$router.push(`/list/${this.listenId}`);
      } catch (error) {
        this.errorMessage = error.response?.data?.detail || "Fehler beim Speichern";
      }
    },
    /**
     * Löscht Produkt über API und navigiert zurück zur Liste. 
     */
    async deleteProduct() {
      this.message = "";
      this.errorMessage = "";
      try {
        await axios.request({
          method: "delete",
          url: `http://141.56.137.83:8000/listen/${this.listenId}/produkte/${this.produkt_id}`,
          data: { hinzugefügt_von: this.hinzugefügt_von },
          headers: { "Content-Type": "application/json" },
        });
        this.message = "Produkt erfolgreich gelöscht.";
        this.$router.push(`/list/${this.listenId}`);
      } catch (error) {
        this.errorMessage = error.response?.data?.detail || "Fehler beim Löschen.";
      }
    },
  },
};
</script>

<style scoped>
.wrapper {
  padding-top: 4em;
}

.product-detail {
  min-width: 250px;
  max-width: 720px;
  padding: 1rem 1.3rem;
  background-color: var(--box-bg-color);
  border-radius: 8px;
  align-items: center;
  box-shadow: 0 4px 12px var(--box-shadow-color);
}

.product-name {
  font-weight: 700;
  font-size: 2em;
  text-align: center;
  justify-content: center;
  margin-bottom: 0.5em;
  word-break: break-word;
  word-wrap: break-word;  
  width: 100%;
}

form div {
  align-items: left;
  gap: 0;
}

form label {
  text-align: center;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 1.25rem;
}

label {
  font-weight: 600;
  margin-bottom: 0.35rem;
}

textarea {
  min-height: 80px;
}

.button-row {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
  width: 100%;
}

input,
textarea,
select {
  width: 100%;
}

.success, .error {
  max-width: 210px;
}

button.button-delete,
button.button-submit {
  width: 100%;
}
</style>