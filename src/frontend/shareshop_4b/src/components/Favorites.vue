<template class="liste">
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

  <FavGrid :favs="favorites" name="FavGrid" />

  <PopUp v-if="add_fav" @close="add_fav = false" name="Favoriten hinzufügen">
    <AddFav @load_fav="get_favs" />
  </PopUp>
</template>

<script>
import axios from "axios";
import FavGrid from "./FavGrid.vue";
import AddFav from "./AddFav.vue";
import PopUp from "./PopUp.vue";
import AppHeader from "./AppHeader.vue";
import { inject } from "vue";

export default {
  name: "Liste",
  components: {
    PopUp,
    AddFav,
    FavGrid,
    AppHeader,
  },
  data() {
    const user = inject("user");
    return {
      errMsg: "",
      add_fav: false,
      favorites: [],
      user,
    };
  },
  methods: {
    async get_favs() {
      const url =
        "http://141.56.137.83:8000/fav_produkte/nutzer/" + this.user.id;
      const response = await axios.get(url);
      this.favorites = response.data;
    },
  },
  mounted() {
    this.get_favs();
  },
};
</script>

<style scoped>
.liste {
  padding-top: 50px;
}
</style>
