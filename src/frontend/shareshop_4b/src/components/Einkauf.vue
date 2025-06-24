<template>
    <div class="Einkauf">
        <div class="header">
            <button @click="einkauf_abbrechen" class="button button-cancel">Einkauf abbrechen</button>
            <h2 class="list-title">{{ list_name }}</h2>
        </div>
    </div>


</template>

<script>
import axios from 'axios'
import { inject } from 'vue'

export default {
    name: 'Einkauf',
    inject: ['user', 'getUser'],
    props: ['list_id'],
    data() {
        return {
        list_name: '',
        errorMessage: '',
        listenproduke: [], // Tippfehler: vermutlich "listenprodukte"
        userData: null,
        }
    },
    methods: {
        async get_list(id) {
            this.errorMessage = '';
            try {
                const response = await axios.get(`http://141.56.137.83:8000/listen/by-id/${id}`);
                this.list_name = response.data.name;
            } catch (error) {
                if (error.response?.data?.detail) {
                this.errorMessage = error.response.data.detail;
                } else {
                this.errorMessage = 'Fehler beim Laden der Liste';
                }
            }
        },

        async get_products(id) {
            this.errorMessage = '';
            try {
                const response = await axios.get(`http://141.56.137.83:8000/listen/${id}/produkte`);
                this.listenproduke = response.data;

                for (const produkt of this.listenproduke) {
                try {
                    const res1 = await axios.get(`http://141.56.137.83:8000/produkte/by-id/${produkt.produkt_id}`);
                    produkt.name = res1.data.name;
                } catch {
                    produkt.name = '[Fehler beim Laden]';
                }

                try {
                    const res2 = await axios.get(`http://141.56.137.83:8000/einheiten/${produkt.einheit_id}`);
                    produkt.einheit_abk = res2.data.abkürzung;
                } catch {
                    produkt.einheit_abk = '';
                }

                if (produkt.produkt_menge !== undefined && produkt.produkt_menge !== null) {
                    const menge = Number(produkt.produkt_menge);
                    if (Number.isInteger(menge)) {
                    produkt.produkt_menge = menge.toString();
                    } else {
                    produkt.produkt_menge = menge.toFixed(2);
                    }
                }
                }
            } catch (error) {
                if (error.response?.data?.detail) {
                this.errorMessage = error.response.data.detail;
                } else {
                this.errorMessage = 'Fehler beim Laden der Produkte';
                }
            }
        },

        einkauf_abbrechen() {
            const list_id = this.list_id || this.$route.params.listenId;
            this.$router.push(`/list/${list_id}`);
        }
    },
  mounted() {
    this.errorMessage = '';
    const id = this.list_id || this.$route.params.listenId;
    this.userData = this.user;
    this.get_list(id);
    this.get_products(id);
  },
}; 

</script>

<style scoped>

</style>