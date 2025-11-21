<template>
  <div class="liste">
    <!-- HEADER -->
    <div class="header">
      <button
        @click="$router.push('/listen')"
        class="button-cancel back-button"
      >
        Zurück
      </button>
      <h2>Favoriten</h2>
      <button @click="add_fav = true" class="button-add button-add-header">
        +
      </button>
    </div>

    <!-- Other -->
    <div v-if="loadingActive" class="loading">Laden...</div>
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>

    <!-- Favorites -->
    <FavGrid :favs="favorites"/>

    <!-- PopUp's -->
    <PopUp v-if="add_fav" @close="add_fav = false" name="Favoriten hinzufügen">
      <AddFav @load_fav="get_favs" />
    </PopUp>
  </div>
</template>

<script>
import axios from "axios";
import FavGrid from "./FavGrid.vue";
import AddFav from "./AddFav.vue";
import PopUp from "./PopUp.vue";
import { inject } from "vue";

export default {
  name: "Liste",
  components: {
    PopUp,
    AddFav,
    FavGrid,
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

/* Produkt hinzufügen Button rechts */
.button-add-header {
  position: absolute;
  right: 20px;
  top: 25px;
}
</style>
