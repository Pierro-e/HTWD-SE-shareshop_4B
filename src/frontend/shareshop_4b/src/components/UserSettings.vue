<template>
  <div class="settings">
    <AppHeader :title="String('Einstellungen')">
      <template #left>
        <button class="button-cancel" @click="$router.push('/listen')">
          <font-awesome-icon icon='arrow-left'/>
        </button>
      </template>

      <template #right>
      </template>

    </AppHeader>

    <div class="info-block">
      <div v-if="loadingActive" class="loading">Laden...</div>
      <p v-if="!loadingActive">
        <strong>Hallo </strong>{{name}}<strong>, du kannst hier Einstellungen zur Ansicht, Produktvorschlägen und zum Profil ändern.</strong>
      </p>
      <p v-if="!loadingActive">
        <strong>Aktuelle E-Mail:</strong> {{ email }}
      </p>
    </div>

    <details>
      <summary>
        <div class="summary-title">Ansicht</div>
      </summary>
      <div class="appearance-settings">
        <form @submit.prevent="applyAppearance">
          <div class="form-content">
            <div>
              <label for="theme-select">Thema: </label>
              <select id="theme-select" v-model="theme">
                <option>Automatisch</option>
                <option>Dunkel</option>
                <option>Hell</option>
              </select>
            </div>
            <div>
              <label for="accent-select">Akzent&shy;farbe: </label>
              <select id="accent-select" v-model="accent">
                <option style="color: #646cff">Blau</option>
                <option style="color: #9d60ff">Lila</option>
                <option style="color: #4ca6a6">Grün</option>
                <option style="color: #b25050">Rot</option>
                <option style="color: #ca7631">Orange</option>
              </select>
            </div>
          </div>

          <button class="button-submit" type="submit">Änderungen speichern</button>
        </form>
      </div>
    </details>
   
    <details>
      <summary>
        <div class="summary-title">Produktvorschläge</div>
      </summary>
      <div class="profile-settings">
        <form @submit.prevent="applyDecayDays">  
          <div class="form-content">
            <div>
              <label for="decay-days">Verfalls&shy;zeitraum (Tage): </label>
              <input v-model.number="decaydays" 
                    type="number"
                    id="decay-days" 
                    min="0" 
                    step="1"
                    required
              />
            </div>
          </div>
          <button class="button-submit" type="submit">Änderungen speichern</button>
        </form>
      </div> 
    </details>

    <details>
      <summary>
        <div class="summary-title">Profil</div>
      </summary>
      <div class="user-settings">
        <form @submit.prevent="updateUser">
          <div class="form-content">
            <div>
              <label for="name">Name: </label>
              <input v-model="name" 
                  type="name" 
                  id="name"            
              />
            </div>
            
            <div>
              <label for="email">E-Mail: </label>
              <input v-model="email" 
                  type="email" 
                  id="email" 
                  required 
              />
            </div>
            <div>
              <label for="password">Passwort: </label>
              <input v-model="password" 
                  type="password" 
                  id="password"
                  />
            </div>
          </div>
          <button class="button-submit" type="submit">Änderungen speichern</button>
        </form>
      </div>
    </details>

      <div>
        <button @click="logout()">Abmelden</button>
      </div>

      <div v-if="message" class="success">{{ message }}</div>
      <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
  </div>
  <BottomBar 
    :highlight-btn="4"
  />
</template>

<script>
import AppHeader from "./AppHeader.vue";
import axios from 'axios'
import BottomBar from "./BottomBar.vue";

export default {
  name: 'UserSettings',
  inject: ['user', 'deleteUser', 'getThemeText', 'getAccentText'],
  components: {
    AppHeader,
    BottomBar
  },
  data() {
    return {
      theme: '',
      accent: '',

      name: '',
      currentName: '',
      currentEmail: '',
      email: '',
      password: '',
      decaydays: 0,
      message: '',

      errorMessage: '',
      loadingActive: true
    };
  },

  async mounted() {
    this.loadAppearanceData();
    // Beim Laden: Werte aus globalem User setzen
    if (this.user?.id) {
      await this.loadUserData()
    }
  },

  methods: {
    async loadAppearanceData() {
      // Theme laden
      this.theme = this.getThemeText(this.user.theme)
      document.documentElement.setAttribute('css-theme', this.theme) // Thema setzen

      // Akzentfarbe laden
      this.accent = this.getAccentText(this.user.color)
      document.documentElement.setAttribute('css-accent', this.accent) // Farbe setzen

    },

    async loadUserData() {
      try {
        const response = await axios.get(`http://141.56.137.83:8000/nutzer/by-id?id=${this.user.id}`)
        this.currentEmail = response.data.email
        this.name = response.data.name
        this.currentName = response.data.name
        this.email = response.data.email
        this.decaydays = Math.trunc(response.data.decaydays);
      }  catch (error) {
        if (
          error.response &&
          error.response.data &&
          error.response.data.detail
        ) {
          this.errorMessage = error.response.data.detail;
        } else {
          this.errorMessage = "Fehler beim Laden der Daten";
        }
      }
      this.loadingActive = false;
    },

    async applyAppearance(){
       try {
          await axios.put(`http://141.56.137.83:8000/nutzer_change/${this.user.id}/theme_color`, {
            theme: this.getThemeNumber(this.theme),
            color: this.getAccentNumber(this.accent)
          })
      } catch(error) {
        if (
          error.response &&
          error.response.data &&
          error.response.data.detail
        ) {
          this.errorMessage = error.response.data.detail;
        } else {
          this.errorMessage = "Konnte Ansicht nicht hochladen!";
        }
      }

      // localStorage User aktualisieren
      this.user.theme = this.getThemeNumber(this.theme)
      this.user.color = this.getAccentNumber(this.accent)
      localStorage.setItem('user', JSON.stringify(this.user)) 

      document.documentElement.setAttribute("css-theme", this.theme); // Thema setzen
      document.documentElement.setAttribute("css-accent", this.accent); // Farbe setzen
    },

    // Integerwert als Farbe interpretieren
    getAccentNumber(userAccent) {
      switch (userAccent){
        case "Blau": return 0;
        case "Lila": return 1;
        case "Grün": return 2; 
        case "Rot": return 3;
        case "Orange": return 4;
        default: return 0 // Default setzen
      }
    },

    getThemeNumber(userTheme) {
      switch (userTheme){
        case "Automatisch": return 0;
        case "Dunkel": return 1;
        case "Hell": return 2;
        default: return 0 // Default setzen
      }
    },

    async applyDecayDays(){
       try {
          await axios.put(`http://141.56.137.83:8000/nutzer_change/${this.user.id}/decaydays`, {
            neue_decaydays: this.decaydays
          })
      } catch(error) {
        if (
          error.response &&
          error.response.data &&
          error.response.data.detail
        ) {
          this.errorMessage = error.response.data.detail;
        } else {
          this.errorMessage = "Konnte Verfallszeitraum nicht hochladen!";
        }
      }
    },

    async updateUser() {
      this.message = ''
      this.errorMessage = ''

      try {
        const promises = []
        const trimmedName = this.name.trim()
        const trimmedEmail = this.email.trim()
        const trimmedPassword = this.password.trim()

        // Name ändern
        if (trimmedName !== '' && trimmedName !== this.currentName) {
          promises.push(
            axios.put(`http://141.56.137.83:8000/nutzer_change/${this.user.id}/name`, {
              neuer_name: trimmedName
            })
          )
        }

        // Email ändern
        if (trimmedEmail !== '' && trimmedEmail !== this.currentEmail) {
          promises.push(
            axios.put(`http://141.56.137.83:8000/nutzer_change/${this.user.id}/email`, {
              neue_email: trimmedEmail
            })
          )
        }

        // Passwort ändern
        if (trimmedPassword !== '') {
          promises.push(
            axios.put(`http://141.56.137.83:8000/nutzer_change/${this.user.id}/passwort`, {
              neues_passwort: trimmedPassword
            })
          )
        }

      // Warten, bis alle API-Aufrufe abgeschlossen sind
      await Promise.all(promises);

        this.message = 'Daten erfolgreich aktualisiert!'
        this.errorMessage = ''
        this.user.email = this.email
        this.user.name = trimmedName
        this.password = ''
      } catch (err) {
        this.errorMessage = err.response?.data?.detail || 'Fehler beim Aktualisieren'
        this.message = ''
      }
      this.loadUserData();
    },

    logout() {
      this.deleteUser()
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
details {
  padding: 1em;
  background-color: var(--box-bg-color);
  border-radius: 0.5em;
  margin-bottom: 1em;
  transition: all 0.3s ease-in-out;
  max-height: 50px;
  overflow: hidden;
}

details[open] summary::before {
  transform: rotate(90deg);
}

details[open] summary {
  padding-bottom: 1em;
}

details[open] {
  margin-top: 1em;
  max-height: 500px;
}

.summary-title {
  font-size: larger;
  font-weight: bold;
}

summary {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-size: larger;
}

/* kein nativer Marker */
summary::-webkit-details-marker {
  display: none;
}

summary::before {
  content: "▶";
  transition: transform .2s ease;
}

.settings {
  margin-top: 70px;
}

form label {
  width: 100px;
}

.success {  
  max-width: 75%;
}

.info-block {
  background-color: var(--box-bg-color);
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 0.5rem;
  font-size: 0.95rem;
}

@media (max-width: 480px) {
  form label {
    width: 60px;
  }
}
</style>


