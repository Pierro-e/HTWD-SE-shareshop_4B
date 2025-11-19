<template>
  <button @click="openItem">{{name}}</button>
</template>

<script>
  export default {
    props: {
      name: {type: String},
      item: { type: Object, default: null },
    },
    methods: {
      openItem() {
        if (this.item.id) {
         this.$router.push({
          name: "List",   
          params: { id: this.item.id }
        });
        } else if(this.item.purchase_id){
          this.$router.push({ 
            name: "ProductArchive", 
            params: { purchase_id: this.item.einkauf_id }, 
          });
        }
      }
    }
  }
</script>

<style scoped>

</style>
