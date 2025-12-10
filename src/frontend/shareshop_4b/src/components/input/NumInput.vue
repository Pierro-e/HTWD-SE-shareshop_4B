<template>
  <label>
    {{ label }}
    <input
      type="number"
      :value="num"
      :step="step"
      min="0"
      placeholder="0"
      @input="$emit('update:num', $event.target.value)"
    />
  </label>
</template>

<script>
export default {
  props: {
    num: { type: Number },
    step: { type: Number, default: 0.25 },
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
  margin-top: 0.5rem;
}
</style>
