import { createRouter, createWebHistory } from 'vue-router'

import Login from '../views/login.vue'
import RetrievePassword from '../views/retrieve_password.vue'
import UserManagement from '../views/user_management.vue'
import Admin from '../views/admin.vue'
import Administrator_Update_Profile from '../views/administrator_update_profile.vue'
import Operator from '../views/operator.vue'
const routes = [
  {path: '/',component: Login},
  {path: '/retrieve',component: RetrievePassword},
  {path: '/admin',component: Admin},
  {path: '/user_management',component: UserManagement},
  {path: '/administrator_update_profile',component:Administrator_Update_Profile},
  {path: '/operator',component:Operator},
  { path: '/customer', component: Operator },
  { path: '/port', component: Operator },
  { path: '/cargo', component: Operator },
  { path: '/order', component: Operator },
  { path: '/settings', component: Operator },
  // {path: '/appointer',component: () => import('../views/appointer.vue')},
  // {path: '/transporter',component: () => import('../views/transporter.vue')},
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router