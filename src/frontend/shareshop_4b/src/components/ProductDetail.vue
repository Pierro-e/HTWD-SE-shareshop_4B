<template>
  <div class="product-detail">
    <button class="button-cancel" @click="$router.push(`/list/${listenId}`)">abbrechen</button>

    <h2 class="product-name">{{ name }}</h2>

    <form @submit.prevent="saveProduct">
      <div class="form-group">
        <label for="beschreibung">Beschreibung:</label>
        <textarea id="beschreibung" v-model="beschreibung"></textarea>
      </div>

      <div class="form-group">
        <label for="menge">Menge:</label>
        <input id="menge" type="number" step="0.01" min="0" v-model.number="menge" />
      </div>

      <div class="form-group">
        <label for="einheit">Einheit:</label>
        <select id="einheit" v-model="einheit">
          <option disabled value="">Bitte wählen</option>
          <option v-for="e in einheiten" :key="e.id" :value="e.id">{{ e.name }}</option>
        </select>
      </div>

      <div class="button-row">
        <button type="button" class="button-delete" @click="deleteProduct">Löschen</button>
        <button type="submit" class="button-submit">Speichern</button>
      </div>
    </form>

    <div v-if="message" class="success">{{ message }}</div>
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: ["produktId", "listenId", "nutzerId"],
  data() {
    return {
      produkt_id: null,
      name: "",
      beschreibung: "",
      menge: "",
      einheit: "",
      hinzugefügt_von: null,
      einheiten: [],
      errorMessage: "",
      message: "",
    };
  },
  async mounted() {
    this.hinzugefügt_von = this.nutzerId;
    await this.fetchEinheiten();
    await this.fetchProduct();
    await this.fetchProduktName();
  },
  methods: {
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
        this.menge = produkt.produkt_menge || "";
        this.einheit = produkt.einheit_id || "";
        this.beschreibung = produkt.beschreibung || "";
      } catch (error) {
        this.errorMessage = error.response?.data?.detail || "Fehler beim Laden des Produkts.";
      }
    },
    async fetchEinheiten() {
      try {
        const response = await axios.get(`http://141.56.137.83:8000/einheiten`);
        this.einheiten = response.data;
      } catch {
        this.errorMessage = "Einheiten konnten nicht geladen werden.";
      }
    },
    async fetchProduktName() {
      try {
        const response = await axios.get(
          `http://141.56.137.83:8000/produkte/by-id/${this.produkt_id}`
        );
        this.name = response.data.name;
      } catch {
        console.warn("Name konnte nicht geladen werden.");
      }
    },
    async saveProduct() {
      this.message = "";
      this.errorMessage = "";

      // Validierung: Menge > 0 aber keine Einheit ausgewählt
      if (this.menge > 0 && (!this.einheit || this.einheit === "" || this.einheit === 0)) {
        this.errorMessage = "Bitte wählen Sie eine Einheit aus, wenn eine Menge angegeben ist.";
        return; // abbrechen
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
.product-detail {
  min-width: 300px;
  max-width: 720px;
  margin: 2rem auto;
  padding: 2rem 2.5rem;
  background-color: #2a2a2a;
  border-radius: 8px;
  color: #eee;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.product-name {
  font-weight: 700;
  font-size: 2rem;
  margin-bottom: 2rem;
  text-align: center;
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
  color: #ccc;
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
  width: 125%
}

.success, .error {
  max-width: 250px;
}

@media (max-width: 480px) {
  .product-detail {
    padding: 1rem 1.2rem;
  }

  .button-row {
    flex-direction: column;
    gap: 0.8rem;
  }

  button.button-delete,
  button.button-submit {
    min-width: auto;
    width: 100%;
  }
}
</style>
