<template>
  <div class="list-archive">

    <AppHeader :title="`Listenarchiv für\n${list_name}`" class="multiline-title">
      <template #left>
        <button @click="einkauf_abbrechen" class="button button-cancel back-button">
          Zurück
        </button>
      </template>
    </AppHeader>

    <div v-if="loadingActive" class="loading">Laden...</div>
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
  </div>
</template>

<script>
import axios from "axios";
import AppHeader from "./AppHeader.vue";
export default {
    name: "ListArchive",
    props: ["list_id"],
    components: {AppHeader},

    data(){
        return{
            list_name: "",
            errorMessage: "",
            loadingActive: true,
        };
    },

    methods: {
        async get_list(id) {
        this.errorMessage = "";
        try {
            const response = await axios.get(
            `http://141.56.137.83:8000/listen/by-id/${id}`,
            );
            this.list_name = response.data.name;
        } catch (error) {
            if (error.response?.data?.detail) {
            this.errorMessage = error.response.data.detail;
            } else {
            this.errorMessage = "Fehler beim Laden der Liste";
            }
        }
        this.loadingActive = false;
        },
    },
    mounted() {
        this.errorMessage = "";
        const id = this.list_id || this.$route.params.listenId;
        this.get_list(id);
    },





};
</script>

<style>
.multiline-title h2 {
    white-space: pre-line;
}
</style>
