import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/teams',
      name: 'teams',
      component: () => import('@/views/TeamsView.vue')
    },
    {
      path: '/retrospectives',
      name: 'retrospectives',
      component: () => import('@/views/RetrospectivesView.vue')
    },
    {
      path: '/retrospectives/:id',
      name: 'retrospective-detail',
      component: () => import('@/views/RetrospectiveDetailView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue')
    }
  ]
})

export default router 