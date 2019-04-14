import Vue from 'vue'
import App from './App.vue'
import vSelect from 'vue-select'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'

Vue.config.productionTip = false
Vue.component('v-select', vSelect)
Vue.use(Vuetify)

new Vue({
  render: h => h(App),
}).$mount('#app')
