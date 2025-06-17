<template>

    <div class="create_account-container">
        <div class="header">    
            <button class="button-cancel" @click="$router.push('/')">Zurück</button>
            <h1>Registrieren</h1>
        </div>
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

<style scoped>
.create_account-container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #2a2a2a;
  border-radius: 0.6em;
  box-shadow: 0 0 10px rgba(0,0,0,0.3);
  color: rgba(255, 255, 255, 0.9);
  font-family: inherit;
  text-align: left;
}

.header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.header h1 {
  margin: 0;
  flex-grow: 1;
  text-align: center;
  font-size: 2.8rem;
  font-weight: 600;
}

button.button-cancel {
  position: static; /* Wichtig, keine absolute Position */
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
  font-weight: 600;
  font-size: 1rem;
}

input[type="email"],
input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 0.5em 0.75em;
  border-radius: 0.4em;
  border: 1px solid #555;
  background-color: #3a3a3a;
  color: white;
  font-size: 1rem;
  font-family: inherit;
  transition: border-color 0.25s;
}

input[type="email"]:focus,
input[type="text"]:focus,
input[type="password"]:focus {
  outline: none;
  border-color: #646cff;
  box-shadow: 0 0 5px #646cff;
}

button.button-submit {
  align-self: center;
  padding: 0.6em 2em;
  font-size: 1.1rem;
  margin-top: 1rem;
}

.error {
  color: #ff4c4c;
  margin-top: 0.8rem;
  text-align: center;
  font-weight: 600;
}

</style>
