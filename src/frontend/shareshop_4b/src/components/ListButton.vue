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
        if (this.item.id) {             // bei Übergabe durch ListOverview hat das Objekt List die Variable id
         this.$router.push({
          name: "List",   
          params: { id: this.item.id }
        });
        } else if(this.item.einkauf_id){    // bei Übergabe durch ListArchive ist es einkauf_id (noch auf deutsch, da es direkt aus der DB kommt)
          this.$router.push({ 
            name: "ProductArchive", 
            params: { purchase_id: this.item.einkauf_id },
            query: {
              list_id: this.item.listen_id,
              purchase_name: this.name,
              price: this.item.gesamtpreis
            }
          });
        }
      }
    }
  }
</script>

<style scoped>

</style>
