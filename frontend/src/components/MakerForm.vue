<template>
  <div id="app">
    <div id="maker-select" class="maker-select">
      <h3>Maker:</h3>
      <v-select v-model="makerx" label="name" :options="makers">
      </v-select>
    </div>
    <CarForm v-bind:maker="makerx"/>
  </div>
</template>

<script>
import CarForm from "./CarForm.vue";

export default {
  name: "MakerForm",
  components: {
    CarForm
  },
  props: {
    makers: []
  },
  data() {
    return { makerx: "" };
  }
};
</script>

<style scoped>
#app {
  background: #f4f6f7;
}

.maker-select {
  max-width: 25em;
  margin-left: auto;
  margin-right: auto;
}
</style>
