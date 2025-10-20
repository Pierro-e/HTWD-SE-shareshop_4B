<template>
  <h1>Einstellungen</h1>

  <div class="info-block">
      <p><strong>Hallo </strong>{{name}}<strong>, du hier Einstellungen zur Ansicht und zum Profil ändern.</strong></p>
      <p>
        <strong>Aktuelle E-Mail:</strong> {{ email }}
      </p>
  </div>

  <div class="appearance-settings">
    <h2>Ansicht</h2>

  <form @submit.prevent="applyAppearance">
    <div class="form-content">
      <div>
        <label for="theme-select">Thema: </label>
        <select id="theme-select" v-model="theme">
          <option>Dunkel</option>
          <option>Hell</option>
          <option>Automatisch</option>
        </select>
      </div>
      <div>
        <label for="accent-select">Akzentfarbe: </label>
        <select id="accent-select" v-model="accent">
          <option style="color: #646cff">Blau</option>
          <option style="color: #c04cff">Lila</option>
          <option style="color: #4ca6a6">Grün</option>
          <option style="color: #b25050">Rot</option>
          <option style="color: #cc5c00">Orange</option>
        </select>
      </div>
    </div>

  <button class="button-submit" type="submit">Änderungen übernehmen</button>
  </form>
  </div>

  <div class="user-settings">
    <h2>Profil</h2>

    <form @submit.prevent="updateUser">
      <div class="form-content">
        <div>
          <label for="name">Neuer Name: </label>
          <input v-model="name" 
              type="name" 
              id="name"            
          />
        </div>
        
        <div>
          <label for="email">Neue E-Mail: </label>
          <input v-model="email" 
              type="email" 
              id="email" 
              required 
          />
        </div>

        <div>
          <label for="password">Neues Passwort: </label>
          <input v-model="password" 
              type="password" 
              id="password"
              />
        </div>
      </div>

      <button class="button-submit" type="submit">Änderungen speichern</button>
    </form>



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
      theme: '',
      accent: '',

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
    this.loadAppearanceData();
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
    async loadAppearanceData() {
      this.theme = localStorage.getItem("theme");
      if (this.theme === null){ // Default setzen
        localStorage.setItem("theme", "Dunkel");
        this.theme = "Dunkel";
      }

      this.accent = localStorage.getItem("accent-color");
       if (this.accent === null){ // Default setzen
        localStorage.setItem("accent-color", "Blau");
        this.accent = "Blau";
      }

    },

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

    async applyAppearance(){
      this.errorMessage = "Thema: " + this.theme + " | Akzent: " + this.accent;
      localStorage.setItem("theme", this.theme);
      localStorage.setItem("accent-color", this.accent);

      document.documentElement.setAttribute("css-theme", this.theme); // Thema setzen
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
    }
  }
};
</script>


<style scoped>
form label {
  width: 101px;
}

.success {  
  max-width: 250px;
}

.info-block {
  background-color: #333;
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 0.5rem;
  color: #ddd;
  font-size: 0.95rem;
}

@media (max-width: 480px) {
  input {
    max-width: 200px;
  }
}
</style>


