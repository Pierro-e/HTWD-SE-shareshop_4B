<template>
  <header>
    <h1>Neue Liste erstellen</h1>
  </header>
  <main>
    <Form
      to="url"
      after="function"
      />
  </main>
  <Footer>
  </Footer>
</template>

<script>
  import Form from './Form.vue'
  // TODO: Form einbinden

  export default {
    data() {
    },
    components: {
      Form
    },
    methods: {
      // TODO: Funktion die aufgerufen wird, wenn Form abgeschickt wird
    }
  }
</script>

<style scoped>

</style>
