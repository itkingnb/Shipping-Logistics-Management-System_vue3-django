<template>
  <div class="layout">

    <!-- ===== 侧边栏（保持不变） ===== -->
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
        <li><router-link to="/report_location"><i class="fas fa-tasks"></i><span>位置上报</span></router-link></li>
        <li><router-link to="/fault_center" class="active"><i class="fas fa-exclamation-triangle"></i><span>故障上报</span></router-link></li>
        <li><router-link to="/transporter_update_profile"><i class="fas fa-cog"></i><span class="link-text">系统设置</span></router-link></li>
      </ul>
    </div>

    <!-- ===== 主体 ===== -->
    <div class="main">

      <!-- Header -->
      <div class="header">
        <h2>故障上报</h2>

        <div class="user">
          <img :src="user.avatar || defaultAvatar" />
          <div>
            <div>{{ user.name }}</div>
            <small>{{ user.role }}</small>
          </div>
        </div>
      </div>

      <!-- 卡片 -->
      <div class="card">

        <div class="form-group">
          <label>当前用户</label>
          <input :value="user.name" disabled />
        </div>

        <div class="form-group">
          <label>所属任务 *</label>
          <select v-model="form.task_id">
            <option value="">请选择任务</option>
            <option v-for="t in tasks" :key="t.task_id" :value="t.task_id">
              任务{{ t.task_id }}（{{ t.origin_port }} → {{ t.destination_port }}）
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>故障描述 *</label>
          <textarea v-model="form.fault_info" rows="4"></textarea>
        </div>

        <div class="form-group">
          <label>时间</label>
          <input :value="now" disabled />
        </div>

        <div class="actions">
          <button @click="submit">提交</button>
          <button class="secondary" @click="reset">重置</button>
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

const user = reactive({})
const tasks = ref([])

const form = reactive({
  task_id: '',
  fault_info: ''
})

const now = new Date().toLocaleString()
const defaultAvatar = '/avatar.png'

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
  if (!form.task_id || !form.fault_info) {
    alert('请填写完整')
    return
  }

  const formData = new FormData()
  formData.append('task_id', form.task_id)
  formData.append('fault_info', form.fault_info)

  const res = await api.post('/api/report_fault/', formData)

  if (res.data.success) {
    alert('提交成功')
    router.push('/fault_center')
  } else {
    alert(res.data.message)
  }
}

// 重置
const reset = () => {
  form.task_id = ''
  form.fault_info = ''
}

onMounted(() => {
  loadUser()
  loadTasks()
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
.main {
  margin-left: 240px;
  padding: 25px;
  background: #f4f7fb;
}

.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.user {
  display: flex;
  align-items: center;
  background: white;
  padding: 6px 12px;
  border-radius: 20px;
}

.user img {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  margin-right: 10px;
}

.card {
  background: white;
  padding: 25px;
  border-radius: 10px;
}

.form-group {
  margin-bottom: 15px;
}

input, select, textarea {
  width: 100%;
  padding: 8px;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 10px;
}

button {
  padding: 8px 16px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  background: #3182ce;
  color: white;
}

.secondary {
  background: #a0aec0;
}
</style>