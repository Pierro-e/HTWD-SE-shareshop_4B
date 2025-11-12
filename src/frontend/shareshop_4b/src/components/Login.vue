<template>
  <div class="login_container">
    <h2>Login</h2>
    <form @submit.prevent="onSubmit">
      <div class="login_email">
        <label for="email" class="login_block">E-Mail: </label>
        <input
          v-model="email"
          type="email"
          id="email"
          placeholder="E-Mail"
          required
        />
      </div>
      <div class="login_pw">
        <label for="password" class="login_block">Passwort: </label>
        <div class="password-input-container">
        <input
          v-model="password"
          :type="passwordFieldType" 
          id="password"
          maxlength="30"
          placeholder="Passwort"
          required
        />
        <span class="password-toggle-icon" @click="togglePasswordVisibility">
          {{ passwordFieldType === 'password' ? '👁️' : '🕳️' }}
        </span>
      </div>  
      </div>
      <button class="button-submit" type="submit">Einloggen</button>
    </form>
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
  </div>
  <div class="create_account">
    <p>Du hast noch keinen Account?</p>
    <button class="button-add" @click="$router.push('/registrieren')">
      Registrieren
    </button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Login",
  inject: ["setUser", 'getThemeText', 'getAccentText', 'deleteUser'], // theme, accent, setUser aus app.vue injizieren
  data() {
    return {
      email: "",
      password: "",
      errorMessage: "",
      passwordFieldType: "password",
      theme: '',
      accent: ''
    };
  },
  methods: {
    togglePasswordVisibility() {
      this.passwordFieldType =
        this.passwordFieldType === "password" ? "text" : "password";
    },
    async onSubmit() {
      this.errorMessage = "";
      let response;
      try {
        response = await axios.post("http://141.56.137.83:8000/login", {
          email: this.email,
          passwort: this.password,
        });
      } catch (error) {
        if (
          error.response &&
          error.response.data &&
          error.response.data.detail
        ) {
          this.errorMessage = error.response.data.detail;
        } else {
          this.errorMessage = "Falsche Zugangsdaten";
        }
        return
      }
      this.setUser(response.data); // Benutzerdaten setzen

      // Theme setzen
      const json = response.data
      this.theme = this.getThemeText(json.theme)
      this.accent = this.getAccentText(json.color)

      document.documentElement.setAttribute("css-theme", this.theme) // Thema setzen
      document.documentElement.setAttribute('css-accent', this.accent) // Farbe setzen

      this.$router.push("/listen"); // Einkaufslisten des Nutzers aufrufen
    },
  },
  mounted() {
    this.deleteUser() // Vor dem Login sicherstellen, dass kein User eingeloggt ist
  },
};
</script>

<style scoped>
.login_container {
  min-width: 200px;
  max-width: 400px;
  margin: 3em auto;
  padding: 2em;
  background-color: var(--box-bg-color);
  border-radius: 0.75em;
  box-shadow: 0 4px 12px var(--box-shadow-color);
  color: inherit;
  font-size: 1.1rem;
  text-align: left;
}

h2 {
  margin-top: 0;
  margin-bottom: 1.2em;
  font-weight: 600;
  font-size: 26.4px;
}

form {
  display: flex;
  flex-direction: column;
  gap: 1.2em;
}

form div {
  gap: 0;
}

form label {
  width: auto;
}

.login_email,
.login_pw {
  display: flex;
  flex-direction: column;
}
.password-input-container {
  position: relative;
  display: flex;
  align-items: center;
}
.password-toggle-icon {
  position: absolute;
  right: 10px;
  cursor: pointer;
  user-select: none;
  font-size: 1.2em;
}
/* falls passwörter lange sind */
.password-input-container input {
    width: 100%;
    padding-right: 2.5em; /* Platz für das Icon */
}


.login_block {
  margin-bottom: 0.4em;
  font-weight: 500;
}

.success, .error {
  width: calc(100% - 2rem);
  margin-bottom: 0;
}

.create_account {
  text-align: center;
  margin-top: 2em;
  color: inherit;
}

.create_account p {
  margin-bottom: 0.5em;
  font-size: 1rem;
}
</style>
