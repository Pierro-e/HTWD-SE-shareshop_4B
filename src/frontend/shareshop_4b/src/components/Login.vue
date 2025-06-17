<template>
  <div class="login_container">                      
    <h2>Login</h2>
    <form @submit.prevent="onSubmit">
      <div class="login_email">
        <label for="email" class="login_block">Email</label>
        <input
          v-model="email"
          type="email"
          id="email"
          placeholder="Email"
          required
        />
      </div>
      <div class="login_pw">
        <label for="password" class="login_block">Passwort</label>
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
    <button class="button-add" @click="$router.push('/registrieren')">Registrieren</button>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const email = ref('')              // Reaktive Variable, die mit v-model im Template verknüpft ist
const password = ref('')
const errorMessage = ref('')
const router = useRouter()

const setUser = inject('setUser')       // Funktion setUser aus App.vue importieren

const onSubmit = async () => {
  errorMessage.value = ''
  try {
    const response = await axios.post('http://141.56.137.83:8000/login', {
      email: email.value,           // Benutzereingaben für Email und Passwort
      passwort: password.value,     // das erste Wort ist das Schlüsselwort im Backend, das zweite ist der Wert
    })

    setUser(response.data)          // Benutzerdaten setzen
    router.push('/einfuehrung')     // Weiterleitung nach erfolgreichem Login
  } catch (error) {
    if (error.response && error.response.data && error.response.data.detail) {
      errorMessage.value = error.response.data.detail
    } else {
      errorMessage.value = 'Login fehlgeschlagen. Bitte überprüfe deine Eingaben.'
    }
  }
}
</script>


<style scoped>
.login_container {
  max-width: 400px;
  margin: 3em auto;
  padding: 2em;
  background-color: #2a2a2a;
  border-radius: 0.75em;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
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

.login_email,
.login_pw {
  display: flex;
  flex-direction: column;
}

.login_block {
  margin-bottom: 0.4em;
  font-weight: 500;
}

input[type="email"],
input[type="password"] {
  padding: 0.6em 0.8em;
  border-radius: 0.4em;
  border: none;
  font-size: 1em;
  box-sizing: border-box;
  background-color: #3a3a3a;
  color: white;
  transition: background-color 0.25s, border-color 0.25s;
}

input[type="email"]:focus,
input[type="password"]:focus {
  outline: none;
  background-color: #505050;
  border: 1px solid #646cff;
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


