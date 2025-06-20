<template>
  <header>
    <h1>Neue Liste erstellen</h1>
    <button id="done" @click="createList">Fertig</button>
  </header>
  <main>
  </main>
  <Footer>
  </Footer>
</template>

<script>
  export default {
    methods: {
      createList() {
        // TODO: function which creates a new List in the database and returns its ID
        // axios post mit get User id
        const id = "1234"
        this.$router.push('/list/' + id)  // Einkaufsliste aufrufen
      }
    }
  }
</script>

<style scoped>

</style>
