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
      theme: null,
      accent: null
    })

    var theme = ref(null)
    var accent = ref(null)

    // User beim Start aus localStorage laden
    onMounted(() => {
      let storedUser = localStorage.getItem('user')
      if (storedUser) {
        try {
          user.value = JSON.parse(storedUser)
        } catch {
          user.value = { id: null, email: '', name: '', theme: null, accent: null }
          localStorage.setItem('user', JSON.stringify(user.value))
        }
      }
      else { // Leerwerte setzen
        user.value = { id: null, email: '', name: '', theme: null, accent: null }
        localStorage.setItem('user', JSON.stringify(user.value))
        
        storedUser = localStorage.getItem('user') // user erneut laden
      }

      // Theme laden
      theme = getThemeText(storedUser.theme)
      document.documentElement.setAttribute('css-theme', theme) // Thema setzen

      // Akzentfarbe laden
      accent = getAccentText(storedUser.color)
      document.documentElement.setAttribute('css-accent', accent) // Farbe setzen
    });

    // Integerwert als Thema interpretieren
    function getThemeText(userTheme) {
      switch (userTheme){
        case 0: return "Automatisch"
        case 1: return "Dunkel"
        case 2: return "Hell"
        default: return "Automatisch" // Default setzen
      }
    }

    // Integerwert als Farbe interpretieren
    function getAccentText(userAccent) {
      switch (userAccent){
        case 0: return "Blau";
        case 1: return "Lila";
        case 2: return "Grün"; 
        case 3: return "Rot";
        case 4: return "Orange";
        default: return "Blau" // Default setzen
      }
    }

    function setUser(userData) {
      user.value = {
        ...userData
      }
      // User auch im localStorage speichern
      localStorage.setItem('user', JSON.stringify(user.value))
    }

    function deleteUser(){
      user.value = { id: null, email: '', name: '', theme: null, accent: null }
      localStorage.setItem('user', JSON.stringify(user.value))

      // Theme zurücksetzen
      let storedUser = localStorage.getItem('user')
      //console.log("Theme reset: " + storedUser)
      theme = getThemeText(storedUser.theme)
      accent = getAccentText(storedUser.color)

      document.documentElement.setAttribute("css-theme", theme) // Thema setzen
      document.documentElement.setAttribute('css-accent', accent) // Farbe setzen
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
    provide('getThemeText', getThemeText)
    provide('getAccentText', getAccentText)

    return {}
  }
}
</script>
