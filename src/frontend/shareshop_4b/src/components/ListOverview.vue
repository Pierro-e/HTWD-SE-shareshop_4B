<template>
  <header>
    <h1>Einkaufslisten</h1>
    <button @click="newList" id="newlist">+</button>
  </header>
  <main>
<ListButton v-for="list in lists" :key="list.id" :name="list.name" />
  </main>
  <Footer>
    <button class= "button-edit" @click="$router.push('/settings')">
      Zu den Profileinstellungen
    </button>
  </Footer>
</template>

<script>
import ListButton from './ListButton.vue'
/*
// INFO: currently this ref object is for test purposes to show show the list display
*/
export default {
  data() {
    return {
      lists: [
        {id: 1, name: "WG1"},
        {id: 2, name: "WG2"},
        {id: 3, name: "WG3"}
      ]
    }
  },
  methods: {
    newList() {
        this.$router.push('/neueliste')  // Weiterleiten
    }
  },
  components: {
    ListButton
  }
}
</script>

<style scoped>
</style>
