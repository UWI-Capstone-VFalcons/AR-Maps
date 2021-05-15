import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
import QRScreen from '../views/Scanner.vue';
import OverheadMap from '../views/OverheadMap.vue';
import ARGuide from '../views/ARGuide.vue';
import BuildingInfo from '../views/buildinginfo.vue';
import Help from '../components/Help.vue';



Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { title: 'UWI AR Maps' },
  },
  {
    path: '/map',
    name: 'Map',
    component: OverheadMap,
    meta: { title: 'Map' },
  },
  {
    path: '/help',
    name: 'Help',
    component: Help,
    meta: { title: 'Help'},
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
    meta: { title: 'AR' },
  },
  {
    path: '/building_info',
    name: 'BuildingInfo',
    component: BuildingInfo,
    meta: { title: 'Building Info' },
    props: true,
  },
  {
    path: '*',
    name: '404',
    component: Home,
    meta: { title: 'UWI AR Maps' },
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});
export default router;
