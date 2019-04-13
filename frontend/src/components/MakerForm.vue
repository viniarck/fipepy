<template>
  <div id="app">
    <div id="maker-select" class="maker-select">
      <h3>Maker:</h3>
      <!-- <select v&#45;model="makerx" @change="onChange($event)"> -->
      <!--   <option v&#45;for="maker in makers">{{maker.name}}</option> -->
      <!-- </select> -->
      <v-select v-model="makerx" label="name" :options="makers" @change="onChange($event)">
      </v-select>
    </div>
    <CarForm v-bind:maker="makerx"/>
  </div>
</template>

<script>
import CarForm from "./CarForm.vue";
import axios from "axios"

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
  },
  methods: {
    onChange(event){
      console.log(`Maker onChange ${event}`);
      if (typeof event === "object") {
        console.log(`Maker onChange {$event.name}`);
      }
      // console.log(`maker ${event.target.value}`);
      // this.makerx = event.target.value;
    }
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
