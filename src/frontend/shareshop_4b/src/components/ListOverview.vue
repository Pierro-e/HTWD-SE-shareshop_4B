<template>
  <header>
    <h1>Einkaufslisten</h1>
    <button @click="newList" id="newlist">+</button>
  </header>
  <main>
    <ListButton
      v-for="list in lists"
      :key="list.id"
      :name="list.name"
    />
  </main>
  <Footer>
    <button class= "button-edit" @click="$router.push('/settings')">
      Zu den Profileinstellungen
    </button>
  </Footer>
</template>

<script>
import ListButton from './ListButton.vue'
import axios from 'axios'

// INFO: currently this ref object is for test purposes to show show the list display
export default {
  data() {
    return {
      lists: []
    }
  },
  methods: {
    newList() {
        this.$router.push('/neueliste')  // Weiterleiten
    }
  },
  components: {
    ListButton
  },
  mounted() {
    this.lists = axios.get("/lists", {id,name,ersteller,datum})
    //id: int
    //name: str
  }
}
</script>

<style scoped>
</style>
