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
import Order_management from '../views/order_management.vue'
import Create_order from '../views/create_order.vue'
import Edit_order from '../views/edit_order.vue'
import Appointer from '../views/appointer.vue'
import Appointer_update_profile from '../views/appointer_update_profile.vue'
import Assign_orders from '../views/assign_orders.vue'
import Appointer_order from '../views/appointer_order.vue'
import Assign_order from '../views/assign_order.vue'
import Task_management from '../views/task_management.vue'
import Show_track from '../views/show_track.vue'
import Show_task from '../views/show_task.vue'
import Show_order from '../views/show_order.vue'
import Edit_task from '../views/edit_task.vue'
import Create_task from '../views/create_task.vue'
import Fault from '../views/fault.vue'
import Show_fault from '../views/show_fault.vue'
import Transporter from '../views/transporter.vue'
import Transporter_update_profile from '../views/transporter_update_profile.vue'
import Task_center from '../views/task_center.vue'
import Task_detail from '../views/task_detail.vue'
import Transporter_show_order from '../views/transporter_show_order.vue'
import Report_location from '../views/report_location.vue'
import Falut_center from '../views/falut_center.vue'
import Fault_detail from '../views/fault_detail.vue'
import Report_fault from '../views/report_fault.vue'


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
  { path: '/order', component: Order_management },
  { path: '/create-order', component: Create_order },
  {path: '/operator_update_profile',component:Operator_update_profile},
  {path: '/order/edit/:id',component: Edit_order },
  {path: '/appointer',component:Appointer},
  {path: '/appointer_update_profile',component:Appointer_update_profile},
  {path: '/assign_orders',component:Assign_orders},
  {path: '/appointer_order/:id',component:Appointer_order},
  {path: '/assign_order/:id',component:Assign_order},
  {path: '/task_management',component:Task_management},
  {path: '/show_track/:id',component:Show_track},
  {path: '/show_task/:id',component:Show_task},
  {path: '/show_order/:id',component:Show_order},
  {path: '/edit_task/:id',component:Edit_task},
  {path: '/create_task',component:Create_task},
  {path: '/fault',component:Fault},
  {path: '/fault/:id',component:Show_fault},
  {path: '/transporter',component:Transporter},
  {path: '/transporter_update_profile',component:Transporter_update_profile},
  {path: '/task_center',component:Task_center},
  {path: '/task_detail/:id',component:Task_detail},
  {path: '/transporter_show_order/:id',component:Transporter_show_order},
  {path: '/report_location',component:Report_location},
  {path: '/fault_center',component:Falut_center},
  {path: '/fault_detail/:id',component:Fault_detail},
  {path: '/report_fault',component:Report_fault},

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router