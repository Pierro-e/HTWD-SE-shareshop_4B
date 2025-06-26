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
        <p>Ersteller: {{ list_creator }}</p>
        <ul>
          <li v-for="mitglied in mitglieder" :key="mitglied.id">
            Mitglied: {{ mitglied.name }} (ID: {{ mitglied.id }})
          </li>
        </ul>
        <button @click="showpopup_list = false" class="button button-cancel">Schließen</button>
      </div>
    </div>

    <div v-if="showpopup_product" class="popup-overlay">
      <div class="popup-content">
        <h3>Neues Produkt hinzufügen</h3>
        <button @click="showpopup_product = false" class="button button-cancel">Abbrechen</button>
        <button @click="showpopup_product = false" class="button button-add">Hinzufügen</button>
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
      list_creator: '',
      errorMessage: '',
      showpopup_product: false,
      showpopup_list: false,
      listenprodukte: [],
      mitglieder: [],
      mitglieder_ids: [],
    }
  },

  methods: {
  async get_list(id) {
    this.errorMessage = '';
    try {
      const response = await axios.get(`http://141.56.137.83:8000/listen/by-id/${id}`);
      this.list_name = response.data.name;
      const creator_id = response.data.ersteller;

      // getUser ist injected, also this.getUser()
      const creator = await this.getUser(creator_id);

      // creator ist schon response.data aus App.vue getUser()
      this.list_creator = creator ? creator.name : 'Unbekannt';

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
        const response = await axios.get(`http:///listen/${id}/mitglieder`)
        this.mitglieder = response.data
        this.mitglieder_ids = this.mitglieder.map(member => member.id)
      }catch (error) {
        if (error.response && error.response.data && error.response.data.detail) {
          this.errorMessage = error.response.data.detail
        } else {
          this.errorMessage = 'Fehler beim Laden der Mitglieder'
        }
      }
    },

    openListPopup() {
      this.showpopup_list = true;
      this.showpopup_product = false;
      this.get_list_members(this.list_id);
    },

    openProductPopup() {
      this.showpopup_product = true;
      this.showpopup_list = false;
    },
  },

  mounted() {
    const id = this.list_id || this.$route.params.id
    this.get_list(id)
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
