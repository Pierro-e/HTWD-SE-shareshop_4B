<template>
  <div class="card">
    <div class="card-header">
      <h3 class="card-name">{{ name }}</h3>
      <button class="button-product-settings" @click="edit_fav = true">✏️</button>
    </div>
  </div>
  <PopUp v-if="edit_fav" @close="edit_fav = false">
    <FavEditor :fav="fav"/>
  </PopUp>
</template>

<script>
import axios from "axios";
import FavEditor from "./FavEditor.vue";
import PopUp from "./PopUp.vue";

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
  methods: {
    async get_name() {
      const url =
        "http://141.56.137.83:8000/produkte/by-id/" + this.fav.produkt_id;
      const response = await axios.get(url);
      this.name = response.data.name;
    },
  },
  mounted() {
    this.get_name();
  },
};
</script>

<style scoped>
</style>
