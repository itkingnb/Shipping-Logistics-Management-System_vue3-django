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
        <li><router-link to="/transporter"><i class="fas fa-home"></i><span>运输报表</span></router-link></li>
        <li><router-link to="/task_center" class="active"><i class="fas fa-clipboard-check"></i><span>任务中心</span></router-link></li>
        <li><router-link to="/report_location"><i class="fas fa-tasks"></i><span>位置上报</span></router-link></li>
        <li><router-link to="/fault_center"><i class="fas fa-exclamation-triangle"></i><span>故障上报</span></router-link></li>
        <li><router-link to="/transporter_update_profile"><i class="fas fa-cog"></i><span class="link-text">系统设置</span></router-link></li>
      </ul>
    </div>

    <!-- ===== 主内容 ===== -->
    <div class="main-content">

      <!-- header -->
      <div class="header">
        <h1>运输员控制台</h1>
        <div class="user-info">
          <img :src="user.avatar || defaultAvatar" />
          <div>
            <div>{{ user.name }}</div>
            <div class="role">{{ user.role }}</div>
          </div>
        </div>
      </div>

      <!-- 任务列表 -->
      <div class="card">
        <div class="card-header">
          <h2>任务列表</h2>
        </div>

        <div class="card-body">
          <table class="table">
            <thead>
              <tr>
                <th>任务编号</th>
                <th>始发港</th>
                <th>到达港</th>
                <th>任务时间</th>
                <th>指派员</th>
                <th>状态</th>
                <th>操作</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="task in (tasks || [])" :key="task.task_id">
                <td>{{ task.task_id }}</td>
                <td>{{ task.origin_port }}</td>
                <td>{{ task.destination_port }}</td>
                <td>{{ task.assigned_time }}</td>
                <td>{{ task.assigned_by }}</td>

                <!-- 状态 -->
                <td>
                  <span :class="statusClass(task.status)">
                    {{ task.status }}
                  </span>
                </td>

                <!-- 操作 -->
                <td>
                  <button class="btn btn-info" @click="view(task.task_id)">
                    查看
                  </button>

                  <button
                    v-if="task.status === '待处理'"
                    class="btn btn-success"
                    @click="accept(task.task_id)"
                  >
                    接受
                  </button>
                </td>
              </tr>

              <tr v-if="!tasks || tasks.length === 0">
                <td colspan="7" class="empty">暂无任务</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { api, fixAvatar } from "../utils/common.js"

const router = useRouter()

const tasks = ref([])
const user = reactive({ name: '', role: '', avatar: '' })
const defaultAvatar = '/avatar.png'

// 获取用户
const loadUser = async () => {
  const res = await api.get('/api/user_info/')
  Object.assign(user, fixAvatar(res.data))
}

// 获取任务
const loadTasks = async () => {
  try {
    const res = await api.get('/api/task_center/')
    // console.log(res)
    tasks.value = res.data.data || []   // ⭐关键兜底
    // console.log(tasks)
  } catch (e) {
    console.error(e)
    tasks.value = []                     // ⭐防炸
  }
}

// 状态颜色
const statusClass = (status) => {
  if (status === '待处理') return 'badge status-pending'
  if (status === '运输中') return 'badge status-running'
  if (status === '已完成') return 'badge status-done'
  return 'badge'
}

// 查看详情
const view = (id) => {
  router.push(`/task_detail/${id}`)
}

// 接受任务
const accept = async (id) => {
  await api.post(`/api/accept_task/${id}/`)
  loadTasks()
}

onMounted(() => {
  loadUser()
  loadTasks()
})
</script>

<style scoped>
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

/* ===== 主体 ===== */
.main-content {
  margin-left: 240px;
  padding: 16px 20px;   /* ❗从30改小 */
}

/* ===== Header ===== */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  margin-bottom: 25px;
  padding-bottom: 15px;

  border-bottom: 1px solid #e5e7eb;
}

.header h1 {
  font-size: 24px;
  font-weight: 600;
  color: #1a3a5f;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-info img {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  margin-right: 10px;
  border: 2px solid #3182ce;
}

.role {
  font-size: 12px;
  color: #718096;
}

/* ===== 卡片 ===== */
.card {
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.08);
  overflow: hidden;
}

.card-header {
  padding: 18px 24px;
  border-bottom: 1px solid #f1f5f9;
  background: linear-gradient(90deg, #e6f0ff, #f8fbff);
}

.card-header h2 {
  font-size: 18px;
  color: #1a3a5f;
  font-weight: 600;
}

.card-body {
  padding: 16px;   /* ❗从25改小 */
}

/* ===== 表格 ===== */
.table {
  border-spacing: 0 6px;  /* ❗原来10，缩小 */
}

.table thead th {
  padding: 8px;
  font-size: 13px;
}
.table tbody tr {
  background: #f9fafb;
  transition: all 0.2s;
  border-radius: 10px;
}

.table tbody tr:hover {
  background: #edf2f7;
  transform: scale(1.01);
}

.table td {
  padding: 10px 8px;   /* ❗更紧凑 */
  font-size: 13px;
}

/* ===== 状态标签 ===== */
.badge {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

/* 待处理（黄色） */
.status-pending {
  background: #fff7cc;
  color: #b7791f;
}

/* 运输中（蓝色） */
.status-running {
  background: #e6f0ff;
  color: #2b6cb0;
}

/* 已完成（绿色） */
.status-done {
  background: #e6fffa;
  color: #2f855a;
}

.warning {
  background: #fff3cd;
  color: #856404;
}

.info {
  background: #d1ecf1;
  color: #0c5460;
}

.success {
  background: #d4edda;
  color: #155724;
}

/* ===== 按钮 ===== */
.btn {
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 13px;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.btn-info {
  background: #3182ce;
  color: white;
}

.btn-info:hover {
  background: #2b6cb0;
  transform: translateY(-1px);
}

.btn-success {
  background: #38a169;
  color: white;
}

.btn-success:hover {
  background: #2f855a;
  transform: translateY(-1px);
}

/* ===== 空数据 ===== */
.empty {
  text-align: center;
  color: #a0aec0;
  padding: 20px;
  font-style: italic;
}
</style>