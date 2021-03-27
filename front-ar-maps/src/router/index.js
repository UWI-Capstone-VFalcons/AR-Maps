import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
import QRScreen from '../views/Scanner.vue';
Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { title: 'AR Maps' },
  },
  {
    path: '/map',
    name: 'Map',
    component: Home,
  },
  {
    path: '/scan',
    name: 'Scan',
    component: QRScreen,
    meta: { title: 'Scan' },
  },
  {
    path: '/ar',
    name: 'AR-Map',
    component: Home,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});
export default router;
