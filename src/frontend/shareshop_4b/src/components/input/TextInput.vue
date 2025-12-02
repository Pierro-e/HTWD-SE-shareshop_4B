<template>
  <label>
    {{ label }}
    <input
      type="text"
      :value="text"
      :placeholder="placeholder"
      maxlength="30"
      @input="$emit('update:text', $event.target.value)"
    />
  </label>
</template>
<script>
export default {
  props: {
    text: { type: String },
    placeholder: { type: String },
    label: { type: String },
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

input {
  width: 100%;
  margin-top: 0.5rem;
}
</style>
