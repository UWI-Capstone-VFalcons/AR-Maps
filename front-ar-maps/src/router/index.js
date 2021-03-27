import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
import QRScreen from '../views/Scanner.vue';
import OverheadMap from '../views/OverheadMap.vue';
import ARGuide from '../views/ARGuide.vue';


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
    component: OverheadMap,
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
    component: ARGuide,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});
export default router;
