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
          <h1>编辑任务</h1>

          <div class="user">
            <img :src="user.avatar || '/avatar.png'" />
            <div>
              <div>{{ user.name }}</div>
              <small>{{ user.role }}</small>
            </div>
          </div>
        </div>

        <!-- ===== 表单 ===== -->
        <div class="card">

          <div class="form-row">
            <label>任务ID</label>
            <input v-model="form.task_id" disabled />
          </div>

          <div class="form-row">
            <label>运输员</label>
            <select v-model="form.assigned_to">
              <option value="">请选择</option>
              <option v-for="u in users" :key="u.id" :value="u.id">
                {{ u.name }}
              </option>
            </select>
          </div>

          <div class="form-row">
            <label>始发港</label>
            <select v-model="form.origin_port">
              <option v-for="p in ports" :key="p.name">
                {{ p.name }}
              </option>
            </select>
          </div>

          <div class="form-row">
            <label>目的港</label>
            <select v-model="form.destination_port">
              <option v-for="p in ports" :key="p.name">
                {{ p.name }}
              </option>
            </select>
          </div>

          <div class="form-row">
            <label>开始时间</label>
            <input type="datetime-local" v-model="form.start_time" />
          </div>

          <div class="form-row">
            <label>状态</label>
            <select v-model="form.task_status">
              <option>待处理</option>
              <option>进行中</option>
              <option>已完成</option>
              <option>草稿</option>
            </select>
          </div>

          <!-- 按钮 -->
          <div class="btn-group">
            <button class="btn green" @click="submit">保存</button>
            <button class="btn orange" @click="reset">重置</button>
            <button class="btn" @click="goBack">返回</button>
          </div>

        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api, fixAvatar } from '../utils/common.js'

const route = useRoute()
const router = useRouter()

const user = reactive({ name: '', role: '', avatar: '' })

const form = reactive({task_id: '',assigned_to: '',origin_port: '',destination_port: '',start_time: '',task_status: ''})

const users = ref([])
const ports = ref([])

// ===== 加载任务 =====
const loadTask = async () => {
  const res = await api.get(`/api/edit_task/${route.params.id}/`)
  Object.assign(form, res.data)
}

// ===== 加载用户+港口 =====
const loadMeta = async () => {
  const res = await api.get('/api/task_meta/')
  users.value = res.data.users
  ports.value = res.data.ports
}

// ===== 用户 =====
const loadUser = async () => {
  const res = await api.get('/api/user_info/')
  Object.assign(user, fixAvatar(res.data))
}

// ===== 提交 =====
const submit = async () => {
  await api.post(
    `/api/task/${route.params.id}/update/`,
    form,
    {
      headers: {
        'Content-Type': 'application/json'
      }
    }
  )
  alert('修改成功')
  router.push('/task_management')
}

// ===== 重置 =====
const reset = () => loadTask()

// ===== 返回 =====
const goBack = () => {
  router.push(`/task_management`)
}

onMounted(() => {
  loadTask()
  loadMeta()
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

.main {
  margin-left: 240px;
}

.content {
  max-width: 1000px;
  margin: auto;
  padding: 30px;
}

.card {
  background: white;
  padding: 20px;
  border-radius: 10px;
}

.form-row {
  margin-bottom: 15px;
  display: flex;
  flex-direction: column;
}

.btn-group {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  background: #3182ce;
  color: white;
}

.green { background: #2ecc71; }
.orange { background: #f39c12; }
.user img {
  width: 32px;
  height: 32px;
  border-radius: 50%;
}
</style>