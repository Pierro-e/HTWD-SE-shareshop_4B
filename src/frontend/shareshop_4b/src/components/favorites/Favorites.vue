<template>
  <AppHeader title="Favoriten">
    <template v-slot:left>
      <button @click="$router.go(-1)" class="button-cancel back-button">
        Zurück
      </button>
    </template>
    <template v-slot:right>
      <button @click="add_fav = true" class="button-add">+</button>
    </template>
  </AppHeader>

  <Grid>
    <FavItem v-for="f in favorites" :fav="f"/>
  </Grid>

  <PopUp v-if="add_fav" @close="add_fav = false" name="Favoriten hinzufügen">
    <AddFav/>
  </PopUp>
</template>

<script>
import axios from "axios";
import AddFav from "./AddFav.vue";
import FavItem from "./FavItem.vue";
import PopUp from "../PopUp.vue";
import Grid from "../Grid.vue";
import AppHeader from "../AppHeader.vue";
import { inject, ref } from "vue";

export default {
  inject: ["updateFavorites", "favorites"],
  components: {
    PopUp,
    AddFav,
    Grid,
    FavItem,
    AppHeader,
  },
  data() {
    return {
      add_fav: false,
    };
  },
  mounted() {
    this.updateFavorites();
  },
};
</script>

<style scoped></style>
