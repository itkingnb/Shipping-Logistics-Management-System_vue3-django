<template>
  <div class="app">

    <!-- sidebar（保持一致） -->
    <div class="sidebar">
      <div class="logo-container">
        <div class="logo">
          <i class="fas fa-ship"></i>
          <span class="logo-text">航运物流公司管理系统</span>
        </div>
      </div>

      <ul class="nav-links">
        <li><router-link to="/operator">报表统计</router-link></li>
        <li><router-link to="/customer" class="active">客户管理</router-link></li>
        <li><router-link to="/port">港口管理</router-link></li>
        <li><router-link to="/cargo">货物管理</router-link></li>
        <li><router-link to="/order">订单管理</router-link></li>
        <li><router-link to="/settings">系统设置</router-link></li>
      </ul>
    </div>

    <!-- main -->
    <div class="main-content">

      <!-- header -->
      <div class="header">
        <h1>创建客户</h1>

        <div class="user-info">
          <img :src="user.avatar || defaultAvatar" />
          <div>
            <div>{{ user.name }}</div>
            <div style="font-size:12px;color:#999">{{ user.role }}</div>
          </div>
        </div>
      </div>

      <!-- alert -->
      <div v-if="msg.text" :class="['alert', msg.type]">
        {{ msg.text }}
      </div>

      <!-- form -->
      <div class="card">
        <form @submit.prevent="submitForm" class="form-grid">

        <div class="form-item">
          <label>客户姓名 *</label>
          <input v-model="form.customer_name" placeholder="请输入客户姓名" />
        </div>

        <div class="form-item">
          <label>手机号 *</label>
          <input v-model="form.customer_phone" placeholder="11位手机号" />
        </div>

        <div class="form-item">
          <label>邮箱</label>
          <input v-model="form.customer_email" placeholder="example@email.com" />
        </div>

        <div class="form-item full">
          <label>地址 *</label>
          <input v-model="form.customer_address" placeholder="详细地址" />
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-primary">保存客户</button>
          <button type="button" class="btn-secondary" @click="resetForm">重置</button>
          <button type="button" class="btn-back" @click="router.push('/customer')">
            返回
          </button>
        </div>

      </form>
      </div>

    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

const defaultAvatar = 'https://via.placeholder.com/40'

const user = reactive({
  name: '',
  role: '',
  avatar: ''
})

const form = reactive({
  customer_name: '',
  customer_phone: '',
  customer_email: '',
  customer_address: ''
})

const msg = reactive({
  text: '',
  type: ''
})

const showMsg = (text, type = 'success') => {
  msg.text = text
  msg.type = type === 'error' ? 'alert-danger' : 'alert-success'
  setTimeout(() => (msg.text = ''), 2500)
}

const resetForm = () => {
  form.customer_name = ''
  form.customer_phone = ''
  form.customer_email = ''
  form.customer_address = ''
}

const submitForm = async () => {
  try {
    if (!form.customer_name || !form.customer_phone || !form.customer_address) {
      showMsg('姓名、手机号、地址必填', 'error')
      return
    }

    if (form.customer_phone.length !== 11) {
      showMsg('手机号必须11位', 'error')
      return
    }

    await axios.post('/api/create_customer/', form)

    showMsg('客户创建成功')

    setTimeout(() => {
      router.push('/customer')
    }, 800)

  } catch (e) {
    showMsg('创建失败，请检查后端接口', 'error')
  }
}

onMounted(async () => {
  const res = await axios.get('/api/user_info/')
  Object.assign(user, res.data)
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

/* sidebar */
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  width: 220px;
  height: 100vh;
}
.sidebar {
  width: 250px;
  position: fixed;
  height: 100vh;
  background: #1a3a5f;
  color: white;
}

.main-content {
  margin-left: 250px;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.card {
  background: white;
  padding: 20px;
  border-radius: 8px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}

/* 单行铺满 */
.form-item.full {
  grid-column: 1 / -1;
}

.form-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-item label {
  font-size: 13px;
  color: #4a5568;
  font-weight: 600;
}

/* 输入框升级 */
.form-item input {
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  background: #f8fafc;
  transition: all 0.2s ease;
  font-size: 14px;
}

.form-item input:focus {
  outline: none;
  border-color: #3182ce;
  background: white;
  box-shadow: 0 0 0 3px rgba(49,130,206,0.15);
}

/* hover效果 */
.form-item input:hover {
  border-color: #90cdf4;
}

/* 按钮区 */
.form-actions {
  grid-column: 1 / -1;
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 10px;
}

/* 按钮升级 */
.btn-primary {
  background: linear-gradient(135deg, #3182ce, #2b6cb0);
  color: white;
  padding: 10px 18px;
  border-radius: 10px;
}

.btn-secondary {
  background: #a0aec0;
  color: white;
  padding: 10px 18px;
  border-radius: 10px;
}

.btn-back {
  background: #f6ad55;
  color: white;
  padding: 10px 18px;
  border-radius: 10px;
}

button:hover {
  transform: translateY(-1px);
  transition: 0.2s;
  opacity: 0.9;
}

.alert {
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 6px;
}

.alert-success {
  background: #e6ffed;
  color: #2e7d32;
}

.alert-danger {
  background: #ffe6e6;
  color: #c62828;
}
.logo{display:flex;align-items:center;font-weight:700;white-space: nowrap;  }
.logo i{margin-right:10px;color:var(--accent)}
</style>