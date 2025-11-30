<template>
  <div>
    <slot></slot>
  </div>
</template>

<script></script>

<style scoped>
div {
  width: 90%;
  display: grid;
  gap: 1rem;
}

@media (min-width: 768px) {
  div {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  div {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>
