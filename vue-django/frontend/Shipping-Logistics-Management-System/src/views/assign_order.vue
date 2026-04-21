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
        <li><router-link to="/assign_orders" class="active"><i class="fas fa-clipboard-check"></i><span>订单指派</span></router-link></li>
        <li><router-link to="/task_management"><i class="fas fa-tasks"></i><span>任务管理</span></router-link></li>
        <li><router-link to="/fault"><i class="fas fa-exclamation-triangle"></i><span>通知中心</span></router-link></li>
        <li><router-link to="/appointer_update_profile"><i class="fas fa-cog"></i><span class="link-text">系统设置</span></router-link></li>
        </ul>
    </div>

    <!-- main -->
    <div class="main-content">

      <!-- header -->
      <div class="header">
        <h1>指派订单</h1>
        <div class="user-info">
          <img :src="user.avatar || defaultAvatar">
          <div>
            <div>{{ user.name }}</div>
            <div class="role">{{ user.role }}</div>
          </div>
        </div>
      </div>

      <!-- 卡片 -->
      <div class="card">

        <!-- 提示 -->
        <div v-if="msg" :class="['alert', success ? 'alert-success' : 'alert-danger']">
          {{ msg }}
        </div>

        <!-- 表单区域 -->
        <div class="form-grid">

          <!-- 当前订单 -->
          <div class="form-item full">
            <label>当前订单</label>
            <input
              class="input"
              :value="`订单 ${order.order_id} — ${order.customer_name}（${order.origin_port} → ${order.destination_port}）`"
              readonly
            />
          </div>

          <!-- 状态 -->
          <div class="form-item">
            <label>订单状态</label>
            <input class="input" :value="order.order_status" readonly />
          </div>

          <!-- 选择任务 -->
          <div class="form-item">
            <label>选择任务 *</label>
            <select v-model="selectedTask" class="input">
              <option value="">请选择任务</option>
              <option v-for="t in tasks" :key="t.task_id" :value="t.task_id">
                任务 {{ t.task_id }} — {{ t.assigned_to }}（{{ t.origin_port }} → {{ t.destination_port }}）
              </option>
            </select>
          </div>

        </div>

        <!-- 按钮 -->
        <div class="actions">
          <button class="btn submit" @click="submit">确认指派</button>
          <button class="btn back" @click="goBack">返回</button>
        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, reactive,onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api, fixAvatar } from '../utils/common.js'

const route = useRoute()
const router = useRouter()

const order = ref({})
const tasks = ref([])
const selectedTask = ref('')

const user = reactive({ name: '', role: '', avatar: '' })
const loadUser = async () => {
  const res = await api.get('/api/user_info/')
  const fixed = fixAvatar(res.data)
  Object.assign(user, fixed)
  console.log(user)
}
const msg = ref('')
const success = ref(false)

const defaultAvatar = '/avatar.png'

const load = async () => {
  const id = route.params.id
  const res = await api.get(`/api/assign_order/${id}/`)
  if (res.data.success) {
    order.value = res.data.data.order
    tasks.value = res.data.data.tasks
  }
  console.log(tasks)
}

const submit = async () => {
  if (!selectedTask.value) {
    msg.value = '请选择任务'
    success.value = false
    return
  }

  const id = route.params.id
  const form = new FormData()
  form.append('task_id', selectedTask.value)

  const res = await api.post(`/api/assign_order/${id}/submit/`, form)

  msg.value = res.data.message
  success.value = res.data.success

  if (res.data.success) {
    setTimeout(() => router.push('/assign_orders'), 1000)
  }
}

const goBack = () => {
  router.push('/assign_orders')
}

onMounted(() => {
  load()
  loadUser()
})
</script>

<style scoped>

/* ===== 布局 ===== */
.layout {
  display: flex;
}

/* ===== 侧边栏 ===== */
.sidebar {
  position: fixed;
  width: 240px;
  height: 100vh;
  background: #1a3a5f;
  color: white;
}

/* ===== 主区域 ===== */
.main-content {
  margin-left: 240px;
  flex: 1;
  padding: 30px;
  background: #edf2f7;
}

/* ===== header ===== */
.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30px;
}

/* ===== 卡片 ===== */
.card {
  max-width: 900px;
  margin: 0 auto;
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.08);
}

/* ===== 表单 grid ===== */
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

/* 占满一行 */
.full {
  grid-column: span 2;
}

/* ===== 表单项 ===== */
.form-item label {
  display: block;
  margin-bottom: 6px;
  font-weight: 500;
}

/* 输入框 */
.input {
  width: 100%;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ddd;

  /* ❗禁止换行 */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* ===== 按钮 ===== */
.actions {
  margin-top: 30px;
  display: flex;
  justify-content: space-between;
}

.btn {
  padding: 10px 25px;
  border-radius: 8px;
  border: none;
  color: white;
  cursor: pointer;
}

.submit {
  background: #38a169;
}

.back {
  background: #f59e0b;
}

/* ===== 提示 ===== */
.alert {
  padding: 12px;
  margin-bottom: 20px;
  border-radius: 8px;
}

.alert-success {
  background: #d4edda;
}

.alert-danger {
  background: #f8d7da;
}

</style>