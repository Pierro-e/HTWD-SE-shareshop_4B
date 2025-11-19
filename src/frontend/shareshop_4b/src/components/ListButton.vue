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
        } else if(this.item.einkauf_id){
          this.$router.push({ 
            name: "ProductArchive", 
            params: { purchase_id: this.item.einkauf_id },
            query: {
              list_id: this.item.listen_id,
              purchase_name: this.name
            }
          });
        }
      }
    }
  }
</script>

<style scoped>

</style>
