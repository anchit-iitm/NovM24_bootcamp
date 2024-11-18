import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import registeration from '@/views/register.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/test',
    name: 'testRoute',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/test.vue')
  },
  {
    path: '/register',
    name: 'registerRoute',
    component: registeration
  },
  {
    path: '/login',
    name: 'loginRoute',
    component: () => import('@/views/login.vue')
  },
  {
    path: '/home',
    name: 'homeRoute',
    component: () => import('@/views/dashboard.vue')
  },
  {
    path: '/category/create',
    name: 'categoryCreateRoute',
    component: () => import('@/views/categoryCreate.vue')
  },
  {
    path: '/product/create',
    name: 'productCreateRoute',
    component: () => import('@/views/productCreate.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
