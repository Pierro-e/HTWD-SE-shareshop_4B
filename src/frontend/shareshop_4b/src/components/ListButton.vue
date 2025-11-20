<template>
  <div class="card" @click="openList">
    <div class="card-header">
      <h3 class="card-name">
        {{name}}
      </h3>
    </div>

    <div class="card-info" v-if="id">
      <span>
        <strong>Ersteller:</strong> {{ ersteller_name }}
      </span>
    </div>
    <div class="card-info" v-else>
      <span style="visibility: hidden">Platzhalter</span>
    </div>
  </div>
</template>

<script>
export default {
  name: "ListButton",
  props: {
    name: {typed: String},
    id: {typed: Number},
    ersteller_name: {typed: String},
  },
  methods: {
      openList() {
        this.$router.push(`/List/${this.id}`)
      }
    }
};
</script>