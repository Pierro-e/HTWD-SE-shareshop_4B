<template>
  <header>
    <h1>{{ user.name }}'s Einkaufslisten</h1>
    <button @click="newList" id="newlist">+</button>
  </header>
  <main>
    <ListButton
      v-for="list in lists"
      :key="list.id"
      :id="list.id"
      :name="list.name"
    />
  </main>
  <footer>
    <button class= "button-edit" @click="$router.push('/settings')">
      Zu den Profileinstellungen
    </button>
  </footer>
</template>

<script>
import ListButton from './ListButton.vue'
import { inject } from 'vue'
import axios from 'axios'

// TODO: inject('user') nur einmal rufen

// INFO: Doc -> inject soll in setup() ?

export default {
  data() {
    // momentanen Nutzer holen
    const user = inject('user')

    return { lists: [], user}
  },
  methods: {
    // Nutzer möchte neue Liste erstellen
    newList() {this.$router.push('/neueliste')}
  },
  components: {
    ListButton
  },
  async mounted() {
    // Listen des momentanen Nutzers holen
    const user = inject('user')
    const user_id = user.value.id
    const response = await axios.get(`http://141.56.137.83:8000/nutzer/${user_id}/listen`)
    this.lists = response.data
  }
}
</script>

<style scoped>
</style>
