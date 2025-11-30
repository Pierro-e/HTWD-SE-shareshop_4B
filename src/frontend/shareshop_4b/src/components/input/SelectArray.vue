<template>
  <label>
    {{ label }} - {{ choice }}
    <select>
      <option v-for="(i, index) in opts" :key="i.id" :value="i">
        {{ i.name }}
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
