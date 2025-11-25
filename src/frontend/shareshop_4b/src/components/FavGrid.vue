<template>
  <div class="card-grid">
    <FavItem v-for="f in favs" :fav="f"/>
  </div>
</template>

<script>
import FavItem from "./FavItem.vue";

export default {
  components: { FavItem },
  props: {
    favs: { type: Array },
  },
};
</script>

<style scoped></style>
