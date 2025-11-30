<template>
  <label>
    {{ label }}
    <select :value="choice" @change="onChange">
      <option value="">Keine Angabe</option>
      <option
        v-for="(option, index) in options"
        :key="index"
        :value="option[valueKey]"
      >
        {{ option[displayKey] }}
      </option>
    </select>
  </label>
</template>

<script>
export default {
  name: "SelectArray",
  emits: ["update:choice"],
  props: {
    options: { type: Array, required: true },
    displayKey: { type: String, required: true },
    valueKey: { type: String, require: true },
    choice: { required: true },
    label: { type: String },
  },
  data() {
    return { local_choice: "" };
  },
  methods: {
    onChange(event) {
      const newValue = event.target.value;
      console.log(newValue);
      this.$emit("update:choice", newValue);
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
