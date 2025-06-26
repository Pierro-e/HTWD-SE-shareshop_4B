<template>
  <div class="product-detail">
    <h2> Produkt {{name}} bearbeiten</h2>
   
    <form @submit.prevent="saveProduct">
      <div>
        <label for="name">Name:</label>
        <input id="name" v-model="name" required />
      </div>
 
      <div>
        <label for="beschreibung">Beschreibung:</label>
        <textarea id="beschreibung" v-model="beschreibung"></textarea>
      </div>

      <div>
        <label for="menge">Menge:</label>
        <input id="menge" type="number" v-model.number="menge" required />
      </div>

      <div>
        <label for="einheit">Einheit:</label>
        <select id="einheit" v-model="einheit" required>
          <option disabled value="">Bitte wählen</option>
          <option v-for="e in einheiten" :key="e.id" :value="e.name">
            {{ e.name }}
          </option>
        </select>
      </div>

      <button class="button-submit" type="submit">Speichern</button>
      <button class="button-delete" type="button" @click="deleteProduct">Löschen</button>
    </form>

    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ProductDetail',
  props: ['produktId', 'listenId', 'nutzerId'], //  direkt aus der Route

  data() {
    return {
      produkt_id: null,
      name: '',
      beschreibung: '',
      menge: '',
      einheit: '',
      hinzugefügt_von: null,

      einheiten: [],
      errorMessage: '',
    };
  },

  async mounted() {
     console.log('Props:', this.produktId, this.listenId, this.nutzerId);
  await this.fetchEinheiten();
  await this.fetchProduct();
  },

  methods: {
    async fetchProduct() {
      try {
        const response = await axios.get(`http://141.56.137.83:8000/produkte/by-id/${this.produktId}`);
        const produkt = response.data;

        this.produkt_id = produkt.id;
        this.name = produkt.name;
        this.beschreibung = produkt.beschreibung || '';
        this.menge = produkt.menge || 1;
        this.einheit = produkt.einheit || '';
        this.hinzugefügt_von = produkt.hinzugefügt_von;
      } catch (error) {
        this.errorMessage = error.response?.data?.detail || 'Ein unbekannter Fehler ist aufgetreten.';
      }
    },

    async fetchEinheiten() {
      try {
        const response = await axios.get(`http://141.56.137.83:8000/einheiten`);
        this.einheiten = response.data;
        console.log('Einheiten geladen:', response.data);
      } catch (error) {
        this.errorMessage = 'Einheiten konnten nicht geladen werden.';
      }
    },

    async saveProduct() {
      try {
        await axios.put(`http://141.56.137.83:8000/lists/${this.listenId}/products/${this.produkt_id}/user/${this.hinzugefügt_von}`, {
          id: this.produkt_id,
          name: this.name,
          beschreibung: this.beschreibung,
          menge: this.menge,
          einheit: this.einheit,
          hinzugefügt_von: this.hinzugefügt_von,
        });
        alert('Produkt gespeichert!');
      } catch (error) {
        this.errorMessage = 'Fehler beim Speichern.';
      }
    },

    async deleteProduct() {
      try {
        await axios.delete(`/api/lists/${this.listenId}/products/${this.produkt_id}/user/${this.hinzugefügt_von}`);
        this.$router.push(`/listen/${this.listenId}`);
      } catch (error) {
        this.errorMessage = 'Fehler beim Löschen.';
      }
    },

    product_settings(produkt) {
      this.errorMessage = '';
      this.$router.push(`/listen/${this.listenId}/produkte/${produkt.produkt_id}/nutzer/${produkt.hinzugefügt_von}`);
    },
  },
};
</script>


<style scoped>
.product-detail {
  max-width: 600px;
  margin: auto;
}
.error {
  color: red;
}
</style>