<template>
  <div class="layout">

    <!-- ===== 侧边栏 ===== -->
    <div class="sidebar">
      <div class="logo">航运物流公司管理系统</div>

      <ul>
        <li @click="go('/operator/report')">报表统计</li>
        <li @click="go('/operator/customer')">客户管理</li>
        <li @click="go('/operator/port')">港口管理</li>
        <li @click="go('/operator/cargo')">货物管理</li>
        <li class="active">订单管理</li>
        <li @click="go('/operator/profile')">个人设置</li>
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
const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  withCredentials: true,
})



const router = useRouter()

const orders = ref([])
const page = ref(1)
const total_pages = ref(1)
const keyword = ref('')

const user = reactive({ name: '', role: '', avatar: '' })

/* ===== 头像处理 ===== */
const fixAvatar = (u) => {
    return 'http://127.0.0.1:8000' + u.avatar
}

/* ===== 用户 ===== */
const loadUser = async () => {
  const res = await api.get("/api/user_info/")

  console.log("返回原始数据：", res.data)

  const data = res.data

  if (typeof data !== "object") {
    console.error("接口返回不是JSON，而是：", typeof data)
    return
  }

  data.avatar = fixAvatar(data)
  Object.assign(user, data)

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

//   console.log('接口返回：', res.data)

  // ⭐ 自动兼容两种后端结构
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
    await axios.delete(`/api/delete_order/${id}/`)

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
.layout {
  display: flex;
  height: 100vh;
}

/* ===== 侧边栏 ===== */
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  width: 220px;
  height: 100vh;
  background: #1a3a5f;
  color: white;
  padding: 20px;
}

.sidebar .logo {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 20px;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  padding: 12px;
  cursor: pointer;
  border-radius: 6px;
  transition: 0.2s;
}

.sidebar li:hover {
  background: rgba(255,255,255,0.1);
}

.sidebar .active {
  background: #3182ce;
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