<template>
  <div class="layout">
    <!-- ===== 侧边栏 ===== -->
    <div class="sidebar">
      <div class="logo-container">
        <div class="logo">
          <i class="fas fa-ship"></i>
          <span class="logo-text">航运物流公司管理系统</span>
        </div>
      </div>

      <ul class="nav-links">
        <li><router-link to="/admin"><i class="fas fa-tachometer-alt"></i><span class="link-text">数据统计</span></router-link></li>
        <li><router-link to="/user_management"><i class="fas fa-user-tag"></i><span class="link-text">用户管理</span></router-link></li>
        <li><router-link to="/administrator_update_profile" class="active"><i class="fas fa-cog"></i><span class="link-text">系统设置</span></router-link></li>
      </ul>
    </div>

    <!-- ===== 主内容 ===== -->
    <div class="main-content">
      <!-- header -->
      <div class="header">
        <h1>个人信息维护</h1>
        <div class="user-info">
          <img :src="user.avatar || defaultAvatar" />
          <div>
            <div>{{ user.username || '管理员' }}</div>
            <div class="role">{{ user.role || '操作员' }}</div>
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

          <!-- ===== 表单（五行结构）===== -->
          <div class="form-group">
            <label>用户ID</label>
            <input class="form-control" v-model="user.id" readonly />
          </div>

          <div class="form-group">
            <label>角色</label>
            <input class="form-control" v-model="user.role" readonly />
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
import { api,fixAvatar } from "../utils/common.js"
const router = useRouter()

const user = ref({})
const file = ref(null)
const preview = ref('')
const defaultAvatar = '/avatar.png'
const fileInput = ref(null)

// 跳转
const go = (path) => router.push(path)


// 加载数据
const load = async () => {
  try {
    const res = await api.get('/api/get_profile/')
    console.log('接口返回:', res)

    if (res.data.success) {
      const data = fixAvatar(res.data.data)
      console.log('处理后数据:', data)

      user.value = data
      localStorage.setItem('user', JSON.stringify(data))
    } else {
      console.log('接口返回失败:', res.data)
    }

  } catch (e) {
    console.error('请求报错:', e)
  }
}

// 选文件
const triggerFile = () => fileInput.value.click()

const onFileChange = (e) => {
  file.value = e.target.files[0]
  preview.value = URL.createObjectURL(file.value)
}

// 提交
const submit = async () => {
  const form = new FormData()
  form.append('username', user.value.username)
  form.append('phone', user.value.phone)
  form.append('email', user.value.email)

  if (file.value) {
    form.append('avatar', file.value)
  }

  const res = await api.post(
    'http://127.0.0.1:8000/api/administrator_update_profile/',
    form
  )

  if (res.data.success) {
    alert('更新成功')
    load()
  } else {
    alert(res.data.message)
  }
}

// 退出
const logout = () => {
  localStorage.removeItem('user')
  router.push('/')
}

onMounted(load)
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
}

/* ===== 布局 ===== */
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

/* main */
.main-content{
  margin-left:250px;
  padding:20px;
}

/* header */
.header{
  display:flex;
  justify-content:space-between;
  align-items:center;
  margin-bottom:25px;
  padding-bottom:15px;
  border-bottom:1px solid #e5e7eb;
}

.header h1{
  font-size:22px;
}

.user-info{
  display:flex;
  align-items:center;
}

.user-info img{
  width:40px;
  height:40px;
  border-radius:50%;
  margin-right:10px;
  border:2px solid var(--accent);
}

.role{
  font-size:12px;
  color:var(--gray);
}

/* card */
.card{
  background:#fff;
  border-radius:12px;
  box-shadow:0 8px 24px rgba(0,0,0,.08);
}

.card-header{
  padding:15px;
  border-bottom:1px solid #eee;
}

.card-body{
  padding:30px;
  display:flex;
  flex-direction:column;
  align-items:center;
}

/* avatar */
.avatar-section{
  margin-bottom:25px;
}

.avatar-container{
  position:relative;
  width:120px;
}

.avatar-img{
  width:120px;
  height:120px;
  border-radius:50%;
}

.avatar-upload{
  position:absolute;
  bottom:0;
  right:0;
  background:#3182ce;
  color:white;
  border-radius:50%;
  width:35px;
  height:35px;
  border:none;
  cursor:pointer;
}

/* form */
.form-group{
  width:100%;
  max-width:500px;
  margin-bottom:18px;
}

.form-group label{
  font-size:14px;
  margin-bottom:6px;
  display:block;
}

.form-control{
  width:100%;
  height:42px;
  padding:8px 12px;
  border:1px solid #d1d5db;
  border-radius:8px;
}

.form-control:focus{
  outline:none;
  border-color:#3182ce;
  box-shadow:0 0 0 3px rgba(49,130,206,.2);
}

/* buttons */
.btn-row{
  margin-top:20px;
}

.btn{
  padding:8px 18px;
  border:none;
  border-radius:8px;
  cursor:pointer;
  margin-right:10px;
}

.btn-primary{
  background:#3182ce;
  color:#fff;
}

.btn-danger{
  background:#e53e3e;
  color:#fff;
}
</style>