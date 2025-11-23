<template>
  <div class="bottom-bar">
    <!-- Left Item -->
    <slot name="left"></slot>

    <!-- Middle Items -->
    <slot name="middle"></slot>

    <!-- Right Item -->
    <slot name="right"></slot>
  </div>
</template>

<script>
export default {
  name: "BottomBar"
};
</script>