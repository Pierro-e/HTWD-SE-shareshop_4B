<template>
    <div class="create_account-container">
        <div class="register-header">
            <button class="button-cancel" @click="$router.push('/')">Zurück</button>
            <h1>Registrieren</h1>
        </div>
        <form @submit.prevent="onSubmit">
            <div class="create_email">
                <label for="email" class="create_block">E-Mail: </label>
                <input
                    v-model="email"
                    type="email"
                    id="email"
                    placeholder="E-Mail"
                    required
                >
            </div>
            <div class="create_name">
                <label for="name" class="create_block">Vorname: </label>
                <input
                    v-model="name"
                    type="text"
                    id="name"
                    placeholder="Name"
                    required
                >
            </div>
            <div class="create_pw">
                <label for="password" class="create_block">Passwort: </label>
                <input
                    v-model="password"
                    type="password"
                    id="password"
                    maxlength="30"
                    placeholder="Passwort"
                    required
                >
            </div>
            <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
            <button class="button-submit" type="submit">Account erstellen</button>
        </form>
    </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CreateAccount',
  data() {
    return {
      email: '',
      name: '',
      password: '',
      errorMessage: ''
    }
  },
  methods: {
    async onSubmit() {
      this.errorMessage = ''
      try {
        const response = await axios.post('http://141.56.137.83:8000/nutzer_create', {
          email: this.email,
          name: this.name,
          passwort_hash: this.password,
        })
        this.$router.push('/')
      } catch (error) {
        if (error.response && error.response.data && error.response.data.detail) {
          this.errorMessage = error.response.data.detail
        } else {
          this.errorMessage = 'Ein unbekannter Fehler ist aufgetreten.'
        }
      }
    }
  }
}
</script>

<style scoped>
/* dein CSS bleibt unverändert */
.create_account-container {
  max-width: 400px;
  padding: 2rem;
  background-color: var(--box-bg-color);
  border-radius: 0.6em;
  box-shadow: 0 4px 12px var(--box-shadow-color);
  text-align: left;
}

.register-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.register-header h1 {
  margin: 0;
  flex-grow: 1;
  text-align: center;
  font-size: 26.4px;
  font-weight: 600;
}

button.button-cancel {
  position: static;
  padding: 0.5em 1em;
  font-size: 1em;
  flex-shrink: 0;
  cursor: pointer;
}

form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.create_block {
  display: block;
  margin-bottom: 0.3rem;
  font-size: 1rem;
}

form label {
  width: 70px;
}

input {
  width: 100%;
}

button.button-submit {
  align-self: center;
  padding: 0.6em 2em;
  font-size: 1.1rem;
  margin-top: 1rem;
}
</style>
