import HomePage from './components/HomePage.vue';



import { createRouter, createWebHistory } from 'vue-router';

const routes = [

    { path: '/', name: 'HomePage', component: HomePage },

];

const router = createRouter({
    history: createWebHistory(),
    routes
    
})

export default router
