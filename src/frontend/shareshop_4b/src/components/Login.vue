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
.error {
  color: red;
  margin-top: 10px;
}
</style>