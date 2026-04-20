<template>
  <div class="app">

    <!-- sidebar -->
    <div class="sidebar">
      <div class="logo-container">
        <div class="logo">
          <i class="fas fa-ship"></i>
          <span class="logo-text">航运物流公司管理系统</span>
        </div>
      </div>

      <ul class="nav-links">
        <li><router-link to="/operator"><i class="fas fa-user-tag"></i><span class="link-text">报表统计</span></router-link></li>
        <li><a class="active"><i class="fas fa-tachometer-alt"></i><span class="link-text">客户管理</span></a></li>
        <li><router-link to="/port"><i class="fas fa-anchor"></i><span class="link-text">港口管理</span></router-link></li>
        <li><router-link to="/cargo"><i class="fas fa-box"></i><span class="link-text">货物管理</span></router-link></li>
        <li><router-link to="/order"><i class="fas fa-file-invoice"></i><span class="link-text">订单管理</span></router-link></li>
        <li><router-link to="/settings"><i class="fas fa-cog"></i><span class="link-text">系统设置</span></router-link></li>
      </ul>
    </div>

    <!-- main -->
    <div class="main-content">

      <!-- header -->
      <div class="header">
        <h1>编辑客户</h1>

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

        <div class="card-header">
          <h2><i class="fas fa-user-edit"></i> 编辑客户基本信息</h2>
        </div>

        <div class="card-body">
          <form @submit.prevent="submit">

            <div class="form-row">
              <div class="form-group">
                <label>客户姓名 *</label>
                <input v-model="form.customer_name" class="form-control" />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>手机号 *</label>
                <input v-model="form.customer_phone" class="form-control" />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>邮箱</label>
                <input v-model="form.customer_email" class="form-control" />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>地址 *</label>
                <input v-model="form.customer_address" class="form-control" />
              </div>
            </div>

            <div style="text-align:center;margin-top:30px;">
              <button type="submit" class="btn btn-primary">
                <i class="fas fa-save"></i> 更新客户
              </button>

              <button type="button" class="btn btn-secondary" @click="reset">
                <i class="fas fa-undo"></i> 重置
              </button>

              <button type="button" class="btn btn-back" @click="$router.push('/customer')">
                返回客户管理
              </button>

              <button
                type="button"
                class="btn btn-danger"
                @click="deleteCustomer"
              >
                删除客户
              </button>
            </div>

          </form>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
import { api,fixAvatar } from "../utils/common.js"

const route = useRoute()
const router = useRouter()

const id = route.params.id

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
  setTimeout(() => (msg.text = ''), 2000)
}

/** 获取客户详情 */
const loadCustomer = async () => {
  const res = await api.get(`/api/customers/${id}/`)
  Object.assign(form, res.data)
}

/** 更新 */
const submit = async () => {
  try {
    if (!form.customer_name || !form.customer_phone || !form.customer_address) {
      showMsg('必填项不能为空', 'error')
      return
    }

    if (form.customer_phone.length !== 11) {
      showMsg('手机号必须11位', 'error')
      return
    }

    await api.put(`/api/edit-customers/${id}/`, form)

    showMsg('更新成功')

    setTimeout(() => {
      router.push('/customer')
    }, 800)

  } catch (e) {
    showMsg('更新失败', 'error')
  }
}

/** 删除 */
const deleteCustomer = async () => {
  if (!confirm('确定删除该客户？')) return
  await api.delete(`/api/delete-customers/${id}/`)
  router.push('/customer')
}

/** 重置 */
const reset = () => {
  loadCustomer()
}

onMounted(async () => {
  await loadCustomer()
  const userRes = await api.get('/api/user_info/')
  user.value = fixAvatar(userRes.data)
  Object.assign(user, userRes.data)
  console.log(user)
})
</script>

<style scoped>
/* ====== 你原版 CSS 直接搬过来（这里省略不改风格） ====== */
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
  border-radius: 8px;
  overflow: hidden;
}

.card-header {
  padding: 15px;
  background: #f7fafc;
  border-bottom: 1px solid #e2e8f0;
}

.card-body {
  padding: 20px;
}

.form-row {
  margin-bottom: 15px;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #cbd5e0;
  border-radius: 4px;
}

.btn {
  padding: 8px 14px;
  margin: 0 5px;
  border: none;
  cursor: pointer;
}

.btn-primary { background: #3182ce; color: white; }
.btn-secondary { background: #a0aec0; color: white; }
.btn-back { background: #f59e0b; color: white; }
.btn-danger { background: #e53e3e; color: white; }

.alert {
  padding: 10px;
  margin-bottom: 10px;
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