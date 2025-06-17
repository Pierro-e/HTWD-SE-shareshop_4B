<template>

    <div class="create_account-container">
        <button class="button-cancel" @click="$router.push('/')">Zurück</button>
      <h1>Registrieren</h1>
        <form @submit.prevent="onSubmit">
            <div class="create_email">
                <label for="email" class="create_block">Email: </label>
                <input
                    v-model="email"
                    type="email"
                    id="email"
                    placeholder="Email"
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
            <button class="button-submit" type="submit">Account erstellen</button>
        </form>
        <div v-if="errorMessage" class="error">{{ errorMessage }}</div>

    </div>
            


</template>

<script setup>
import { ref, inject } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const email = ref('')              // Reaktive Variable, die mit v-model im Template verknüpft ist
const name = ref('')
const password = ref('')

const errorMessage = ref('')
const router = useRouter()


const onSubmit = async () => {
  errorMessage.value = ''
  try {
    const response = await axios.post('http://141.56.137.83:8000/nutzer_create', {
      email: email.value,           // Benutzereingaben für Email und Passwort
      name: name.value,
      passwort_hash: password.value,     // das erste Wort ist das Schlüsselwort im Backend, das zweite ist der Wert
    })

    router.push('/')     // Weiterleitung nach erfolgreicher Registrierung
    } catch (error) {
        if (error.response && error.response.data && error.response.data.detail) {
            errorMessage.value = error.response.data.detail
        } else {
            errorMessage.value = 'Ein unbekannter Fehler ist aufgetreten.'
        }
    }
}
</script>