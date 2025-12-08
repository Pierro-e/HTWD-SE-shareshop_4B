<template>
  <div class="list-archive">
    <AppHeader :title="`Einkaufsarchiv für\n${user.name}`">
      <template #left>
        <button @click="this.$router.go(-1)" class="button button-cancel back-button">
          <font-awesome-icon icon='arrow-left'/>
        </button>
      </template>
    </AppHeader>

        
    <div class="filter">
      <select v-model="selectedListID" class="filter-dropdown">
        <option :value="null">Alle Einkäufe</option>

        <option 
          v-for="list in userLists" 
          :key="list.id" 
          :value="list.id"
        >
          {{ list.name }}
        </option>
      </select>
    </div>


    <div v-if="loadingActive" class="loading">Laden...</div>
    <div v-else-if="errorMessage" class="error">{{ errorMessage }}</div>

    <!-- wenn es insgesamt keine Einkäufe gibt -->
    <div v-else-if="purchases.length === 0" class="info">
      Keine Einkäufe   
    </div>

    <!-- Wenn keine Einkäufe nach Filter vorhanden sind -->
    <div v-else-if="filteredPurchases.length === 0" class="info">
      Keine Einkäufe für die ausgewählte Liste
    </div>

    <div v-else>
      <div class="card-list">
        <ListButton
          v-for="purchase in filteredPurchases"
          :key="purchase.einkauf_id"
          :item="purchase"
          :name="`${purchase.listen_name} - ${formatDate(purchase.eingekauft_am)}`"
          :isUserArchive="true"
        />
      </div>
    </div>
  </div>
  <BottomBar 
    :highlight-btn="2"
  />
</template>

<script>
import axios from "axios";
import AppHeader from "./AppHeader.vue";
import ListButton from "./ListButton.vue";
import BottomBar from "./BottomBar.vue";
export default {
  name: "userArchive",
  inject: ["user"],
  components: {
    AppHeader, 
    ListButton, 
    BottomBar
  },
  data(){
      return{
          purchases: [],
          loadingActive: true,
          errorMessage: "",
          userLists: [],
          selectedListID: null,
      };
  },
  methods: {
    async getData(id) {
      try {   
        const response1 = await axios.get(`http://141.56.137.83:8000/einkaufsarchiv/nutzer_alle/${this.user.id}`);
        
        const response2 = await axios.get(`http://141.56.137.83:8000/nutzer/${this.user.id}/listen`);
       
        if (response1.data.length === 0) {
          this.purchases = [];
          return;
        }
        this.purchases = response1.data;
        console.log(this.purchases);

        if (response2.data.length === 0) {
          this.userLists = [];
          return;
        }
        this.userLists = response2.data;
        
      } catch (error) {
        this.errorMessage = error.response?.data?.detail || "Fehler beim Laden der Daten";
      } finally {
        this.loadingActive = false;
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return "";
      const date = new Date(dateStr);
      return new Intl.DateTimeFormat("de-DE", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric"
      }).format(date);  // aus "JJJJ-MM-TT" wird "TT.MM.JJJJ"
    },
  },
  computed: {
    filteredPurchases() {
      if (!this.selectedListID) return this.purchases;

      return this.purchases.filter(p => p.listen_id === this.selectedListID);
    }
  },
  mounted() {
    this.getData(this.user.id);
  },
};
</script>

<style scoped>
.card-list {
  padding-top: 60px;
}
.filter {
  position: relative;      
  margin-top: 80px;        
  z-index: 1001;           
}

.filter-dropdown {
  width: 100%;
  padding: 8px;
  font-size: 15px;
  border-radius: 6px;
  border: 1px solid #ccc;
  background-color: white;
  z-index: 1001;          
}




</style>
