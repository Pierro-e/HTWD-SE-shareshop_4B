<template>
  <form @submit.prevent="alter_fav">
    <TextInput v-model:text="fav_copy.beschreibung" label="Beschreibung" />
    <NumInput v-model:num="fav_copy.menge" label="Menge" />
    <SelectObjectArray
      v-model:choice="fav_copy.einheit_id"
      :options="units"
      displayKey="name"
      valueKey="id"
      label="Einheit"
    />
    <button type="submit" class="button-submit">speichern</button>
    <button type="button" class="button-delete" @click="delete_fav">löschen</button>
  </form>
</template>

<script>
import TextInput from "../input/TextInput.vue";
import NumInput from "../input/NumInput.vue";
import SelectObjectArray from "../input/SelectObjectArray.vue";
import axios from "axios";

export default {
  inject: ["fetchUnits", "user", "updateFavorites"],
  components: {
    TextInput,
    NumInput,
    SelectObjectArray,
  },
  props: {
    fav: { required: true },
  },
  methods: {
    async alter_fav() {
      const url =
        "http://141.56.137.83:8000/fav_produkte_update/nutzer/" +
        this.user.id +
        "/produkt/" +
        this.fav.produkt_id;

      const response = await axios.put(url, this.fav_copy);
      // close PopUP
      this.$parent.$emit("close");
      this.$parent.$emit("update"); // Fav updaten
    },
    async delete_fav() {
      console.log("DeleteFav")
      const url =
        "http://141.56.137.83:8000/fav_produkte_delete/nutzer/" +
        this.user.id +
        "/produkt/" +
        this.fav.produkt_id;
      const response = await axios.delete(url);
      // close PopUP
      this.$parent.$emit("close");
      this.$parent.$emit("update"); // Fav updaten
    },
  },
  data() {
    return { units: [], fav_unit: {}, fav_copy: {} };
  },
  async mounted() {
    this.fav_copy = { ...this.fav }; // Arbeitskopie
    try {
      this.units = await this.fetchUnits();

      /*
      const url = "http://141.56.137.83:8000/einheiten/" + this.fav.einheit_id;
      const response = await axios.get(url);
      this.fav_unit = response.data.id;
      */

    } catch (error) {
      console.log(error);
      return;
    }
  },
};
</script>

<style scoped>
button {
  width: 100%;
}
form {
  display: flex;
  flex-direction: column;
  margin-bottom: 1.25rem;
}
</style>