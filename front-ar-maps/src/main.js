import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css';
import './assets/css/app.css';


Vue.config.productionTip = false;

// Set the default app title
document.title =  'UWI AR Maps';
Vue.prototype.$title = 'UWI AR Maps';

// Vue.prototype.$host = 'http://localhost:5000/'; // Host for testing locally
Vue.prototype.$host = ''; // Host for depoyment to production

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
