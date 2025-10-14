<template>
  <div class="user-settings">
    <h2>Profil bearbeiten</h2>

    <div>
      <button class="button-cancel" @click="$router.push('/listen')">Zurück zu den Listen</button>
    </div>

    <div class="current-user-data">
      <p><strong>Hallo </strong>{{name}}<strong>, du kannst hier deine E-mail, deinen Namen und dein Passwort ändern</strong></p>
      <p><strong>Aktuelle E-Mail:</strong> {{ email }}</p>
      
    </div>

    <form @submit.prevent="updateUser">
      
      <div>
        <label for="name">Neuer Name:</label>
        <input v-model="name" 
            type="name" 
            id="name"            
        />
      </div>
      
      <div>
        <label for="email">Neue E-Mail:</label>
        <input v-model="email" 
            type="email" 
            id="email" 
            required 
        />
      </div>

      <div>
        <label for="password">Neues Passwort:</label>
        <input v-model="password" 
            type="password" 
            id="password"
            />
      </div>

      <button class="button-submit" type="submit">Änderungen speichern</button>
    </form>

    <div>
      <button class="button-submit" @click="logout()">Abmelden</button>
    </div>

    <div v-if="message" class="success">{{ message }}</div>
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserSettings',
  inject: ['user'],
  data() {
    return {
      name: '',
      currentName: '',
      email: '',
      password: '',
      //currentEmail: '',//gebraucht?
      message: '',
      errorMessage: ''
    };
  },


 
  async mounted() {
    // Beim Laden: Werte aus globalem User setzen
    if (this.user?.id) {
      await this.loadUserData()
      //this.name = this.user.name
      //this.email = this.user.email
    }  else {
      // Für Test: User-ID auf 1 setzen und laden
      this.user.id = 1
      await this.loadUserData()
    }
  },

  methods: {

    async loadUserData() {
      try {
        
        const response = await axios.get(`http://141.56.137.83:8000/nutzer/by-id?id=${this.user.id}`)
        
        this.currentEmail = response.data.email
        this.name = response.data.name
        this.currentName = response.data.name
        this.email = response.data.email
      } catch (err) {
        this.errorMessage = 'Fehler beim Laden der Daten'
      }
    },

  async updateUser() {
      
      this.message = ''
      this.errorMessage = ''
      
    try {
      const promises = []

    // Trim, damit Leerzeichen ignoriert werden
    const trimmedName = this.name.trim();
    const trimmedPassword = this.password.trim();

    // Name ändern, wenn anders als vorher
    if (trimmedName !== '') {
      promises.push(
        axios.put(`http://141.56.137.83:8000/nutzer_change/${this.user.id}/name`, {
          neuer_name: trimmedName
        })
      );
    }

     // Passwort ändern, wenn etwas eingegeben wurde
    if (trimmedPassword !=='') {
      promises.push(
        axios.put(`http://141.56.137.83:8000/nutzer_change/${this.user.id}/passwort`, {
          neues_passwort: trimmedPassword
        })
      );
    }

      // Warten, bis alle API-Aufrufe abgeschlossen sind
      await Promise.all(promises);


      this.message = 'Daten erfolgreich aktualisiert!'
        this.errorMessage = ''

        // Optional: globalen Benutzer aktualisieren
        this.user.email = this.email
        this.user.name = trimmedName

        this.password = ''

      } catch (err) {
        this.errorMessage = err.response?.data?.detail || 'Fehler beim Aktualisieren'
        this.message = ''
      }
    },

    logout() {
      // Einfaches Logout: Seite neu laden und User-Daten löschen
      this.user.id = null
      this.user.name = ''
      this.user.email = ''
      this.$router.push(`/`,);    }
  }
};
</script>


<style scoped>
.success {
  color: green;
}

.error {
  color: #ff4c4c;
  margin-top: 0.8rem;
  text-align: center;
  font-weight: 600;
}

.current-user-data {
  background-color: #333;
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 0.5rem;
  color: #ddd;
  font-size: 0.95rem;
}
</style>


