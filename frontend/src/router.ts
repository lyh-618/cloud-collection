import { createRouter, createWebHistory } from 'vue-router'
import HomeView from './views/HomeView.vue'
import CategoryView from './views/CategoryView.vue'
import ContentDetailView from './views/ContentDetailView.vue'
import LoginView from './views/LoginView.vue'
import PublishView from './views/PublishView.vue'
import AdminView from './views/AdminView.vue'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: HomeView },
    { path: '/:category(film|dance|image|song|fanwork)', component: CategoryView },
    { path: '/content/:id(\\d+)', component: ContentDetailView },
    { path: '/login', component: LoginView },
    { path: '/publish', component: PublishView },
    { path: '/admin', component: AdminView },
  ],
})
