<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
import { ref, provide, onMounted, watch } from 'vue'
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

    const theme = ref('Dunkel'); // Standardwert

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
    
    document.documentElement.setAttribute('css-theme', theme.value); // Thema setzen
    }),

    // schauen ob sich Thema geändert hat und setzen
    watch(theme, () => {
      const theme = localStorage.getItem("theme");
      if (theme === null){ // Default setzen
        localStorage.setItem("theme", "Dunkel");
      }

      document.documentElement.setAttribute("css-theme", theme); // Thema setzen
    });

    function setUser(userData) {
      user.value = userData
      // User auch im localStorage speichern
      localStorage.setItem('user', JSON.stringify(userData))
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

    return {}
  }
}
</script>
