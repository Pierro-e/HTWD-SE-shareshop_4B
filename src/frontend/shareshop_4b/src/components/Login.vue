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
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const errorMessage = ref('')
const router = useRouter()

const onSubmit = async () => {
  errorMessage.value = ''
  try {
    const response = await axios.post('http://141.56.137.83:8000/login', {
      email: email.value,
      passwort: password.value,
    })
    // Weiterleitung nach erfolgreichem Login
    router.push('/einfuehrung')
  } catch (error) {
    errorMessage.value = 'Login fehlgeschlagen. Bitte überprüfe deine Eingaben.'
  }
}
</script>

<style scoped>
.error {
  color: red;
  margin-top: 10px;
}
</style>