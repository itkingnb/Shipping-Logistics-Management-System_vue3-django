<template>
  <div class="app">

    <!-- ===== 侧边栏（不动） ===== -->
    <div class="sidebar">
      <div class="logo-container">
        <div class="logo">
          <i class="fas fa-ship"></i>
          <span class="logo-text">航运物流公司管理系统</span>
        </div>
      </div>

      <ul class="nav-links">
        <li><router-link to="/operator"><i class="fas fa-user-tag"></i><span class="link-text">报表统计</span></router-link></li>
        <li><router-link to="/customer"><i class="fas fa-user-tag"></i><span class="link-text">客户管理</span></router-link></li>
        <li><router-link to="/port" class="active"><i class="fas fa-user-tag"></i><span class="link-text">港口管理</span></router-link></li>
        <li><router-link to="/cargo"><i class="fas fa-box"></i><span class="link-text">货物管理</span></router-link></li>
        <li><router-link to="/order"><i class="fas fa-file-invoice"></i><span class="link-text">订单管理</span></router-link></li>
        <li><router-link to="/operator_update_profile"><i class="fas fa-cog"></i><span class="link-text">系统设置</span></router-link></li>
      </ul>
    </div>

    <!-- ===== 主体 ===== -->
    <div class="main">

      <!-- Header -->
      <div class="header card-shadow">
        <h2>创建港口</h2>

        <div class="user">
          <img :src="user.avatar || defaultAvatar" />
          <div>
            <div class="name">{{ user.name }}</div>
            <small>{{ user.role }}</small>
          </div>
        </div>
      </div>

      <!-- 表单卡片 -->
      <div class="card">

        <div class="card-header">
          <h3>港口信息填写</h3>
        </div>

        <div class="card-body">

          <form @submit.prevent="submitForm">

            <!-- 分组1 -->
            <div class="form-block">
              <div class="form-row">
                <input v-model="form.port_code" placeholder="港口代码" />
                <input v-model="form.port_name" placeholder="港口中文名" />
              </div>

              <div class="form-row">
                <input v-model="form.port_name_en" placeholder="英文名" />
                <input v-model="form.city" placeholder="城市" />
              </div>
            </div>

            <!-- 分组2 -->
            <div class="form-block">
              <div class="form-row">
                <input v-model="form.country" placeholder="国家" />
                <input v-model="form.longitude" type="number" placeholder="经度" />
              </div>

              <div class="form-row">
                <input v-model="form.latitude" type="number" placeholder="纬度" />
                <input v-model="form.contact_person" placeholder="联系人" />
              </div>
            </div>

            <!-- 分组3 -->
            <div class="form-block">
              <div class="form-row">
                <input v-model="form.contact_phone" placeholder="电话" />

                <select v-model="form.status">
                  <option value="启用">启用</option>
                  <option value="停用">停用</option>
                  <option value="维护中">维护中</option>
                </select>
              </div>
            </div>

            <!-- 按钮 -->
            <div class="button-group">
              <button class="btn submit">提交</button>
              <button type="reset" class="btn reset">重置</button>
              <button type="button" class="btn back" @click="goBack">返回</button>
            </div>

          </form>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { api, fixAvatar } from '../utils/common'

const router = useRouter()

const user = reactive({})
const defaultAvatar = '/avatar.png'

const form = reactive({
  port_code: '',
  port_name: '',
  port_name_en: '',
  city: '',
  country: '',
  longitude: '',
  latitude: '',
  contact_person: '',
  contact_phone: '',
  status: '启用'
})

const submitForm = async () => {
  try {
    await axios.post('/api/create_port/', form)
    alert('创建成功')
    router.push('/port')
  } catch (e) {
    alert('创建失败')
  }
}

const goBack = () => router.push('/port')

onMounted(async () => {
  const res = await api.get('/api/user_info/')
  Object.assign(user, fixAvatar(res.data))
})
</script>

<style scoped>
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
  justify-content: center;  

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
/* ===== 主体 ===== */
.main {
  flex: 1; 
  margin-left: 240px;
  padding: 30px;
  background: #f4f7fb;
}

/* ===== header ===== */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.card-shadow {
  background: white;
  padding: 15px 20px;
  border-radius: 12px;
  box-shadow: 0 6px 18px rgba(0,0,0,0.06);
}

.user {
  display: flex;
  align-items: center;
  background: #f8fafc;
  padding: 6px 12px;
  border-radius: 20px;
}

.user img {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  margin-right: 10px;
}

.name { font-weight: 500 }

/* ===== 卡片 ===== */
.card {
  background: white;
  border-radius: 14px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
  overflow: hidden;
}

.card-header {
  padding: 18px 25px;
  background: #f1f5f9;
  font-weight: 600;
}

.card-body {
  padding: 25px;
}

/* ===== 表单 ===== */
.form-block {
  margin-bottom: 20px;
}

.form-row {
  display: flex;
  gap: 15px;
  margin-bottom: 15px;
}

input, select {
  flex: 1;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  transition: all 0.2s;
}

/* 输入框 focus 动效 */
input:focus, select:focus {
  border-color: #3182ce;
  box-shadow: 0 0 0 3px rgba(49,130,206,0.15);
  outline: none;
}

/* ===== 按钮 ===== */
.button-group {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 20px;
}

.btn {
  padding: 10px 22px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

/* 提交 */
.submit {
  background: linear-gradient(135deg,#38a169,#2f855a);
  color: white;
}

.submit:hover {
  transform: translateY(-2px);
}

/* 重置 */
.reset {
  background: #ed8936;
  color: white;
}

/* 返回 */
.back {
  background: #e2e8f0;
}

/* hover */
.btn:hover {
  opacity: 0.9;
}

</style>