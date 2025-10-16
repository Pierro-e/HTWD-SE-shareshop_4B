<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
import { ref, provide, onMounted } from 'vue'
import axios from 'axios'

// TODO: formal der Options API von Vue.js anpassen
export default {
  name: 'App',
  setup() {
    const user = ref({
      id: null,
      email: '',
      name: '',
    })

    // User beim Start aus localStorage laden
    onMounted(() => {
      const storedUser = localStorage.getItem('user')
      if (storedUser) {
        try {
          user.value = JSON.parse(storedUser)
        } catch {
          localStorage.removeItem('user')
        }
      }
    })

    function setUser(userData) {
      user.value = userData
      // User auch im localStorage speichern
      localStorage.setItem('user', JSON.stringify(userData))
    }

    function deleteUser(){
      user.value = { id: null, email: '', name: '' }
      localStorage.removeItem('user') 
    }

    async function getUser(id) {
      try {
        const response = await axios.get(`http://141.56.137.83:8000/nutzer/by-id`, {
          params: { id: id }
        })
        return response.data
      } catch (error) {
        console.error('Fehler beim Laden des Nutzers:', error)
        throw error
      }
    }

    provide('user', user)
    provide('setUser', setUser)
    provide('getUser', getUser)
    provide('deleteUser', deleteUser)

    return {}
  }
}
</script>
