import { createRouter, createWebHistory } from 'vue-router'
import HomeView from './views/HomeView.vue'
import CategoryView from './views/CategoryView.vue'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: HomeView },
    { path: '/:category(film|dance|image|song|fanwork)', component: CategoryView },
  ],
})
