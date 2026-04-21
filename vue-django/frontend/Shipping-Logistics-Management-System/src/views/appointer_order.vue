<template>
  <div class="layout">
    <div class="sidebar">
        <div class="logo-container">
        <div class="logo">
            <i class="fas fa-ship"></i>
            <span class="logo-text">航运物流公司管理系统</span>
        </div>
        </div>

        <ul class="nav-links">
        <li><router-link to="/appointer"><i class="fas fa-home"></i><span>指派记录</span></router-link></li>
        <li><router-link to="/assign_orders" class="active"><i class="fas fa-clipboard-check"></i><span>订单指派</span></router-link></li>
        <li><router-link to="/task_management"><i class="fas fa-tasks"></i><span>任务管理</span></router-link></li>
        <li><router-link to="/fault"><i class="fas fa-exclamation-triangle"></i><span>通知中心</span></router-link></li>
        <li><router-link to="/appointer_update_profile"><i class="fas fa-cog"></i><span class="link-text">系统设置</span></router-link></li>
        </ul>
    </div>

    <!-- main -->
    <div class="main-content">

      <!-- header -->
      <div class="header">
        <h1>订单信息</h1>
      </div>

      <!-- 卡片 -->
      <div class="card">

        <!-- 基本信息 -->
        <div class="section">
          <h3>订单详情</h3>

          <div class="grid">
            <div>订单编号：{{ order.order_id }}</div>
            <div>客户名称：{{ order.customer_name }}</div>
            <div>始发港：{{ order.origin_port }}</div>
            <div>目的港：{{ order.destination_port }}</div>
            <div>创建时间：{{ order.created_at }}</div>
          </div>
        </div>

        <!-- 任务信息 -->
        <div v-if="order.task" class="section">
          <h3>任务信息</h3>

          <div class="grid">
            <div>任务ID：{{ order.task.task_id }}</div>
            <div>任务状态：{{ order.task.task_status }}</div>
          </div>
        </div>

        <!-- 货物 -->
        <div class="section">
          <h3>货物列表</h3>

          <table>
            <thead>
              <tr>
                <th>名称</th>
                <th>类型</th>
                <th>重量</th>
                <th>体积</th>
                <th>数量</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="c in order.cargos" :key="c.cargo_name">
                <td>{{ c.cargo_name }}</td>
                <td>{{ c.cargo_type }}</td>
                <td>{{ c.cargo_weight || '-' }}</td>
                <td>{{ c.cargo_volume || '-' }}</td>
                <td>{{ c.quantity }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 返回 -->
        <div class="btn-row">
          <button @click="goBack">返回</button>
        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref,reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { api, fixAvatar } from "../utils/common.js"

const user = reactive({ name: '', role: '', avatar: '' })

const route = useRoute()
const router = useRouter()

const order = ref({ cargos: [] })

const load = async () => {
  const id = route.params.id
  const res = await api.get(`/api/appointer_order/${id}/`)

  if (res.data.success) {
    order.value = res.data.data
  }
}
const loadUser = async () => {
  const res = await api.get('/api/user_info/')
  const fixed = fixAvatar(res.data)
  Object.assign(user, fixed)
  console.log(user)
}
const goBack = () => {
  router.back()
}
onMounted(() => {
  load()
  loadUser()
})
</script>

<style scoped>
.layout { display: flex; }

/* sidebar */
.sidebar {
  width: 220px;
  background: #1a3a5f;
  color: #fff;
  height: 100vh;
  position: fixed;
}

/* main */
.main-content {
  margin-left: 220px;
  padding: 20px;
  width: calc(100% - 220px);
}

/* header */
.header {
  margin-bottom: 20px;
}

/* card */
.card {
  background: #fff;
  padding: 25px;
  border-radius: 8px;
}

/* section */
.section {
  margin-bottom: 25px;
}

/* grid */
.grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

/* table */
table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #eee;
  white-space: nowrap;
}

/* 按钮 */
.btn-row {
  text-align: right;
}

button {
  padding: 8px 20px;
  background: #3182ce;
  color: #fff;
  border: none;
  border-radius: 5px;
}
</style>