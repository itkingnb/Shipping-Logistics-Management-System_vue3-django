<template>
  <div class="layout">

    <!-- ===== 侧边栏 ===== -->
    <div class="sidebar">
      <div class="logo-container">
        <div class="logo">
          <i class="fas fa-ship"></i>
          <span class="logo-text">航运物流公司管理系统</span>
        </div>
      </div>

      <ul class="nav-links">
        <li><router-link to="/operator"><i class="fas fa-user-tag"></i><span class="link-text">报表统计</span></router-link></li>
        <li><router-link to="/customer"><i class="fas fa-user-tag"></i><span class="link-text">客户管理</span></router-link></li>
        <li><router-link to="/port"><i class="fas fa-anchor"></i><span class="link-text">港口管理</span></router-link></li>
        <li><router-link to="/cargo"><i class="fas fa-box"></i><span class="link-text">货物管理</span></router-link></li>
        <li><router-link to="/order" class="active"><i class="fas fa-file-invoice"></i><span class="link-text">订单管理</span></router-link></li>
        <li><router-link to="/operator_update_profile"><i class="fas fa-cog"></i><span class="link-text">系统设置</span></router-link></li>
      </ul>
    </div>

    <!-- ===== 主体 ===== -->
    <div class="main">

      <!-- header -->
      <div class="header">
        <h2>订单管理</h2>

        <div class="user">
          <img :src="user.avatar" />
          <div>
            <div>{{ user.name }}</div>
            <small>{{ user.role }}</small>
          </div>
        </div>
      </div>

      <!-- 搜索栏 -->
      <div class="toolbar">
        <input 
          v-model="keyword" 
          placeholder="搜索客户 / 港口 / 状态"
          class="search-input"
        />

        <button class="btn primary" @click="load">
         搜索
        </button>

        <button class="btn success" @click="go('create-order')">
         创建订单
        </button>
      </div>

      <!-- 表格 -->
      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>客户</th>
              <th>始发港</th>
              <th>目的港</th>
              <th>状态</th>
              <th>金额</th>
              <th>创建时间</th>
              <th>操作</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="item in orders" :key="item.order_id">
              <td>{{ item.order_id }}</td>
              <td>{{ item.customer_name }}</td>
              <td>{{ item.origin_port_name }}</td>
              <td>{{ item.destination_port_name }}</td>
              <td>
                <span :class="statusClass(item.order_status)">
                  {{ item.order_status }}
                </span>
              </td>
              <td>¥{{ item.total_amount }}</td>
              <td>{{ formatTime(item.created_at) }}</td>
                <td class="actions">
                <button class="btn edit" @click="edit(item.order_id)">
                    编辑
                </button>

                <button class="btn delete" @click="remove(item.order_id)">
                    删除
                </button>
                </td>
            </tr>

            <!-- 空数据 -->
            <tr v-if="!orders || orders.length === 0">
              <td colspan="8" class="empty">暂无数据</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 分页 -->
      <div class="pagination">
        <button class="btn" @click="changePage(page-1)" :disabled="page<=1">
          上一页
        </button>

        <span>{{ page }} / {{ total_pages }}</span>

        <button class="btn" @click="changePage(page+1)" :disabled="page>=total_pages">
          下一页
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, reactive,onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { api,fixAvatar } from "../utils/common.js"

const router = useRouter()

const orders = ref([])
const page = ref(1)
const total_pages = ref(1)
const keyword = ref('')

const user = reactive({ name: '', role: '', avatar: '' })

/* ===== 用户 ===== */
const loadUser = async () => {
  const userRes = await api.get('/api/user_info/')
  user.value = fixAvatar(userRes.data)
  Object.assign(user, userRes.data)
  console.log(user)
}

/* ===== 订单（兼容所有返回格式）===== */
const load = async () => {
  const res = await api.get('/api/orders/', {
    params: {
      page: page.value,
      keyword: keyword.value
    }
  })

  const data = res.data.data || res.data

  orders.value = data.list || []
  total_pages.value = data.total_pages || 1
  page.value = data.current_page || page.value
}

/* ===== 分页 ===== */
const changePage = (p) => {
  if (p < 1 || p > total_pages.value) return
  page.value = p
  load()
}

/* ===== 状态颜色 ===== */
const statusClass = (s) => {
  if (s === '已完成') return 'tag green'
  if (s === '运输中') return 'tag blue'
  return 'tag orange'
}

/* ===== 跳转 ===== */
const edit = (id) => {
  router.push(`/order/edit/${id}`)
}
const remove = async (id) => {
  if (!confirm('确定删除该订单？')) return

  try {
    await api.delete(`/api/delete_order/${id}/`)

    alert('删除成功')

    load()  // 重新加载列表

  } catch (err) {
    console.error(err)

    if (err.response?.data?.error) {
      alert(err.response.data.error)
    } else {
      alert('删除失败')
    }
  }
}
const go = (path) => router.push(path)

/* ===== 时间格式 ===== */
const formatTime = (t) => {
  if (!t) return '-'
  return t.replace('T', ' ').slice(0, 19)
}

onMounted(() => {
  loadUser()
  load()
})
</script>

<style scoped>
html, body {
  margin: 0;
  padding: 0;
}

/* ===== 布局 ===== */
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

/* ===== 主体 ===== */
.main {
  flex: 1;
  margin-left: 220px;
  padding: 20px;
  background: #f5f7fa;
  min-height: 100vh;
}

/* ===== header ===== */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.user {
  display: flex;
  align-items: center;
}

.user img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 10px;
}

/* ===== 搜索栏 ===== */
.toolbar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  align-items: center;
}

.search-input {
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 8px;
  width: 260px;
  outline: none;
  transition: 0.2s;
}

.search-input:focus {
  border-color: #3182ce;
  box-shadow: 0 0 0 2px rgba(49,130,206,0.2);
}

/* ===== 按钮 ===== */
.btn {
  padding: 8px 14px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap; /* ⭐防止换行 */
}

.btn.primary {
  background: #3182ce;
  color: white;
}

.btn.primary:hover {
  background: #2563eb;
}

.btn.success {
  background: #38a169;
  color: white;
  margin-left: auto;
}

.btn.success:hover {
  background: #2f855a;
}

/* 编辑按钮 */
.btn.edit {
  background: #3182ce;
  color: white;
}

.btn.edit:hover {
  background: #2563eb;
}

/* 删除按钮 */
.btn.delete {
  background: #e53e3e;
  color: white;
}

.btn.delete:hover {
  background: #c53030;
}

/* ===== 表格 ===== */
.table-wrapper {
  background: white;
  border-radius: 12px;
  overflow-x: auto;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  background: #f1f5f9;
  font-weight: 600;
  color: #2d3748;
}

th, td {
  padding: 12px;
  border-bottom: 1px solid #eee;
  text-align: left;

  white-space: nowrap;   /* ⭐关键：禁止换行 */
}

tr:hover {
  background: #f9fafb;
}

/* ===== 操作列（核心修复）===== */
.actions {
  display: flex;
  gap: 8px;
  align-items: center;
  white-space: nowrap; /* ⭐不换行 */
}

/* ===== 状态标签 ===== */
.tag {
  display: inline-flex;          /* ⭐关键：用flex居中 */
  align-items: center;
  justify-content: center;

  min-width: 64px;               /* ⭐统一宽度（核心） */
  height: 24px;                  /* ⭐统一高度 */

  padding: 0 8px;                /* 左右留白 */
  border-radius: 6px;

  color: white;
  font-size: 12px;
  line-height: 1;                /* ⭐防止文字上下偏 */
  white-space: nowrap;           /* 防止换行 */
}

.green { background: #38a169; }
.blue { background: #3182ce; }
.orange { background: #d69e2e; }

/* ===== 分页 ===== */
.pagination {
  margin-top: 20px;
  text-align: center;
}

.pagination .btn {
  margin: 0 5px;
}

/* ===== 空数据 ===== */
.empty {
  text-align: center;
  padding: 20px;
  color: #999;
}
</style>