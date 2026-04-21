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

        <div class="page-header">
          <h1>创建任务</h1>
          <p>Create Transport Task</p>
        </div>

        <div class="card">

          <!-- ===== 订单 ===== -->
          <div class="section">
            <h3>订单信息</h3>

            <div class="form-group">
              <label>选择订单</label>
              <select v-model="form.order_id">
                <option value="">不绑定订单</option>
                <option v-for="o in orders" :key="o.id" :value="o.id">
                  {{ o.label }}
                </option>
              </select>
            </div>
          </div>

          <!-- ===== 基本信息 ===== -->
          <div class="section">
            <h3>任务信息</h3>

            <div class="grid">

              <div class="form-group">
                <label>运输员</label>
                <select v-model="form.assigned_to">
                  <option value="">请选择</option>
                  <option v-for="u in users" :key="u.id" :value="u.id">
                    {{ u.name }}
                  </option>
                </select>
              </div>

              <div class="form-group">
                <label>开始时间</label>
                <input type="datetime-local" v-model="form.start_time" />
              </div>

              <div class="form-group">
                <label>始发港</label>
                <select v-model="form.origin_port">
                  <option v-for="p in ports" :key="p.name" :value="p.name">
                    {{ p.name }}（{{ p.city }}）
                  </option>
                </select>
              </div>

              <div class="form-group">
                <label>目的港</label>
                <select v-model="form.destination_port">
                  <option v-for="p in ports" :key="p.name" :value="p.name">
                    {{ p.name }}（{{ p.city }}）
                  </option>
                </select>
              </div>

              <div class="form-group full">
                <label>任务状态</label>
                <select v-model="form.task_status">
                  <option value="待处理">待处理</option>
                  <option value="进行中">进行中</option>
                  <option value="已完成">已完成</option>
                  <option value="草稿">草稿</option>
                </select>
              </div>

            </div>
          </div>

          <!-- ===== 操作 ===== -->
          <div class="actions">
            <button class="btn primary" @click="submit">提交</button>
            <button class="btn warning" @click="reset">重置</button>
            <button class="btn ghost" @click="go('/task_management')">返回</button>
          </div>

        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../utils/common.js'

const router = useRouter()

const user = reactive({
  name: '',
  role: '',
  avatar: ''
})
const ports = ref([])
const orders = ref([])

const form = ref({
  order_id: '',
  assigned_to: '',
  origin_port: '',
  destination_port: '',
  start_time: '',
  task_status: '待处理'
})

const load = async () => {
  const res = await api.get('/api/task/create/meta/')
  users.value = res.data.users
  ports.value = res.data.ports
  orders.value = res.data.orders
}
const loadUser = async () => {
  const res = await api.get('/api/user_info/')
  Object.assign(user, fixAvatar(res.data))
}
const submit = async () => {
  await api.post('/api/task/create/', form.value)
  alert('创建成功')
  router.push('/task_management')
}

const reset = () => {
  form.value = {
    order_id: '',
    assigned_to: '',
    origin_port: '',
    destination_port: '',
    start_time: '',
    task_status: '待处理'
  }
}

const go = (p) => router.push(p)

onMounted(() => {
  load()
  loadUser()
})
</script>

<style scoped>
/* ===== layout ===== */
.main {
  flex: 1;
  margin-left: 240px;
  background: #f4f6f9;
  min-height: 100vh;
}

.content {
  max-width: 1000px;
  margin: auto;
  padding: 30px;
}

/* ===== header ===== */
.page-header h1 {
  margin: 0;
}
.page-header p {
  color: #888;
  margin-bottom: 20px;
}

/* ===== card ===== */
.card {
  background: #fff;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.05);
}

/* ===== section ===== */
.section {
  margin-bottom: 25px;
}
.section h3 {
  margin-bottom: 15px;
  color: #1a3a5f;
  border-left: 4px solid #3182ce;
  padding-left: 10px;
}

/* ===== grid ===== */
.grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.full {
  grid-column: span 2;
}

/* ===== form ===== */
.form-group {
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 6px;
  font-weight: 500;
}

select, input {
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ddd;
  transition: 0.2s;
}

select:focus, input:focus {
  border-color: #3182ce;
  box-shadow: 0 0 0 2px rgba(49,130,206,0.2);
  outline: none;
}

/* ===== buttons ===== */
.actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 20px;
}

.btn {
  padding: 8px 18px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
}

.primary {
  background: #3182ce;
  color: #fff;
}

.warning {
  background: #ed8936;
  color: #fff;
}

.ghost {
  background: #e2e8f0;
}
</style>