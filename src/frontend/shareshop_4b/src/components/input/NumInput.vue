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
    step: { type: String, default: 0.25 },
    label: { type: String },
  },
};
</script>

<style scoped></style>
