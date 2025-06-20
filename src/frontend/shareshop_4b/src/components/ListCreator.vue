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
        this.$router.push('/list')  // Weiterleiten
      }
    }
  }
</script>

<style scoped>

</style>
