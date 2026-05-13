<template>
  <div class="layout">

    <!-- ===== 侧边栏（完全不动） ===== -->
    <div class="sidebar">
      <div class="logo-container">
        <div class="logo">
          <i class="fas fa-ship"></i>
          <span class="logo-text">航运物流公司管理系统</span>
        </div>
      </div>

      <ul class="nav-links">
        <li><router-link to="/transporter"><i class="fas fa-home"></i><span>运输报表</span></router-link></li>
        <li><router-link to="/task_center"><i class="fas fa-clipboard-check"></i><span>任务中心</span></router-link></li>
        <li><router-link to="/report_location" class="active"><i class="fas fa-tasks"></i><span>位置上报</span></router-link></li>
        <li><router-link to="/fault_center"><i class="fas fa-exclamation-triangle"></i><span>故障上报</span></router-link></li>
        <li><router-link to="/transporter_update_profile"><i class="fas fa-cog"></i><span class="link-text">系统设置</span></router-link></li>
      </ul>
    </div>

    <!-- ===== 主体 ===== -->
    <div class="main">

      <!-- Header -->
      <div class="header">
        <h2>位置上报</h2>

        <div class="user">
          <img :src="user.avatar || defaultAvatar" />
          <div>
            <div>{{ user.name }}</div>
            <small>{{ user.role }}</small>
          </div>
        </div>
      </div>

      <!-- ===== 表单卡片 ===== -->
      <div class="card">

        <h3 class="card-title">填写位置信息</h3>

        <div class="form-group">
          <label>当前用户</label>
          <input :value="user.name" disabled />
        </div>

        <div class="form-group">
          <label>选择任务</label>
          <select v-model="form.task_id">
            <option value="">请选择任务</option>
            <option
              v-for="t in tasks"
              :key="t.task_id"
              :value="t.task_id"
            >
              任务{{ t.task_id }}（{{ t.origin_port }} → {{ t.destination_port }}）
            </option>
          </select>
        </div>

        <div class="row">
          <div>
            <label>纬度</label>
            <input v-model="form.latitude" type="number" step="0.000001" placeholder="请输入纬度"/>
          </div>

          <div>
            <label>经度</label>
            <input v-model="form.longitude" type="number" step="0.000001" placeholder="请输入经度"/>
          </div>
        </div>

        <div class="form-group">
          <label>上报时间</label>
          <input :value="now" disabled />
        </div>

        <div class="actions">
          <button @click="router.push('/task_center')">返回</button>
          <button class="primary" @click="submit">提交上报</button>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api, fixAvatar } from '../utils/common'

const router = useRouter()

const tasks = ref([])
const user = reactive({})
const form = reactive({task_id: '',latitude: '',longitude: ''})

const defaultAvatar = '/avatar.png'
const now = new Date().toLocaleString()

// 用户
const loadUser = async () => {
  const res = await api.get('/api/user_info/')
  Object.assign(user, fixAvatar(res.data))
}

// 任务
const loadTasks = async () => {
  const res = await api.get('/api/running_tasks/')
  tasks.value = res.data.tasks || []
}

// 提交
const submit = async () => {
  if (!form.task_id || !form.latitude || !form.longitude) {
    alert("请填写完整")
    return
  }

  const formData = new FormData()
  formData.append('task_id', form.task_id)
  formData.append('latitude', form.latitude)
  formData.append('longitude', form.longitude)

  const res = await api.post('/api/report_location/', formData)

  if (res.data.success) {
    alert("上报成功")
    router.push('/task_center')
  } else {
    alert(res.data.message)
  }
}

onMounted(() => {
  loadUser()
  loadTasks()
})
</script>

<style scoped>
/* ===== 侧边栏（完全保留） ===== */
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

.nav-links li {
  width: 100%;
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
  color: #fff;
}

.nav-links a.active {
  background: rgba(255,255,255,0.15);
  color: #fff;
  border-left: 4px solid #3182ce;
}

/* ===== 主体优化 ===== */
.main {
  flex: 1;
  margin-left: 240px;
  padding: 30px;
  background: #f4f7fb;
}

/* Header */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.header h2 {
  font-size: 22px;
  color: #1a3a5f;
}

.user {
  display: flex;
  align-items: center;
  background: #fff;
  padding: 6px 12px;
  border-radius: 25px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

.user img {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  margin-right: 10px;
}

/* 卡片 */
.card {
  background: white;
  padding: 30px 40px;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.06);
  max-width: 800px;
  margin: 0 auto;
}

.card-title {
  margin-bottom: 20px;
  color: #1a3a5f;
}

/* 表单 */
.form-group {
  margin-bottom: 18px;
}

label {
  margin-bottom: 6px;
  display: block;
  color: #4a5568;
}

input, select {
  width: 100%;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #d1d5db;
}

input:focus, select:focus {
  outline: none;
  border-color: #3182ce;
  box-shadow: 0 0 0 3px rgba(49,130,206,0.15);
}

.row {
  display: flex;
  gap: 15px;
}

.row > div {
  flex: 1;
}

/* 按钮 */
.actions {
  display: flex;
  justify-content: space-between;
  margin-top: 25px;
}

.actions button {
  padding: 10px 22px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
}

.primary {
  background: linear-gradient(135deg, #3182ce, #2b6cb0);
  color: white;
}
</style>