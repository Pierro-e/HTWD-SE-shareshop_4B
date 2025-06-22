<template>
  <div class="liste">
    <div class="header">
      <button 
        :disabled="showpopup_product || showpopup_list" 
        @click="$router.push('/listen')" 
        class="button button-cancel back-button">Zurück</button>

      <h2>{{ list_name }}</h2>

      <button 
        :disabled="showpopup_product || showpopup_list" 
        @click="openProductPopup()" 
        class="button button-add">+</button>

      <div class="settings-container">
        <button 
          :disabled="showpopup_product || showpopup_list" 
          @click="openListPopup()" 
          class="button button-settings">Listeneininformationen</button>
      </div>
    </div>

    <div v-if="showpopup_list" class="popup-overlay">
      <div class="popup-content">
        <h3>Listeninformationen</h3>
        <p>Name der Liste: {{ list_name }}</p>
        <p>Ersteller: {{ list_creator_name }}</p>
        <p>Mitglieder:</p>
          <div v-for="(mitglied, index) in mitglieder_names" :key="index" class="mitglieder-anzeige">
            {{ mitglied }}
          </div>
        <button @click="showpopup_list = false" class="button button-cancel">Schließen</button>
      </div>
    </div>   

    <div v-if="showpopup_product" class="popup-overlay">
      <div class="popup-content">
        <h3>Neues Produkt hinzufügen</h3>
        <input class="input-product"
          v-model="new_product"
          type="text"
          placeholder="Produktname"
          maxlength="30">
        <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
        <button @click="cancel_product_popup" class="button button-cancel">Abbrechen</button>
        <button @click="add_product" class="button button-add">Hinzufügen</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { inject } from 'vue'

export default {
  name: 'Liste',
  inject: ['user', 'getUser'],
  props: ['list_id'],
  data() {
    return {
      list_name: '',
      list_creator_id: null,
      list_creator_name: '',
      errorMessage: '',
      showpopup_product: false,
      showpopup_list: false,
      new_product: '',
      listenprodukte: [],
      mitglieder: [],
      mitglieder_names: [],
      userData: null,   // hier speichern wir den injecteten user
    }
  },

  methods: {
    async get_list(id) {
      this.errorMessage = '';
      try {
        const response = await axios.get(`http://141.56.137.83:8000/listen/by-id/${id}`);
        this.list_name = response.data.name;
        this.list_creator_id = response.data.ersteller;

        const creator = await this.getUser(this.list_creator_id);
        this.list_creator_name = creator.name || 'Unbekannt';

      } catch (error) {
        if (error.response && error.response.data && error.response.data.detail) {
          this.errorMessage = error.response.data.detail;
        } else {
          this.errorMessage = 'Fehler beim Laden der Liste';
        }
      }
    },

    async get_list_members(id) {
      this.errorMessage = ''
      try {
        const response = await axios.get(`http://141.56.137.83:8000/listen/${id}/mitglieder`)
        this.mitglieder = response.data

        this.mitglieder_names = await Promise.all(
          this.mitglieder.map(async (mitglied) => {
            const user = await this.getUser(mitglied.nutzer_id);
            return user.name || 'Unbekannt';
          })
        );

      }catch (error) {
        if (error.response && error.response.data && error.response.data.detail) {
          this.errorMessage = error.response.data.detail
        } else {
          this.errorMessage = 'Fehler beim Laden der Mitglieder'
        }
      }
    },

    openListPopup() {
      this.errorMessage = '';
      this.showpopup_list = true;
      this.showpopup_product = false;
      this.get_list_members(this.list_id);
    },
    
    openProductPopup() {
      this.errorMessage = '';
      this.showpopup_product = true;
      this.showpopup_list = false;
    },

    async add_product() {
      const list_id = this.list_id || this.$route.params.id;
      const user_id = this.user.id;

      this.errorMessage = '';

      if (this.new_product.trim() === '') {
        this.errorMessage = 'Produktname darf nicht leer sein';
        return;
      }

      let produkt_Id;

      try {
        // Produkt existiert schon?
        const responseCheck = await axios.get(`http://141.56.137.83:8000/produkte/by-name/${encodeURIComponent(this.new_product.trim())}`);
        produkt_Id = responseCheck.data.id;
      } catch (error) {
        // Wenn 404 (Produkt nicht gefunden), dann neu anlegen
        if (error.response && error.response.status === 404) {
          try {
            const responseCreate = await axios.post(`http://141.56.137.83:8000/produkte_create`, {
              name: this.new_product.trim()
            });
            produkt_Id = responseCreate.data.id;
          } catch (error) {
            if (error.response && error.response.data && error.response.data.detail) {
              this.errorMessage = error.response.data.detail
            } else {
            this.errorMessage = 'Fehler beim Anlegen des Produkts';
            return;
            }
          }
        }
      }

      if (!list_id || !produkt_Id || !user_id) {
        console.log('Fehlende Liste-, Produkt- oder Nutzer-ID');
        return;
      }

      try {
        await axios.post(`http://141.56.137.83:8000/listen/${list_id}/produkte/${produkt_Id}/nutzer/${user_id}`);
        this.showpopup_product = false;
        this.errorMessage = '';
        this.new_product = '';
      } catch (error) {
        if (error.response) {
          this.errorMessage = error.response.data.detail || 'Unbekannter Fehler beim Hinzufügen des Produkts zur Liste';
        }
      }
    },
    
    cancel_product_popup() {
      this.errorMessage = '';
      this.showpopup_product = false;
      this.new_product = ''; 
    },

  },

  mounted() {
    this.errorMessage = '';
    const id = this.list_id || this.$route.params.id
    this.get_list(id)
    this.get_list_members(id)

    // Injected user in data speichern
    this.userData = this.user;
  },
}
</script>

<style scoped>
.liste {
  padding: 10px 20px;
}

/* Header fixiert oben */
.header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 60px;
  background-color: black;
  z-index: 1100;
  padding: 10px 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 5px rgba(0,0,0,0.3);
  box-sizing: border-box;
  gap: 1rem;
} 

/* Überschrift zentriert */
.header h2 {
  margin: 0;
  font-weight: 400;
  font-size: 1.5rem;
  color: inherit;
  text-align: center;
  flex-grow: 1;
}

.settings-container {
  position: fixed;
  top: 60px; 
  right: 25px;
  left: 70px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.input-product {
  width: 100%;
  padding: 0.5em;
  border-radius: 0.25em;
  border: none;
  background-color: #3a3a3a;
  color: white;
  font-size: 1em;
  box-sizing: border-box;
}

.popup-overlay {
  position: fixed;
  top: 0; left: 0; width: 100vw; height: 100vh;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  /* verhindert Klicks auf darunter liegende Elemente */
  pointer-events: auto;
}

.popup-content {
  background: black;
  color: white;
  padding: 1em 2em;
  border-radius: 0.5em;
  min-width: 300px;
  text-align: center;
  /* Klicks nur auf das Popup zulassen */
  pointer-events: auto;
}

/* Buttons außerhalb Popup (z.B. header) deaktivieren wenn Popup offen */
.button[disabled] {
  cursor: not-allowed;
  opacity: 0.6;
}
</style>
