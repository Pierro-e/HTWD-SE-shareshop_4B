<template>
  <form @submit.prevent="onSubmit">
    <div class="form-content">
      <div>
        <label for="list_name">Name: </label>
        <input
          v-model="name"
          type="text"
          id="list_name"
          placeholder="WG Albertplatz"
        />
      </div>
    </div>
    
    <button class="button-cancel" @click="$router.push(`/listen`)">Abbrechen</button>
    <button class="button-submit" type="submit">Erstellen</button>
  </form>
  <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
  <BottomBar />
</template>

<script>
import axios from "axios";
import BottomBar from "./BottomBar.vue";

export default {
  inject: ["user"],
  components: {BottomBar},
  data() {
    return {
      name: "",
      errorMessage: "",
    };
  },
  methods: {
    async onSubmit() {
      this.errorMessage = "";
      
      if (this.name === ""){
        this.errorMessage = "Listenname darf nicht leer sein";
        return;
      }

      try {
        // eine freie ID für die neue Liste bestimmen
        let new_id = 1;
        const res_list_id = await axios.get("http://141.56.137.83:8000/listen");
        for (let i = 0; i < res_list_id.data.length; i++) {
          if (res_list_id.data[i].id >= new_id) {
            new_id = res_list_id.data[i].id + 1;
          }
        }
        // neue Liste erstellen
        const res = await axios.post("http://141.56.137.83:8000/listen", {
          id: new_id,
          name: this.name,
          ersteller: this.user.id,
        });

        // neu erstellte Liste aufrufen
        this.$router.push(`/list/${new_id}`);
      } catch (error) {
        if (
          error.response &&
          error.response.data &&
          error.response.data.detail
        ) {
          this.errorMessage = error.response.data.detail;
        } else {
          this.errorMessage = "Liste konnte nicht erstellt werden";
        }
      }
    },
  },
};
</script>

<style scoped>
  .error {
    width: 80%;
  }

  form label {
    width: 40px;
  }

</style>
