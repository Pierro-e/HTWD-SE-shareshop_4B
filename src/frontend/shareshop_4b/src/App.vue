<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
import { ref, provide } from 'vue'
import axios from 'axios'

export default {
  name: 'App',
  setup() {
    const user = ref({
      id: null,
      email: '',
      name: '',
    })

    function setUser(userData) {
      user.value = userData
    }

    provide('user', user)
    provide('setUser', setUser)

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
  provide('getUser', getUser)

    return {} 
  }
}
</script>
