import { createRouter, createWebHistory } from 'vue-router'

import Login from '../views/login.vue'
import RetrievePassword from '../views/retrieve_password.vue'
import UserManagement from '../views/user_management.vue'
import Admin from '../views/admin.vue'
import Administrator_Update_Profile from '../views/administrator_update_profile.vue'
import Operator from '../views/operator.vue'
import Customer_management from '../views/customer_management.vue'
import Create_customer from '../views/create_customer.vue'
import Edit_customer from '../views/edit_customer.vue'
import Port_mangement from '../views/port_mangement.vue'
import Create_port from '../views/create_port.vue'
import Edit_port from '../views/edit_port.vue'
import Cargo_management from '../views/cargo_management.vue'
import Create_cargo from '../views/create_cargo.vue'
import Edit_cargo from '../views/edit_cargo.vue'
import Operator_update_profile from '../views/operator_update_profile.vue'


const routes = [
  {path: '/',component: Login},
  {path: '/retrieve',component: RetrievePassword},
  {path: '/admin',component: Admin},
  {path: '/user_management',component: UserManagement},
  {path: '/administrator_update_profile',component:Administrator_Update_Profile},
  {path: '/operator',component:Operator},
  { path: '/customer', component: Customer_management },
  { path: '/create-customer', component: Create_customer },
  {path: '/customer/edit/:id',component: Edit_customer },
  { path: '/port', component: Port_mangement },
  { path: '/create-port', component: Create_port },
  {path: '/port/edit/:id',component: Edit_port },
  { path: '/cargo', component:Cargo_management },
  { path: '/create-cargo', component: Create_cargo },
  {path: '/cargo/edit/:id',component: Edit_cargo },
  { path: '/order', component: Operator },
  { path: '/settings', component: Operator },
  {path: '/operator_update_profile',component:Operator_update_profile},
  
  // {path: '/appointer',component: () => import('../views/appointer.vue')},
  // {path: '/transporter',component: () => import('../views/transporter.vue')},
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router