<template>
  <div class="small">
    <line-chart :chart-data="datacollection" :options="options"></line-chart>
  </div>
</template>

<script>
import LineChart from "./LineChart.js";

export default {
  name: "ModelLineChart",
  props: {
    xValues: {},
    yValues: {},
    yDiffValues: {}
  },
  components: {
    LineChart
  },
  data() {
    return {
      datacollection: null,
      labels: [],
      data: [],
      options: {
        scales: {
          yAxes: [
            {
              ticks: {
                callback: function(value, index, values) {
                  return "$" + value;
                }
              }
            }
          ]
        }
      }
    };
  },
  mounted() {
    this.fillData();
  },
  watch: {
    xValues: {
      immediate: true,
      handler(val, oldVal) {
        if (oldVal !== undefined) {
          this.fillData();
        }
      }
    }
  },
  methods: {
    fillData() {
      this.datacollection = {
        labels: this.xValues,
        datasets: [
          {
            label: "Accumulated Price Difference in BRL ($)",
            backgroundColor: "#ff0000",
            fill: false,
            data: this.yDiffValues
          },
          {
            label: "Total Price in BRL ($)",
            backgroundColor: "#a7c6e5",
            data: this.yValues
          },
        ]
      };
    }
  }
};
</script>

<style>
.small {
  max-width: 600px;
  margin: 10px auto;
}
</style>
