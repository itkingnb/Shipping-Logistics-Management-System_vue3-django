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
          <div>
            <h1>任务详情</h1>
            <p>Task Detail</p>
          </div>

          <div class="user">
            <img :src="user.avatar || '/avatar.png'">
            <div>
              <div>{{ user.name }}</div>
              <small>{{ user.role }}</small>
            </div>
          </div>
        </div>

        <!-- ===== 任务信息 ===== -->
        <div class="card">
          <h3>任务 {{ task.task_id }}</h3>

          <table class="info-table">
            <tr><th>任务编号</th><td>{{ task.task_id }}</td></tr>
            <tr><th>指派人</th><td>{{ task.assigned_by || '-' }}</td></tr>
            <tr><th>执行人</th><td>{{ task.assigned_to || '未指派' }}</td></tr>
            <tr>
              <th>状态</th>
              <td><span :class="badgeClass(task.task_status)">{{ task.task_status }}</span></td>
            </tr>
            <tr><th>始发港</th><td>{{ task.origin_port }}</td></tr>
            <tr><th>目的港</th><td>{{ task.destination_port }}</td></tr>
            <tr><th>指派时间</th><td>{{ task.assigned_time }}</td></tr>
            <tr><th>开始时间</th><td>{{ task.start_time }}</td></tr>
          </table>
        </div>

        <!-- ===== 订单 ===== -->
        <div class="card">
          <h4>包含订单</h4>

          <table>
            <thead>
              <tr>
                <th>订单编号</th>
                <th>客户</th>
                <th>起点</th>
                <th>终点</th>
                <th>状态</th>
                <th>金额</th>
                <th>时间</th>
                <th>操作</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="o in orders" :key="o.order_id">
                <td>{{ o.order_id }}</td>
                <td>{{ o.customer }}</td>
                <td>{{ o.origin_port }}</td>
                <td>{{ o.destination_port }}</td>
                <td>
                  <span :class="orderBadge(o.order_status)">
                    {{ o.order_status }}
                  </span>
                </td>
                <td>{{ o.total_amount }}</td>
                <td>{{ o.created_at }}</td>
                <td>
                  <button class="btn blue" @click="goOrder(o.order_id)">
                    查看
                  </button>
                </td>
              </tr>

              <tr v-if="orders.length === 0">
                <td colspan="8" class="empty">暂无订单</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 返回 -->
        <div class="footer">
          <button class="btn" @click="go('/task_management')">返回</button>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute,useRouter } from 'vue-router'
import { api, fixAvatar } from '../utils/common.js'

const route = useRoute()
const router = useRouter()
const task = ref({})
const orders = ref([])
const user = reactive({ name: '', role: '', avatar: '' })

const load = async () => {
  const res = await api.get(`/api/task/${route.params.id}/`)
  if (res.data.success) {
    task.value = res.data.data.task
    orders.value = res.data.data.orders
  }
}

const loadUser = async () => {
  const res = await api.get('/api/user_info/')
  Object.assign(user, fixAvatar(res.data))
}

const badgeClass = (s) => {
  if (s === '已完成') return 'badge green'
  if (s === '运输中') return 'badge orange'
  return 'badge blue'
}

const orderBadge = (s) => {
  if (s === '已完成') return 'badge green'
  if (s === '待配送') return 'badge orange'
  if (s === '已取消') return 'badge gray'
  return 'badge blue'
}

const go = (p) => router.push(p)
const goOrder = (id) => router.push(`/show_order/${id}`)

onMounted(() => {
  load()
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

/* ===== main ===== */
.main {
  margin-left: 240px;
  width: 100%;
}

.content {
  max-width: 1100px;
  margin: 0px;
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
  width: 120px;
}

/* badge */
.badge {
  padding: 4px 10px;
  border-radius: 20px;
  color: white;
}
.green { background: #2ecc71; }
.orange { background: #f39c12; }
.blue { background: #3498db; }
.gray { background: #95a5a6; }

/* btn */
.btn {
  padding: 6px 12px;
  border-radius: 6px;
  background: #3182ce;
  color: white;
  border: none;
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