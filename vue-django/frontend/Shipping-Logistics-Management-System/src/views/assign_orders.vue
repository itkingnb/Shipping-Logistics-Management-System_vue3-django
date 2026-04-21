<template>
  <div class="layout">

    <!-- sidebar -->
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
        <h1>订单指派</h1>
        <div class="user-info">
          <img :src="user.avatar || defaultAvatar">
          <div>
            <div>{{ user.name }}</div>
            <div class="role">{{ user.role }}</div>
          </div>
        </div>
      </div>

      <!-- 搜索 -->
      <div class="search-container">
        <input v-model="keyword" placeholder="搜索港口 / 状态 / 客户名..." />
        <button @click="fetchOrders(1)">搜索</button>
      </div>

      <!-- 表格 -->
      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>订单编号</th>
              <th>客户</th>
              <th>始发港</th>
              <th>目的港</th>
              <th>状态</th>
              <th>金额</th>
              <th>创建时间</th>
              <th>更新时间</th>
              <th>操作</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="o in orders" :key="o.order_id">
              <td>#{{ o.order_id }}</td>
              <td>{{ o.customer_name }}</td>
              <td>{{ o.origin_port }}</td>
              <td>{{ o.destination_port }}</td>
              <td>{{ o.order_status }}</td>
              <td>{{ o.total_amount }}</td>
              <td>{{ o.created_at }}</td>
              <td>{{ o.updated_at }}</td>
              <td class="action">
                <button class="btn view" @click="view(o.order_id)">查看</button>
                <button v-if="canAssign(o)" class="btn assign" @click="assign(o.order_id)">指派</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 分页 -->
      <div class="pagination">
        <button v-if="page>1" @click="fetchOrders(page-1)">«</button>
        <span>第 {{ page }} / {{ totalPages }} 页</span>
        <button v-if="page<totalPages" @click="fetchOrders(page+1)">»</button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref,reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api, fixAvatar } from "../utils/common.js"

const router = useRouter()

const orders = ref([])
const page = ref(1)
const totalPages = ref(1)
const keyword = ref('')

const user = reactive({ name: '', role: '', avatar: '' })

const defaultAvatar = '/avatar.png'

const fetchOrders = async (p = 1) => {
  const res = await api.get('/api/assign_orders/', {
    params: { page: p, keyword: keyword.value }
  })

  if (res.data.success) {
    orders.value = res.data.data
    page.value = res.data.pagination.page
    totalPages.value = res.data.pagination.total_pages
  }
}

const loadUser = async () => {
  const res = await api.get('/api/user_info/')
  const fixed = fixAvatar(res.data)
  Object.assign(user, fixed)
  console.log(user)
}

const view = (id) => router.push(`/appointer_order/${id}`)
const assign = (id) => router.push(`/assign_order/${id}`)

const canAssign = (o) =>
  o.order_status !== '运输中' && o.order_status !== '已完成'

onMounted(() => {
  fetchOrders()
  loadUser()
})
</script>

<style scoped>
html, body {
  margin: 0;
  padding: 0;
}

.app {
  display: flex;
}

/* ===== 侧边栏整体 ===== */
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

/* ===== logo ===== */
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

/* ===== 菜单 ===== */
.nav-links {
  list-style: none;
  padding: 10px 0;
  margin: 0;
}

/* 每一项 */
.nav-links li {
  width: 100%;
}

/* 链接（重点） */
.nav-links a {
  display: flex;
  align-items: center;
  justify-content: center;   /* ✅ 文字整体居中 */

  width: 100%;
  height: 48px;

  color: rgba(255,255,255,0.8);
  text-decoration: none;

  transition: all 0.2s;
}

/* 图标 */
.nav-links i {
  margin-right: 8px;
}

/* hover */
.nav-links a:hover {
  background: rgba(255,255,255,0.1);
  color: #fff;
}

/* active（整行高亮） */
.nav-links a.active {
  background: rgba(255,255,255,0.15);
  color: #fff;
  border-left: 4px solid #3182ce;
}
/**/


/* ===== header ===== */
.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

/* ===== 搜索 ===== */
.search-container {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  width: 100%;
}

.search-container input {
  flex: 1;
  padding: 10px;
}

.search-container button {
  padding: 10px 20px;
  background: #3182ce;
  color: white;
  border: none;
}

/* ===== 表格修复（重点） ===== */
.table-wrapper {
  overflow-x: auto; /* 防止撑歪 */
}

table {
  width: 100%;
  background: white;
  border-collapse: collapse;
  white-space: nowrap; /* 不换行 */
}

th, td {
  padding: 12px;
  border-bottom: 1px solid #eee;
}

thead {
  background: #f7fafc;
}

/* ===== 按钮 ===== */
.action {
  display: flex;
  gap: 8px;
}

.btn {
  padding: 5px 10px;
  border: none;
  color: white;
  cursor: pointer;
}

.view {
  background: #17a2b8;
}

.assign {
  background: #28a745;
}

/* ===== 分页 ===== */
.pagination {
  margin-top: 20px;
  text-align: center;
}

</style>