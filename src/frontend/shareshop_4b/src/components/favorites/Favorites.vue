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

  <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
  <div v-if="ret == 0" class="info">
      Keine Favoriten
  </div>
  <div class="card-grid">
     <ProductCard
      v-for="(f,index) in favorites"
      :key="index"
      :product="f"
      :onSettings="() => onFavClick(f)"
    />
  </div>

  <PopUp v-if="add_fav" @close="add_fav = false" @update="this.fetchFavorites()" name="Favoriten hinzufügen">
    <AddFav/>
  </PopUp>

  <PopUp v-if="edit_fav" @close="edit_fav = false" @update="this.fetchFavorites()" :name="fav_name" type="no-save">
    <FavEditor :fav="fav" />
  </PopUp>

  <BottomBar 
    :highlight-btn="3"
  />
</template>

<script>
import AddFav from "./AddFav.vue";
import FavEditor from "./FavEditor.vue";
import PopUp from "../PopUp.vue";
import AppHeader from "../AppHeader.vue";
import ProductCard from "../ProductCard.vue";
import BottomBar from "../BottomBar.vue"

export default {
  inject: ["updateFavorites", "favorites"],
  components: {
    PopUp,
    AddFav,
    AppHeader,
    ProductCard,
    FavEditor,
    BottomBar
  },
  data() {
    return {
      add_fav: false,
      edit_fav: false,
      fav: null,
      fav_name: "",
      errorMessage: "",
      ret: 1
    };
  },
  async mounted() {
    this.fetchFavorites();
  },
  methods: {
    onFavClick(f){
      this.edit_fav = true;
      this.fav = f;
      this.fav_name = f.produkt_name;
    },
    async fetchFavorites(){
      this.ret = await this.updateFavorites();
      if (this.ret == -1){
        this.errorMessage = "Favoriten konnten nicht geladen werden."
      }
    }
  }
};
</script>

<style scoped>
.card-grid {
  padding-top: 70px;
}
</style>
