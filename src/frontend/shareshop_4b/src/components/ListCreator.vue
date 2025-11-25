<template>
  <header>
    <h1>Neue Liste erstellen</h1>
  </header>
  <main>
    <NewListForm />
  </main>
  <BottomBar />
</template>

<script>
import NewListForm from "./NewListForm.vue";
import BottomBar from "./BottomBar.vue";

export default {
  components: {
    NewListForm,
    BottomBar
  },
};
</script>

<style scoped></style>
