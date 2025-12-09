<template>
  <div class="list-archive">
    <AppHeader :title="`Einkaufsarchiv für\n${user.name}`">
      <template #left>
        <button @click="goBack()" class="button button-cancel back-button">
          <font-awesome-icon icon='arrow-left'/>
        </button>
      </template>
    </AppHeader>

        
    <div class="filter">
      <select v-model="selectedListID" class="filter-dropdown">
        <option :value="null">Alle Listen</option>

        <option 
          v-for="list in userLists" 
          :key="list.id" 
          :value="list.id"
        >
          {{ list.name }}
        </option>
      </select>

      <select v-model="onlyOwn" class="filter-dropdown">
        <option :value="false">Alle Einkäufe</option>
        <option :value="true">Nur eigene Einkäufe</option>
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
      <div v-for="(group, listName) in groupedPurchases" :key="listName" class="list-group">
        <h2 class="info">{{ listName }}</h2>
        <div class="card-list">
          <ListButton
            v-for="purchase in group"
            :key="purchase.einkauf_id"
            :item="purchase"
            :name="formatDate(purchase.eingekauft_am)"
          />
        </div>
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
  props: {
    listFilter: {
      type: [Number, null],
      default: null
    }
  },
  data(){
      return{
          purchases: [],
          loadingActive: true,
          errorMessage: "",
          userLists: [],
          selectedListID: this.listFilter !== null ? this.listFilter : null,
          onlyOwn: false,
      };
  },
  methods: {
    async getData(id) {
      try {   
        const response1 = await axios.get(`http://141.56.137.83:8000/einkaufsarchiv/nutzer_gesamt/${this.user.id}`);
               
        const response2 = await axios.get(`http://141.56.137.83:8000/nutzer/${this.user.id}/listen`);
        if (response1.data.length === 0) {
          this.purchases = [];
          return;
        }
        this.purchases = response1.data;

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
    goBack() {
      if (this.listFilter) {
        this.$router.push({ 
          name: "List", 
          params: { id: this.listFilter } 
        });
      } else 
      {
        this.$router.push(`/listen`);
      }
    }
  },
  computed: {
    filteredPurchases() {
      return this.purchases.filter(p => {
        const matchesList = this.selectedListID ? Number(p.listen_id) === Number(this.selectedListID) : true;

        const matchesUser = this.onlyOwn ? Number(p.eingekauft_von) === Number(this.user.id) : true;

        return matchesList && matchesUser;
      });    
    },
    groupedPurchases() {
      const groups = {};
      this.filteredPurchases.forEach(purchase => {
        const listName = purchase.listen_name;
        if (!groups[listName]) {
          groups[listName] = [];
        }
        groups[listName].push(purchase);
      });
      return groups;
    }
  },
  mounted() {
    this.getData(this.user.id);
  },
};
</script>

<style scoped>
.filter {     
  margin-top: 70px;             
}

.card-list {
  padding: 0;
}

</style>

