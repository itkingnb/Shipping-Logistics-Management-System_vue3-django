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
            <h1>任务管理</h1>
            <p>Task Dashboard</p>
          </div>

          <div class="user">
            <img :src="user.avatar || defaultAvatar">
            <div>
              <div>{{ user.name }}</div>
              <small>{{ user.role }}</small>
            </div>
          </div>
        </div>

        <!-- toolbar -->
        <div class="toolbar">
          <div class="left">
            <input v-model="keyword" placeholder="搜索任务..." />
            <button class="btn primary" @click="search">搜索</button>
          </div>

          <button class="btn create" @click="go('/create_task')">
            + 创建任务
          </button>
        </div>

        <!-- table -->
        <div class="card">
          <div class="card-header">
            <span>任务列表</span>
            <span class="count">当前页 {{ tasks.length }} 条</span>
          </div>

          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>创建者</th>
                <th>指派给</th>
                <th>时间</th>
                <th>状态</th>
                <th>操作</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="t in tasks" :key="t.task_id">
                <td class="id">#{{ t.task_id }}</td>
                <td>{{ t.assigned_by }}</td>
                <td>{{ t.assigned_to }}</td>
                <td>{{ t.assigned_time }}</td>

                <td>
                  <span :class="badgeClass(t.task_status)">
                    {{ t.task_status }}
                  </span>
                </td>

                <td class="actions">
                  <button class="btn blue" @click="goTrack(t.task_id)">轨迹</button>
                  <button class="btn green" @click="goDetail(t.task_id)">详情</button>
                  <button
                    v-if="t.task_status !== '运输中' && t.task_status !== '已完成'"
                    class="btn orange"
                    @click="goEdit(t.task_id)"
                  >
                    编辑
                  </button>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- ✅ 分页 -->
          <div class="pagination">
            <button 
              class="btn" 
              :disabled="page === 1"
              @click="changePage(page - 1)"
            >
              上一页
            </button>

            <span class="page-info">
              第 {{ page }} / {{ totalPages }} 页
            </span>

            <button 
              class="btn" 
              :disabled="page === totalPages"
              @click="changePage(page + 1)"
            >
              下一页
            </button>
          </div>

        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api, fixAvatar } from '../utils/common.js'

const router = useRouter()

const tasks = ref([])
const keyword = ref('')

const page = ref(1)
const totalPages = ref(1)

const user = reactive({ name: '', role: '', avatar: '' })
const defaultAvatar = '/avatar.png'

const load = async () => {
  const res = await api.get('/api/tasks/', {
    params: {
      keyword: keyword.value,
      page: page.value
    }
  })
  if (res.data.success) {
    tasks.value = res.data.data.list
    totalPages.value = res.data.data.total_pages
  }
}

const search = () => {
  page.value = 1   // ✅ 搜索重置到第一页
  load()
}

const changePage = (p) => {
  if (p < 1 || p > totalPages.value) return
  page.value = p
  load()
}

const loadUser = async () => {
  const res = await api.get('/api/user_info/')
  Object.assign(user, fixAvatar(res.data))
}

const go = (p) => router.push(p)
const goTrack = (id) => router.push(`/show_track/${id}`)
const goDetail = (id) => router.push(`/show_task/${id}`)
const goEdit = (id) => router.push(`/edit_task/${id}`)

const badgeClass = (s) => {
  if (s === '已完成') return 'badge green'
  if (s === '运输中') return 'badge blue'
  if (s === '待处理') return 'badge orange'  // ✅ 修复
  return 'badge gray'
}

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

/* main */
.main {
  margin-left: 240px;
  padding: 30px 0;
}

.content {
  max-width: 1200px;
  margin: auto;
}

/* header */
.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

/* toolbar */
.toolbar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

input {
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ddd;
}

/* card */
.card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.06);
}

.card-header {
  padding: 15px;
  display: flex;
  justify-content: space-between;
}

/* table */
table {
  width: 100%;
}

th {
  background: #f7fafc;
  padding: 12px;
}

td {
  padding: 12px;
  border-bottom: 1px solid #eee;
}

/* btn */
.btn {
  padding: 6px 12px;
  border-radius: 6px;
  color: white;
  border: none;
  cursor: pointer;
}

.primary { background: #3182ce; }
.create { background: linear-gradient(135deg,#3182ce,#2c5282); }

.blue { background: #3498db; }
.green { background: #2ecc71; }
.orange { background: #f39c12; }

/* badge */
.badge {
  padding: 4px 10px;
  border-radius: 20px;
  color: white;
}
.gray { background: #95a5a6; }

/* 分页 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  padding: 20px;
}

.page-info {
  font-weight: bold;
}

.pagination .btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

/* user */
.user img {
  width: 32px;
  height: 32px;
  border-radius: 50%;
}
</style>