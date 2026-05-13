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
        <li><router-link to="/transporter" class="active"><i class="fas fa-home"></i><span>运输报表</span></router-link></li>
        <li><router-link to="/task_center"><i class="fas fa-clipboard-check"></i><span>任务中心</span></router-link></li>
        <li><router-link to="/report_location"><i class="fas fa-tasks"></i><span>位置上报</span></router-link></li>
        <li><router-link to="/fault_center"><i class="fas fa-exclamation-triangle"></i><span>故障上报</span></router-link></li>
        <li><router-link to="/transporter_update_profile"><i class="fas fa-cog"></i><span class="link-text">系统设置</span></router-link></li>
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
      <div class="card">
        <div class="card-header">
          <h2>工作概览</h2>
          <span class="badge bg-primary">实时数据</span>
        </div>

        <div class="card-body">
          <div class="kpi-container">
            <div class="kpi-card">
              <div class="kpi-title">已接任务总数</div>
              <div class="kpi-value">{{ data.total_count }}</div>
              <div class="kpi-trend up">
                <i class="fas fa-history"></i> 历史累计
              </div>
            </div>

            <div class="kpi-card">
              <div class="kpi-title">已完成任务</div>
              <div class="kpi-value">{{ data.completed_count }}</div>
              <div class="kpi-trend up">
                <i class="fas fa-check-circle"></i>
                完成率 {{ data.completion_rate }}%
              </div>
            </div>

            <div class="kpi-card">
              <div class="kpi-title">当前在途货物</div>
              <div class="kpi-value warning">
                {{ data.transit_count }}
              </div>
              <div class="kpi-trend">
                <i class="fas fa-truck-moving"></i> 进行中
              </div>
            </div>

            <div class="kpi-card">
              <div class="kpi-title">累计上报故障</div>
              <div class="kpi-value danger">
                {{ data.fault_count }}
              </div>
              <div class="kpi-trend">
                <i class="fas fa-wrench"></i> 维护记录
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 表格 -->
      <div class="card mt-4">
        <div class="card-header">
          <h2>
            <i class="fas fa-road me-2"></i> 当前在途任务
          </h2>
          <button class="btn btn-outline" @click="go('/task_center')">
            去任务中心处理
          </button>
        </div>

        <div class="card-body">
          <table class="table">
            <thead>
              <tr>
                <th>任务ID</th>
                <th>起始港</th>
                <th>到达港</th>
                <th>指派员</th>
                <th>指派时间</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="task in (data.tasks || [])" :key="task.task_id">
                <td>#{{ task.task_id }}</td>
                <td>{{ task.origin_port }}</td>
                <td>{{ task.destination_port }}</td>
                <td>{{ task.assigned_by }}</td>
                <td>{{ task.assigned_time }}</td>
              </tr>

              <tr v-if="(data.tasks ?? []).length === 0">
                <td colspan="5" class="empty">
                  ☕ 当前没有任务
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { useRouter } from 'vue-router'
import { ref, reactive, onMounted } from 'vue'
import { api, fixAvatar } from "../utils/common.js"

const router = useRouter()
const user = reactive({ name: '', role: '', avatar: '' })
const defaultAvatar = 'https://via.placeholder.com/40'

const data = ref({
  total_count: 0,
  completed_count: 0,
  transit_count: 0,
  fault_count: 0,
  completion_rate: 0,
  tasks: [],
  user_info: {}
})
const loadUser = async () => {
  const res = await api.get('/api/user_info/')
  const fixed = fixAvatar(res.data)
  Object.assign(user, fixed)
  console.log(user)
}
const getData = async () => {
  try {
    const res = await api.get('/api/transporter/', {
      withCredentials: true
    })
    data.value = res.data
    
  } catch (err) {
    console.error(err)
  }
}

const go = (path) => {
  router.push(path)
}

onMounted(() => {
  getData()
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
  justify-content: center;   /*  文字整体居中 */

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

.app {
  display: flex;
  background: #f4f7fb;
  min-height: 100vh;
}

/* ===== 主内容 ===== */
.main-content {
  margin-left: 240px;
  padding: 25px;
  width: 100%;
}

/* ===== 顶部 ===== */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.header h1 {
  font-size: 22px;
  font-weight: 600;
  color: #1a3a5f;
}

/* ===== 用户信息 ===== */
.user-info {
  display: flex;
  align-items: center;
  background: #fff;
  padding: 8px 15px;
  border-radius: 30px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.user-info img {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  margin-right: 10px;
}

.role {
  font-size: 12px;
  color: #888;
}

/* ===== 卡片统一风格 ===== */
.card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 6px 18px rgba(0,0,0,0.05);
  margin-bottom: 25px;
  transition: all 0.2s;
}

.card:hover {
  transform: translateY(-2px);
}

/* ===== 卡片头 ===== */
.card-header {
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  font-size: 16px;
  font-weight: 600;
}

/* ===== KPI区域 ===== */
.kpi-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px,1fr));
  gap: 20px;
}

/* KPI卡片 */
.kpi-card {
  padding: 20px;
  border-radius: 10px;
  background: linear-gradient(135deg, #ffffff, #f7faff);
  border-left: 5px solid #3182ce;
  transition: all 0.2s;
}

.kpi-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.08);
}

.kpi-title {
  font-size: 13px;
  color: #888;
}

.kpi-value {
  font-size: 30px;
  font-weight: bold;
  margin: 8px 0;
}

.kpi-value.warning {
  color: #d69e2e;
}

.kpi-value.danger {
  color: #e53e3e;
}

.kpi-trend {
  font-size: 12px;
  color: #666;
}

/* ===== 表格 ===== */
.table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
}

/* 表头 */
.table thead {
  background: #f7f9fc;
}

.table th {
  padding: 12px;
  font-weight: 600;
  font-size: 14px;
  color: #1a3a5f;
  border-bottom: 1px solid #eee;
}

/* 表格内容 */
.table td {
  padding: 12px;
  font-size: 14px;
  border-bottom: 1px solid #f1f1f1;
}

/* hover效果 */
.table tbody tr:hover {
  background: #f9fbff;
}

/* 空状态 */
.empty {
  text-align: center;
  color: #aaa;
  padding: 30px;
}

/* ===== 按钮优化 ===== */
.btn {
  border-radius: 6px;
  padding: 6px 14px;
  cursor: pointer;
}

.btn-outline {
  border: 1px solid #3182ce;
  color: #3182ce;
  background: transparent;
}

.btn-outline:hover {
  background: #3182ce;
  color: #fff;
}
</style>