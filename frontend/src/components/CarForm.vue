<template>
  <div id="app">
    <div id="car-select" class="car-select">
      <h3>Model:</h3>
      <v-select v-model="modelx" label="name" :options="models" @change="onModelChange($event)"></v-select>
    </div>
    <br>
    <h3 v-if="modelx">Chart:</h3>
    <ModelLineChart
      v-if="modelx"
      v-bind:xValues="xValues"
      v-bind:yValues="yValues"
      v-bind:yDiffValues="yDiffValues"
    />
  </div>
</template>

<script>
import axios from "axios";
import ModelLineChart from "./ModelLineChart.vue";
import * as utils from "../utils.js";

export default {
  name: "CarForm",
  components: {
    ModelLineChart
  },
  props: {
    maker: {}
  },
  data() {
    return {
      cars: [],
      modelx: "",
      models: [],
      xValues: [],
      yValues: [],
      yDiffValues: []
    };
  },
  watch: {
    maker: {
      immediate: true,
      handler(val, oldVal) {
        if (typeof this.maker === "object") {
          // if this parent has been deleted in the v-select component
          if (this.maker === null) {
            this.modelx = "";
            this.models = [];
            return;
          }
          axios
            .get(utils.carsUrl(this.maker.name))
            .then(response => (this.cars = response.data))
            .catch(error => utils.alertError(utils.carsUrl(this.maker.name)));
          axios
            .get(utils.carsUrlUnique(this.maker.name))
            .then(response => (this.models = response.data))
            .catch(error => utils.alertError(utils.carsUrl(this.maker.name)));
        }
      }
    }
  },
  methods: {
    onModelChange(event) {
      let ixValues = [];
      let iyValues = [];
      let iDiffValues = [0];
      let lastPrice = 0;
      let totalDiff = 0;
      let firstFound = false;
      for (let i = 0; i < this.cars.length; i++) {
        let model = this.modelx.name;
        if (!this.cars[i].hasOwnProperty("name")) {
          continue;
        }
        let iModel = this.cars[i].name;
        if (model === iModel) {
          let year = this.cars[i].year;
          let price = this.cars[i].price / 100.0;
          ixValues.push(year);
          iyValues.push(price);
          if (firstFound) {
            let diff = Math.abs(price - lastPrice);
            totalDiff += diff;
            iDiffValues.push(totalDiff);
          }
          firstFound = true;
          lastPrice = price;
        }
      }
      this.xValues = ixValues;
      this.yValues = iyValues;
      this.yDiffValues = iDiffValues;
    }
  }
};
</script>

<style scoped>
#app {
  background: #f4f6f7;
}

.car-select {
  max-width: 25em;
  margin-left: auto;
  margin-right: auto;
}
</style>
