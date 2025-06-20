<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
import { ref, provide } from 'vue'

export default {
  name: 'App',
  setup() {
    const user = ref({
      id: null,
      email: '',
      name: '',
      list: '',
    })

    function setUser(userData) {
      user.value = userData
    }

    provide('user', user)
    provide('setUser', setUser)

    return {} 
  }
}
</script>
