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
      component: () => import('@/views/ManageTeamsView.vue')
    },
    {
      path: '/create-retrospectives',
      name: 'create-trospectives',
      component: () => import('@/views/CreateRetrospectivesView.vue')
    },
    {
      path: '/manage-retrospectives',
      name: 'manage-trospectives',
      component: () => import('@/views/ManageRetrospectivesView.vue')
    },
    {
      path: '/users',
      name: 'users',
      component: () => import('@/views/CreateUsersView.vue')
    },
    {
      path: '/retrospectives/:id',
      name: 'retrospective-detail',
      component: () => import('@/views/RetrospectiveDetailView.vue')
    },
    {
      path: '/run-retrospective/:id',
      name: 'run-retrospective',
      component: () => import('@/views/RunRetrospectiveView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue')
    }
  ]
})

export default router 