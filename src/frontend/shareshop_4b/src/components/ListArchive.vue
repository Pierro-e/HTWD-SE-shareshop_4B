<template>
  <div class="list-archive">
    <h2>Listenarchiv für Liste {{ list_id }}</h2>
    <p>Listenname: {{ list_name }}</p>
  </div>
</template>

<script>
import axios from "axios";
export default {
    name: "ListArchive",
    props: ["list_id"],

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
