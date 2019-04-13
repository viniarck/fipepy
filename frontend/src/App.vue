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
      .get('http://localhost:8000/fipe/v1/makers/?format=json')
      .then(response => (this.makers = response.data))
      .catch(error => console.log(error));
  }
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
