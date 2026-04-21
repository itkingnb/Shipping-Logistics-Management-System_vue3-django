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
        <li><router-link to="/appointer" class="active"><i class="fas fa-home"></i><span>指派记录</span></router-link></li>
        <li><router-link to="/assign_orders"><i class="fas fa-clipboard-check"></i><span>订单指派</span></router-link></li>
        <li><router-link to="/task_management"><i class="fas fa-tasks"></i><span>任务管理</span></router-link></li>
        <li><router-link to="/fault"><i class="fas fa-exclamation-triangle"></i><span>通知中心</span></router-link></li>
        <li><router-link to="/appointer_update_profile"><i class="fas fa-cog"></i><span class="link-text">系统设置</span></router-link></li>
      </ul>
    </div>

    <!-- 主内容 -->
    <div class="main-content">
      <!-- 顶部 -->
      <div class="header">
        <h1>航运物流公司管理系统</h1>
        <div class="user-info">
          <img :src="user.avatar || defaultAvatar" />
          <div>
            <div>{{ user.name }}</div>
            <div class="role">{{ user.role || '指派员' }}</div>
          </div>
        </div>
      </div>

      <!-- KPI -->
      <div class="kpi-container">
        <div class="kpi-card danger">
          <div class="kpi-title">待指派订单</div>
          <h2>{{ kpi.pending_orders_count }}</h2>
        </div>

        <div class="kpi-card">
          <div class="kpi-title">在途任务</div>
          <h2>{{ kpi.my_active_tasks_count }}</h2>
        </div>

        <div class="kpi-card warning">
          <div class="kpi-title">故障报告</div>
          <h2>{{ kpi.my_pending_faults }}</h2>
        </div>

        <div class="kpi-card success">
          <div class="kpi-title">累计完成</div>
          <h2>{{ kpi.my_completed_tasks }}</h2>
        </div>
      </div>

      <!-- 图表 -->
      <div class="chart-row">
        <div class="card">
          <h3>任务状态分布</h3>
          <div id="statusChart" class="chart"></div>
        </div>

        <div class="card quick">
          <router-link to="/assign_orders" class="btn">去指派新订单</router-link>
          <router-link to="/fault" class="btn danger">处理故障报告</router-link>
        </div>
      </div>

      <!-- 表格 -->
      <div class="card">
        <h3>最近任务</h3>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>运输员</th>
              <th>始发港</th>
              <th>目的港</th>
              <th>状态</th>
              <th>时间</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="task in recentTasks" :key="task.task_id">
              <td>#{{ task.task_id }}</td>
              <td>{{ task.assigned_to__username || '未指定' }}</td>
              <td>{{ task.origin_port }}</td>
              <td>{{ task.destination_port }}</td>
              <td>
                <span :class="statusClass(task.task_status)">
                  {{ task.task_status }}
                </span>
              </td>
              <td>{{ formatTime(task.assigned_time) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import * as echarts from 'echarts'
import { api, fixAvatar } from "../utils/common.js"

const kpi = ref({})
const pieData = ref([])
const recentTasks = ref([])
const user = reactive({ name: '', role: '', avatar: '' })

const defaultAvatar = 'https://via.placeholder.com/40'

const fetchData = async () => {
  const res = await api.get('/api/appointer/dashboard/')
  const data = res.data
  kpi.value = data
  pieData.value = data.pie_data
  recentTasks.value = data.recent_tasks
  initChart()
}

const loadUser = async () => {
  const res = await api.get('/api/user_info/')
  const fixed = fixAvatar(res.data)
  Object.assign(user, fixed)
  console.log(user)
}

const initChart = () => {
  const chart = echarts.init(document.getElementById('statusChart'))

  chart.setOption({
    tooltip: { trigger: 'item' },
    legend: { top: '5%' },
    series: [
      {
        type: 'pie',
        radius: ['45%', '70%'],
        itemStyle: {
          borderRadius: 8,
          borderColor: '#fff',
          borderWidth: 2
        },
        data: pieData.value
      }
    ]
  })
}

const formatTime = (t) => new Date(t).toLocaleString()

const statusClass = (status) => {
  if (status === '已完成') return 'badge success'
  if (status === '运输中') return 'badge warning'
  return 'badge'
}

onMounted(() => {
  fetchData()
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

.main-content {
  flex: 1;
  padding: 24px;
}

.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.role {
  font-size: 12px;
  color: #888;
}

/* KPI */
.kpi-container {
  display: grid;
  grid-template-columns: repeat(4,1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.kpi-card {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  border-left: 4px solid #3182ce;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  transition: 0.25s;
}

.kpi-card:hover {
  transform: translateY(-5px);
}

.kpi-title {
  font-size: 13px;
  color: #999;
}

.kpi-card h2 {
  margin-top: 8px;
  font-size: 26px;
}

.kpi-card.danger { border-color: #e53e3e; }
.kpi-card.warning { border-color: #d69e2e; }
.kpi-card.success { border-color: #38a169; }

/* 图表 */
.chart-row {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.chart {
  height: 320px;
}

/* 卡片 */
.card {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

/* 快捷按钮 */
.quick {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 15px;
}

.btn {
  padding: 16px;
  text-align: center;
  background: #3182ce;
  color: #fff;
  border-radius: 8px;
  transition: 0.2s;
}

.btn:hover {
  transform: translateY(-3px);
}

.btn.danger {
  background: #e53e3e;
}

/* 表格 */
table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px;
}

thead {
  background: #f7fafc;
}

tbody tr:hover {
  background: #f9fbfd;
}

/* 状态 */
.badge {
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
}

.success { background: #c6f6d5; }
.warning { background: #fef5e7; }
.danger { background: #fed7d7; }
</style>