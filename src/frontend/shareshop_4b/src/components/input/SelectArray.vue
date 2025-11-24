<template>
  <select v-model="local_choice">
    <option v-for="i in opts" :key="i" :value="i">
      {{ i[display] }}
    </option>
  </select>
</template>

<script>
export default {
  name: "SelectArray",
  emits: ["update:choice"],
  props: {
    opts: { type: Array, required: true },
    display: { type: String, required: true },
    choice: { required: true },
  },
  data() {
    return { local_choice: "" };
  },
  watch: {
    local_choice(val) {
      this.$emit("update:choice", val);
    },
  },
};
</script>

<style scoped></style>
