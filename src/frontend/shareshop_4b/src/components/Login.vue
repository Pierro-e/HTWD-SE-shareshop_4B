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
          placeholder="Email"
          required
        />
      </div>
      <div class="login_pw">
        <label for="password" class="login_block">Passwort: </label>
        <input
          v-model="password"
          type="password"
          id="password"
          maxlength="30"
          placeholder="Passwort"
          required
        />
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
  data() {
    return {
      email: "",
      password: "",
      errorMessage: "",
    };
  },
  inject: ["setUser"], // setUser aus app.vue injizieren
  methods: {
    async onSubmit() {
      this.errorMessage = "";
      try {
        const response = await axios.post("http://141.56.137.83:8000/login", {
          email: this.email,
          passwort: this.password,
        });
        this.setUser(response.data); // Benutzerdaten setzen
        this.$router.push("/listen"); // Einkaufslisten des Nutzers aufrufen
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
      }
    },
  },
};
</script>

<style scoped>
.login_container {
  max-width: 400px;
  margin: 3em auto;
  padding: 2em;
  background-color: #2a2a2a;
  border-radius: 0.75em;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  color: inherit;
  font-size: 1.1rem;
  text-align: left;
}

h2 {
  margin-top: 0;
  margin-bottom: 1.2em;
  font-weight: 600;
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

.login_block {
  margin-bottom: 0.4em;
  font-weight: 500;
}

.error {
  margin-top: 1em;
  font-weight: 600;
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
