<template>
  <div class="header">
    <!--Slots für die unterschiedlichen Buttons in Einkauf und List-->
    <div class="header-element">
      <slot name="left">
        <!--- TODO: implement default stuff here -->
      </slot>
    </div>

    <div class="header-element">
      <h2>{{ title }}</h2>
    </div>

    <div class="header-element">
      <slot name="right">
        <!--- TODO: implement default stuff here -->
      </slot>
    </div>
  </div>
</template>

<script>
export default {
  name: "AppHeader",
  props: {
    title: {
      type: String,
      required: true,
    },
  },
};
</script>

<style scoped>
.header-element {
  width: 33%;
}

.header {
  justify-content: space-around;
}
</style>
