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

/* unnötig, schon in style.css definiert!
.button-cancel {
  align-self: center;
  background-color: #6c757d;
  color: #f0f0f0;
  border: none;
  padding: 0.5rem 1.5rem;
  font-weight: 600;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.5);
  min-width: 120px;
}

.button-cancel:hover,
.button-cancel:focus {
  background-color: #565e64;
}

button.button-delete,
button.button-submit {
  flex: 1;
  font-size: 1.1rem;
  padding: 0.6rem 0;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 600;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.5);
  color: #eee;
  user-select: none;
  min-width: 140px;
  transition: background-color 0.3s ease;
}

button.button-submit {
  background-color: #3399ff;
}

button.button-submit:hover,
button.button-submit:focus {
  background-color: #1a73e8;
}

button.button-delete {
  background-color: #e55353;
}

button.button-delete:hover,
button.button-delete:focus {
  background-color: #b02a2a;
}

input[type="number"],
textarea,
select {
  padding: 0.5rem 0.75rem;
  font-size: 1rem;
  border: 1.5px solid #444;
  border-radius: 5px;
  background-color: #222;
  color: #eee;
  font-family: inherit;
  resize: vertical;
  transition: border-color 0.3s ease;
}

input[type="number"]:focus,
textarea:focus,
select:focus {
  border-color: #3399ff;
  outline: none;
  box-shadow: 0 0 8px #3399ff88;
}
  */

input,
textarea,
select {
  width: 125%
}

.success,
.error {
  margin-top: 1.5rem;
  padding: 0.8rem 1rem;
  border-radius: 5px;
  font-weight: 600;
  text-align: center;
  width: 100%;
}

.success {
  background-color: #264d26;
  border: 1.5px solid #4caf50;
  color: #c8facc;
}

.error {
  background-color: #4d2626;
  border: 1.5px solid #e55353;
  color: #f9c8c8;
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
