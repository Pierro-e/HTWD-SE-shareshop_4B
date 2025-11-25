<template>
  <div class="card" @click="openList">
    <div class="card-header">
      <h3 class="card-name">
        {{name}}
      </h3>
    </div>

    <div class="card-info" v-if="item.ersteller_name">
      <span>
        <strong>Ersteller:</strong> {{ item.ersteller_name }}
      </span>
    </div>
    <div class="card-info" v-else>
      <span style="visibility: hidden">Platzhalter</span>
    </div>
  </div>
</template>

<script>
export default {
  name: "ListButton",
  props: {
    name: {type: String},
    item: { type: Object, default: null },
    isUserArchive: { type: Boolean, default: false }
  },
  methods: {
    openList() {
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
            price: this.item.gesamtpreis,
            isUserArchive: this.isUserArchive
          }
        });
      }
    }
  }
};
</script>

<style scoped>
.card {
  cursor: pointer;
  transition: transform .15s;
}

.card:hover {
  transform: scale(1.02);
}

.card:active {
  transform: scale(0.98);
}
</style>