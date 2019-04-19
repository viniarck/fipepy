<template>
  <div id="app">
    <Header/>
    <MakerForm v-bind:makers="makers"/>
    <Footer/>
  </div>
</template>

<script>
import Header from "./components/Header.vue";
import MakerForm from "./components/MakerForm.vue";
import Footer from "./components/Footer.vue";
import axios from "axios";
import * as utils from "./utils.js";

export default {
  name: "app",
  components: {
    Header,
    MakerForm,
    Footer,
  },
  data() {
    return {
      makers: []
    };
  },
  mounted() {
    axios
      .get(utils.makersUrl())
      .then(response => (this.makers = response.data))
      .catch(error => utils.alertError(utils.makersUrl()));
  },
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background: #f4f6f7;
}
</style>
