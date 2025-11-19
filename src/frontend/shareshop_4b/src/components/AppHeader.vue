<template>
  <div class="header">
    <!--Slots für die unterschiedlichen Buttons in Einkauf und List-->
    <div class="button-left">
      <slot name="left"></slot>
    </div>

    <h2>{{ title }}</h2>

    <div class="button-right">
      <slot name="right"></slot>
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
    }
  }
};
</script>

<style>
/* Header für Listen und Einkauf */
.header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 70px; /* vorher 60px */
  background-color: var(--accent-header-bg-color);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 5px var(--box-shadow-color);
}

/* h2 mittig im Header */
.header h2 {
  vertical-align:bottom;
  margin: 0;
  top: 20px;
  font-weight: 600;
  font-size: 1.4rem;
  color: white;
  text-align: center;
  /* Kein position fixed mehr! */
}

/* Button links */
.button-left {
  position: absolute;
  left: 10px;
  top: 10px;
}

/* Button rechts */
.button-right {
  position: absolute;
  right: 10px;
  top: 10px;
}

</style>