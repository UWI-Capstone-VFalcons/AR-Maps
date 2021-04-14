import Vue from 'vue'
import App from './App.vue'
import * as VueGoogleMaps from 'vue2-google-maps'

Vue.config.productionTip = false



 
Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyB5QmIo_yG56_KI-WC91I1mmsyZ9cOZF9s',

  },

})

new Vue({
  render: h => h(App),
}).$mount('#app')
