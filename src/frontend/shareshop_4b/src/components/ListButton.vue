<template>
  <button @click="openItem">{{name}}</button>
</template>

<script>
  export default {
    props: {
      name: {type: String},
      list_id: {type: Number, default: null},
      purchase_id: {type: Number, default: null},
    },
    methods: {
      openItem() {
        if (this.list_id != null) {
        this.$router.push(`/List/${this.list_id}`)
        } else if(this.purchase_id != null){
          this.$router.push(`/product/archive/${this.purchase_id}`)
        }
      }
    }
  }
</script>

<style scoped>

</style>
