<template>
  <div @click="edit_fav = true" class="card">
    <h3>{{ fav.produkt_name }}</h3>
  </div>

  <PopUp v-if="edit_fav" @close="edit_fav = false" :name="fav.produkt_name" type="no-save">
    <FavEditor :fav="fav" />
  </PopUp>
</template>

<script>
import axios from "axios";
import FavEditor from "./FavEditor.vue";
import PopUp from "../PopUp.vue";

export default {
  components: {
    PopUp,
    FavEditor,
  },
  props: {
    fav: { required: true },
  },
  data() {
    return { name: "Test", edit_fav: false };
  },
};
</script>

<style scoped>
div {
  min-width: 14rem;
  background-color: var(--box-bg-color);
  border-radius: 1rem;
  padding: 1rem;
  box-shadow: 0 1px 2px var(--box-shadow-color);
  transition: box-shadow 0.3s ease;
  border: 1px solid var(--accent-button-color);
}

h3 {
  margin: 0;
  width: 100%;
  color: var(--text-color);
  font-size: 1.2em;
  font-weight: bold;
  word-break: break-word;
}
</style>
