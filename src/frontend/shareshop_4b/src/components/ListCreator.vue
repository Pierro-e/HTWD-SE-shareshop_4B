<template>
  <header>
    <h1>Neue Liste erstellen</h1>
  </header>
  <main>
    <NewListForm />
  </main>
</template>

<script>
import NewListForm from "./NewListForm.vue";

export default {
  components: {
    NewListForm,
  },
};
</script>

<style scoped></style>
