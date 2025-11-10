<template>
  <input
    type="number"
    :value="num"
    :step="step"
    min="0"
    placeholder="0"
    @input="$emit('update:num', $event.target.value)"
  />
</template>

<script>
export default {
  props: {
    num: { type: Number},
    step: { type: String, default: 0.25 },
  },
};
</script>

<style scoped></style>
