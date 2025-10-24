<template>
  <button :class="fav_flag && 'fav'" @click="changeFav"/>
</template>

<script>
  import axios from "axios";

  export default {
    props: {
      fav_flag: {typed: Boolean },
    },
    methods: {
      changeFav() {
        this.$emit("changedFav");
      }
    }
  }
</script>

<style scoped>

  /* Container */
  button{
    background: none;
    outline: none;
    padding: 0;
    width: 48px; /* TODO: make it dynamic */
    height: 48px; /* TODO: make it dynamic */
    display: flex;
  }

  /* ★ */
  button::before {

    /* ★ zeichnen */
    clip-path: polygon(
      50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%,
      50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%
    );

    /* ★ stylen*/
    content: '';
    width: 100%;
    height: 100%;
    background: #242424;
  }

  /* favorisiert -> ★ ausmalen */
  .fav::before{
    background: #ffcc00;
  }
</style>
