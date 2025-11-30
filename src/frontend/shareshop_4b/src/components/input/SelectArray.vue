<template>
  <label>
    {{ label }}
    <select v-model="local_choice">
      <option v-for="i in opts" :key="i" :value="i">
        {{ i[display] }}
      </option>
    </select>
  </label>
</template>

<script>
export default {
  name: "SelectArray",
  emits: ["update:choice"],
  props: {
    opts: { type: Array, required: true },
    display: { type: String, required: true },
    choice: { required: true },
    label: { type: String },
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

<style scoped>
label {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 1.25rem;
}

select {
  margin-top: 0.5rem;
}
</style>
