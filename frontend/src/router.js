import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './components/HomePage.vue';
import CourseDetails from './components/CourseDetails.vue';
import GradedAssignment from './components/GradedAssignment.vue';

const routes = [
  { path: '/', component: HomePage },
  { path: '/courses/:id', component: CourseDetails, props: true },
  { path: '/demo', component: GradedAssignment }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
