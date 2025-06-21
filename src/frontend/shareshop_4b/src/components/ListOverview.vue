<template>
  <header>
    <h1>Einkaufslisten</h1>
    <button @click="newList" id="newlist">+</button>
  </header>
  <main>
    <ul id="einkaufslisten">
      <p>Du hast im Moment noch keine Einkaufslisten. Erstelle doch gerne eine.</p>
    </ul>
  </main>
  <Footer>
    <button id="settings">Einstellungen</button>
  </Footer>
</template>

<script>
export default {
  methods: {
    newList() {
        this.$router.push('/neueliste')  // Weiterleiten
    }
  }
}
</script>

<style scoped>
</style>
