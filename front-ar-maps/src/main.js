import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css';
import './assets/css/app.css';
import * as VueGoogleMaps from 'vue2-google-maps'
import VueGeolocation from 'vue-browser-geolocation'

Vue.config.productionTip = false



 
Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyB5QmIo_yG56_KI-WC91I1mmsyZ9cOZF9s',

  },

})

Vue.use(VueGeolocation)

// Set the default app title
document.title =  'UWI AR Maps';
Vue.prototype.$title = 'UWI AR Maps';

// Vue.prototype.$host = 'http://localhost:5000/'; // Host for testing locally
Vue.prototype.$host = '/'; // Host for depoyment to production

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
