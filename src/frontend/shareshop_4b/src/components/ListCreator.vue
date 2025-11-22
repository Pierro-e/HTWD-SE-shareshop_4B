<template>
    <AppHeader :title="String('Neue Liste')">
    <template #left>
    </template>

    <template #right>
    </template>
  </AppHeader>

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

</template>

<script>
import axios from "axios";
import AppHeader from "./AppHeader.vue";

export default {
  inject: ["user"],
  components: {
    AppHeader
  },
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
        // neue Liste erstellen
        const date = new Date(Date.now());
        const ISODate = date.toISOString().split('T')[0];

        const res = await axios.post("http://141.56.137.83:8000/listen", {
          name: this.name,
          ersteller: this.user.id,
          datum: ISODate
        });

        // neu erstellte Liste aufrufen
        this.$router.push(`/list/${res.data.id}`);
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
  @media (min-width: 480px) {
    input {
      width: 300px;
    }
  }

  .error {
    width: 90%;
  }

  form label {
    width: 40px;
  }
</style>
