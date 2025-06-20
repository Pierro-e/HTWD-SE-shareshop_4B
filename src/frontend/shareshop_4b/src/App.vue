<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script setup>
import { ref, provide} from 'vue'

const user = ref({  //Benutzerdaten bereitgestellt, dass man sie in anderen Komponenten verwenden kann
  id: null,
  email: '',
  name: '',
  list: '',
})
provide('user', user)   //mit provide die Daten bereitstellen, um sie in anderen Komponenten zu verwenden
                        // Nutzung mit inject('user') in anderen Komponenten
function setUser(userData) {
  user.value = userData
}

provide('setUser', setUser)   //mit provide die Funktion bereitstellen, um die Benutzerdaten zu setzen
</script>
