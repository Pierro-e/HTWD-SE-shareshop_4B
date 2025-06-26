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
          <option v-for="e in einheiten" :key="e.id" :value="e.id">
            {{ e.name }}
          </option>
        </select>
      </div>

      <button class="button-submit" type="submit">Speichern</button>
      <button class="button-delete" type="button" @click="deleteProduct">Löschen</button>
    </form>

    <div v-if="message" class="success">{{ message }}</div>
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
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
    this.hinzugefügt_von = this.nutzerId;
    
    await this.fetchEinheiten();
    await this.fetchProduct();
    await this.fetchProduktName();
  },

  methods: {

   

    async fetchProduct() {
      try {
        const response = await axios.get(`http://141.56.137.83:8000/listen/${this.listenId}/produkte`);
        const produkte = response.data;
        
        // Nur das eine Produkt herausfiltern:
        const produkt = produkte.find(p =>
          p.produkt_id === parseInt(this.produktId) &&
          p.hinzugefügt_von === parseInt(this.nutzerId)
        );

        if (!produkt) {
          this.errorMessage = 'Produkt in dieser Liste nicht gefunden.';
          return;
        }

        this.produkt_id = produkt.produkt_id;
        this.menge = produkt.produkt_menge || '';
        this.einheit = produkt.einheit_id || '';
        this.beschreibung = produkt.beschreibung || '';
        
      } catch (error) {
        this.errorMessage = error.response?.data?.detail || 'Fehler beim Laden des Produkts.';
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

    async fetchProduktName() {
      try {
        const response = await axios.get(`http://141.56.137.83:8000/produkte/by-id/${this.produkt_id}`);
        this.name = response.data.name;
      } catch (error) {
        console.warn('Name konnte nicht geladen werden.');
      }
    },

    async saveProduct() {

      this.message = ''
      this.errorMessage = ''
      
      try {
        await axios.put(`http://141.56.137.83:8000/listen/${this.listenId}/produkte/${this.produkt_id}/nutzer/${this.hinzugefügt_von}`, {
          produkt_menge: this.menge,
          einheit_id: this.einheit,  
          beschreibung: this.beschreibung
        });
        alert('Produkt gespeichert!');
        this.message = 'Produkt erfolgreich aktualisiert.'
        this.$router.push(`/list/${this.listenId}`);
      } catch (error) {
        this.errorMessage = error.response?.data?.detail ||'Fehler beim Speichern.';
      }
    },

    async deleteProduct() {
      if (!confirm('Möchtest du dieses Produkt wirklich löschen?')) {
        return; // Abgebrochen
       }

      this.message = '';
      this.errorMessage = '';

      try {
        console.log("DeleteRequest:", {
        hinzugefügt_von: this.hinzugefügt_von,
        listen_id: this.listenId,
        produkt_id: this.produkt_id
        });
        await axios.request({
        method: 'delete',
        url: `http://141.56.137.83:8000/listen/${this.listenId}/produkte/${this.produkt_id}`,
        data: {
          hinzugefügt_von: this.hinzugefügt_von
        },
        
        headers: {
        'Content-Type': 'application/json'
        }
        
      });
      
      this.message = 'Produkt erfolgreich gelöscht.';
      this.$router.push(`/list/${this.listenId}`);
      } catch (error) {
        
        this.errorMessage = error.response?.data?.detail || 'Fehler beim Löschen.';
       
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