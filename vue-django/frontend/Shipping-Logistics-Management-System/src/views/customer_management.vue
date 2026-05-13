<template>
  <div class="app">
    <!-- 侧边栏 -->
    <div class="sidebar">
      <div class="logo-container">
        <div class="logo">
          <i class="fas fa-ship"></i>
          <span class="logo-text">航运物流公司管理系统</span>
        </div>
      </div>

      <ul class="nav-links">
        <li><router-link to="/operator"><i class="fas fa-user-tag"></i><span class="link-text">报表统计</span></router-link></li>
        <li><router-link to="/customer" class="active"><i class="fas fa-user-tag"></i><span class="link-text">客户管理</span></router-link></li>
        <li><router-link to="/port"><i class="fas fa-user-tag"></i><span class="link-text">港口管理</span></router-link></li>
        <li><router-link to="/cargo"><i class="fas fa-box"></i><span class="link-text">货物管理</span></router-link></li>
        <li><router-link to="/order"><i class="fas fa-file-invoice"></i><span class="link-text">订单管理</span></router-link></li>
        <li><router-link to="/operator_update_profile"><i class="fas fa-cog"></i><span class="link-text">系统设置</span></router-link></li>
      </ul>
    </div>

    <!-- main -->
    <div class="main-content">

      <!-- header -->
      <div class="header">
        <h1>客户管理</h1>

        <div class="user-info">
          <img :src="user.avatar" />
          <div>
            <div>{{ user.name }}</div>
            <div style="font-size:12px;color:#999">{{ user.role }}</div>
          </div>
        </div>
      </div>

      <!-- search -->
      <div class="search-bar">
        <input v-model="keyword" placeholder="搜索姓名/电话/邮箱" />
        <button class="search-btn" @click="loadData(1)">搜索</button>
        <button class="btn-menu" @click="go('/create-customer')">创建客户</button>
      </div>

      <!-- table -->
      <div class="card">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>姓名</th>
              <th>邮箱</th>
              <th>电话</th>
              <th>地址</th>
              <th>操作</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="c in list" :key="c.customer_id">
              <td>{{ c.customer_id }}</td>
              <td>{{ c.customer_name }}</td>
              <td>{{ c.customer_email }}</td>
              <td>{{ c.customer_phone }}</td>
              <td>{{ c.customer_address }}</td>

              <td class="action-cell">
                <button class="btn-edit" @click="goEdit(c.customer_id)">编辑</button>
                <button class="btn-delete" @click="deleteCustomer(c.customer_id)">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- pagination -->
      <div class="pagination">
        <button @click="changePage(page-1)" :disabled="page<=1">上一页</button>

        <button
          v-for="p in pageRange"
          :key="p"
          @click="changePage(p)"
          :class="{active: p===page}"
        >
          {{ p }}
        </button>

        <button @click="changePage(page+1)" :disabled="page>=totalPages">下一页</button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { api,fixAvatar } from "../utils/common.js"
const router = useRouter()
const list = ref([])
const page = ref(1)
const totalPages = ref(1)
const keyword = ref('')

const user = reactive({ name: '', role: '', avatar: '' })
const defaultAvatar = 'https://via.placeholder.com/40'
const pageRange = ref([])
const buildPageRange = (cur, total) => {
  const range = []
  const start = Math.max(1, cur - 2)
  const end = Math.min(total, cur + 2)
  for (let i = start; i <= end; i++) range.push(i)
  pageRange.value = range
}

const loadData = async (p = 1) => {
  const res = await api.get('/api/customers/', {
    params: {
      page: p,
      keyword: keyword.value
    }
  })

  const data = res.data.data

  list.value = data.customers
  page.value = data.pagination.current_page
  totalPages.value = data.pagination.total_pages

  buildPageRange(page.value, totalPages.value)
}
const go = (path) => {
  router.push(path)
}
const changePage = (p) => {
  if (p < 1 || p > totalPages.value) return
  loadData(p)
}

const goEdit = (id) => {
  router.push(`/customer/edit/${id}`)
}

const deleteCustomer = async (id) => {
  if (!confirm('确定删除？')) return
  await api.delete(`/api/delete-customers/${id}/`)
  loadData(page.value)
}

onMounted(async () => {
  await loadData(1)
  const userRes = await api.get('/api/user_info/')
  user.value = fixAvatar(userRes.data)
  Object.assign(user, userRes.data)
  console.log(user)
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
  justify-content: center; 

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

.main-content {
  flex:1;
  padding:20px;
  margin-left:250px;
}

.header {
  display:flex;
  justify-content:space-between;
  margin-bottom:20px;
}

/* 搜索 */
.search-bar {
  display:flex;
  gap:10px;
  margin-bottom:20px;
}

.search-bar input {
  flex:1;
  padding:8px;
  border:1px solid #ccc;
  border-radius:6px;
}

.search-bar button {
  padding:8px 12px;
}

.search-bar .create {
  background:#38a169;
  color:white;
}

/* 卡片 */
.card {
  background:white;
  padding:10px;
  border-radius:8px;
  overflow-x:auto;
}

/* 表格核心 */
table {
  width:100%;
  border-collapse:collapse;
  table-layout:auto;
}

th, td {
  padding:10px;
  border-bottom:1px solid #eee;
  white-space: nowrap;  
}

/* 操作列 */
.action-cell {
  display:flex;
  align-items:center;
  gap:8px;
  flex-wrap:nowrap;
  white-space:nowrap;
}

/* 按钮 */
.btn-edit {
  background:#007bff;
  color:white;
  border:none;
  padding:4px 10px;
  border-radius:4px;
  cursor:pointer;
  white-space:nowrap;
}

.btn-delete {
  background:#e53e3e;
  color:white;
  border:none;
  padding:4px 10px;
  border-radius:4px;
  cursor:pointer;
  white-space:nowrap;
}

/* 分页 */
.pagination {
  margin-top:15px;
  display:flex;
  gap:5px;
}

.pagination button {
  padding:6px 10px;
}

.pagination .active {
  background:#007bff;
  color:white;
}
.logo{display:flex;align-items:center;font-weight:700;white-space: nowrap;  }
.logo i{margin-right:10px;color:var(--accent)}
</style>    