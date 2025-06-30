<template>
  <button @click="openList">{{name}}</button>
</template>

<script>
  export default {
    props: {
      name: {typed: String},
      id: {typed: Number}
    },
    methods: {
      openList() {
        this.$router.push(`/List/${this.id}`)
      }
    }
  }
</script>

<style scoped>

</style>
