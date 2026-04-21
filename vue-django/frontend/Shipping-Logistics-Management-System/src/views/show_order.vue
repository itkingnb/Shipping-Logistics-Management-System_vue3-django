<template>
  <div class="layout">

    <!-- ===== sidebar ===== -->
    <div class="sidebar">
      <div class="logo-container">
        <div class="logo">
          <i class="fas fa-ship"></i>
          <span class="logo-text">航运物流公司管理系统</span>
        </div>
      </div>

      <ul class="nav-links">
        <li><router-link to="/appointer"><i class="fas fa-home"></i><span>指派记录</span></router-link></li>
        <li><router-link to="/assign_orders"><i class="fas fa-clipboard-check"></i><span>订单指派</span></router-link></li>
        <li><router-link to="/task_management" class="active"><i class="fas fa-tasks"></i><span>任务管理</span></router-link></li>
        <li><router-link to="/fault"><i class="fas fa-exclamation-triangle"></i><span>通知中心</span></router-link></li>
        <li><router-link to="/appointer_update_profile"><i class="fas fa-cog"></i><span>系统设置</span></router-link></li>
      </ul>
    </div>

    <!-- ===== main ===== -->
    <div class="main">
      <div class="content">

        <!-- header -->
        <div class="header">
          <h1>订单详情</h1>

          <div class="user">
            <img :src="user.avatar || '/avatar.png'" />
            <div>
              <div>{{ user.name }}</div>
              <small>{{ user.role }}</small>
            </div>
          </div>
        </div>

        <!-- ===== 订单信息 ===== -->
        <div class="card">
          <h3>订单 {{ order.order_id }}</h3>

          <table class="info-table">
            <tr><th>订单编号</th><td>{{ order.order_id }}</td></tr>
            <tr><th>客户</th><td>{{ order.customer_name }}</td></tr>
            <tr><th>起始港口</th><td>{{ order.origin_port_name }}</td></tr>
            <tr><th>目的港口</th><td>{{ order.destination_port_name }}</td></tr>
          </table>
        </div>

        <!-- ===== 货物 ===== -->
        <div class="card">
          <h4>货物列表</h4>

          <table>
            <thead>
              <tr>
                <th>货物ID</th>
                <th>名称</th>
                <th>数量</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="c in cargos" :key="c.cargo_id">
                <td>{{ c.cargo_id }}</td>
                <td>{{ c.cargo_name }}</td>
                <td>{{ c.quantity }}</td>
              </tr>

              <tr v-if="cargos.length === 0">
                <td colspan="3" class="empty">暂无货物</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 返回 -->
        <div class="footer">
          <button class="btn" @click="goBack">返回</button>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api, fixAvatar } from '../utils/common.js'

const route = useRoute()
const router = useRouter()

const order = ref({})
const cargos = ref([])
const user = reactive({ name: '', role: '', avatar: '' })

// ===== 加载订单 =====
const loadOrder = async () => {
  const res = await api.get(`/api/order/${route.params.id}/`)
  order.value = res.data
  cargos.value = res.data.cargo_list || []
}

// ===== 用户 =====
const loadUser = async () => {
  const res = await api.get('/api/user_info/')
  Object.assign(user, fixAvatar(res.data))
}

// ===== 返回逻辑（关键）=====
const goBack = () => {
  if (route.query.from === 'task') {
    router.push(`/show_task/${route.query.task_id}`)
  } else {
    router.back()
  }
}

onMounted(() => {
  loadOrder()
  loadUser()
})
</script>

<style scoped>
html, body {
  margin: 0;
  padding: 0;
}

/* sidebar */
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  width: 240px;
  height: 100vh;
  background: #1a3a5f;
  color: #fff;
  display: flex;
  flex-direction: column;
}

.logo-container {
  padding: 20px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.logo {
  display: flex;
  align-items: center;
  font-weight: bold;
}

.logo i {
  margin-right: 10px;
  color: #3182ce;
}

.nav-links {
  list-style: none;
  padding: 10px 0;
  margin: 0;
}

.nav-links a {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 48px;
  color: rgba(255,255,255,0.8);
  text-decoration: none;
}

.nav-links a:hover {
  background: rgba(255,255,255,0.1);
}

.nav-links a.active {
  background: rgba(255,255,255,0.15);
  border-left: 4px solid #3182ce;
}

.main {
  margin-left: 240px;
}

.content {
  max-width: 1000px;
  margin: auto;
  padding: 30px;
}

/* header */
.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

/* card */
.card {
  background: white;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 10px;
}

/* table */
table {
  width: 100%;
}

th, td {
  padding: 10px;
  text-align: center;
}

.info-table th {
  text-align: left;
  width: 140px;
}

/* btn */
.btn {
  padding: 8px 16px;
  background: #3182ce;
  color: white;
  border: none;
  border-radius: 6px;
}

.footer {
  text-align: right;
}

.empty {
  color: #999;
}
.user img {
  width: 32px;
  height: 32px;
  border-radius: 50%;
}
</style>