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
        <li><router-link to="/assign_orders"><i class="fas fa-clipboard-check"></i><span>订单指派</span></router-link></li>
        <li><router-link to="/task_management"><i class="fas fa-tasks"></i><span>任务管理</span></router-link></li>
        <li><router-link to="/fault"><i class="fas fa-exclamation-triangle"></i><span>通知中心</span></router-link></li>
        <li><router-link to="/appointer_update_profile" class="active"><i class="fas fa-cog"></i><span>系统设置</span></router-link></li>
      </ul>
    </div>

    <!-- main -->
    <div class="main-content">

      <div class="header">
        <h1>指派员信息维护</h1>

        <div class="user-info">
          <img :src="user.avatar || defaultAvatar" />
          <div>
            <div>{{ user.username || '指派员' }}</div>
            <div class="role">指派员</div>
          </div>
        </div>
      </div>

      <!-- 卡片 -->
      <div class="card">
        <div class="card-header">
          <h2><i class="fas fa-edit"></i> 基本信息</h2>
        </div>

        <div class="card-body">

          <!-- 头像 -->
          <div class="avatar-section">
            <div class="avatar-container">
              <img :src="preview || user.avatar || defaultAvatar" class="avatar-img"/>

              <button class="avatar-upload" @click="triggerFile">
                <i class="fas fa-camera"></i>
              </button>

              <input type="file" ref="fileInput" @change="onFileChange" hidden />
            </div>
          </div>

          <!-- 表单 -->
          <div class="form-group">
            <label>用户ID</label>
            <input class="form-control" v-model="user.id" readonly />
          </div>

          <div class="form-group">
            <label>角色</label>
            <input class="form-control" value="指派员" readonly />
          </div>

          <div class="form-group">
            <label>用户名 *</label>
            <input class="form-control" v-model="user.username" />
          </div>

          <div class="form-group">
            <label>电话 *</label>
            <input class="form-control" v-model="user.phone" />
          </div>

          <div class="form-group">
            <label>邮箱 *</label>
            <input class="form-control" v-model="user.email" />
          </div>

          <!-- 按钮 -->
          <div class="btn-row">
            <button class="btn btn-primary" @click="submit">保存修改</button>
            <button class="btn btn-danger" @click="logout">退出登录</button>
          </div>

        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { api, fixAvatar } from "../utils/common.js"
const router = useRouter()

const user = ref({})
const file = ref(null)
const preview = ref('')
const defaultAvatar = '/avatar.png'
const fileInput = ref(null)
 

/* 加载用户信息（改接口） */
const load = async () => {
  const res = await api.get('/api/appointer_get_profile/')
  if (res.data.success) {
    user.value = fixAvatar(res.data.data)
  }
}

/* 头像上传 */
const triggerFile = () => fileInput.value.click()

const onFileChange = (e) => {
  file.value = e.target.files[0]
  preview.value = URL.createObjectURL(file.value)
}

/* 提交修改（改接口） */
const submit = async () => {
  const form = new FormData()
  form.append('username', user.value.username)
  form.append('phone', user.value.phone)
  form.append('email', user.value.email)

  if (file.value) {
    form.append('avatar', file.value)
  }

  const res = await api.post('/api/appointer_update_profile/', form)

  if (res.data.success) {
    alert('更新成功')
    load()
  } else {
    alert(res.data.message)
  }
}

/* 退出 */
const logout = () => {
  localStorage.removeItem('user')
  router.push('/')
}

onMounted(load)
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