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
        <li><router-link to="/customer"><i class="fas fa-anchor"></i><span class="link-text">客户管理</span></router-link></li>
        <li><a class="active"><i class="fas fa-tachometer-alt"></i><span class="link-text">港口管理</span></a></li>
        <li><router-link to="/cargo"><i class="fas fa-box"></i><span class="link-text">货物管理</span></router-link></li>
        <li><router-link to="/order"><i class="fas fa-file-invoice"></i><span class="link-text">订单管理</span></router-link></li>
        <li><router-link to="/settings"><i class="fas fa-cog"></i><span class="link-text">系统设置</span></router-link></li>
      </ul>
    </div>

    <!-- main -->
    <div class="main-content">
      <div class="header">
        <h1>创建港口</h1>

        <div class="user-info">
          <img :src="user.avatar || defaultAvatar" />
          <div>
            <div>{{ user.name }}</div>
            <div style="font-size:12px;color:#999">{{ user.role }}</div>
          </div>
        </div>
      </div>

      <!-- card -->
      <div class="card">
        <div class="card-header">
          <h2>港口基本信息</h2>
        </div>

        <div class="card-body">
          <!-- 表单 -->
          <form @submit.prevent="submitForm">

            <div class="form-row">
              <div class="form-group">
                <label>港口代码 *</label>
                <input v-model="form.port_code" class="form-control" required />
              </div>

              <div class="form-group">
                <label>港口中文名 *</label>
                <input v-model="form.port_name" class="form-control" required />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>英文名 *</label>
                <input v-model="form.port_name_en" class="form-control" required />
              </div>

              <div class="form-group">
                <label>城市 *</label>
                <input v-model="form.city" class="form-control" required />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>国家 *</label>
                <input v-model="form.country" class="form-control" required />
              </div>

              <div class="form-group">
                <label>经度 *</label>
                <input v-model="form.longitude" type="number" step="0.000001" class="form-control" required />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>纬度 *</label>
                <input v-model="form.latitude" type="number" step="0.000001" class="form-control" required />
              </div>

              <div class="form-group">
                <label>联系人 *</label>
                <input v-model="form.contact_person" class="form-control" required />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>电话 *</label>
                <input v-model="form.contact_phone" class="form-control" required />
              </div>

              <div class="form-group">
                <label>状态 *</label>
                <select v-model="form.status" class="form-control">
                  <option value="启用">启用</option>
                  <option value="停用">停用</option>
                  <option value="维护中">维护中</option>
                </select>
              </div>
            </div>

            <!-- 按钮 -->
            <div class="button-group">
              <button class="btn btn-submit">提交</button>
              <button type="reset" class="btn btn-reset">重置</button>
              <button type="button" class="btn btn-back" @click="goBack">返回</button>
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
import { useRouter } from 'vue-router'

const router = useRouter()

const defaultAvatar = 'https://via.placeholder.com/40'

const user = reactive({
  name: '',
  role: '',
  avatar: ''
})

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
    console.error(e)
    alert('创建失败')
  }
}

const goBack = () => {
  router.push('/port')
}

onMounted(async () => {
  const res = await axios.get('/api/user_info/')
  Object.assign(user, res.data)
})
</script>

<style scoped>
/* 直接复用你原来的 CSS（略微精简） */
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
.sidebar { width:250px;background:#1a3a5f;color:#fff;position:fixed;height:100% }
.main-content { margin-left:250px;padding:20px;background:#edf2f7 }

.logo{display:flex;align-items:center;font-weight:700;white-space:nowrap}
.logo i{margin-right:10px;color:#3182ce}

.nav-links{list-style:none;padding:0}
.nav-links a{display:block;color:#fff;padding:10px;text-decoration:none}
.nav-links a.active{background:rgba(255,255,255,.1)}

.header{display:flex;justify-content:space-between;margin-bottom:20px}
.user-info{display:flex;align-items:center}
.user-info img{width:40px;height:40px;border-radius:50%;margin-right:10px}

.card{background:#fff;border-radius:8px}
.card-header{padding:15px;border-bottom:1px solid #eee}
.card-body{padding:20px}

.form-row{display:grid;grid-template-columns:1fr 1fr;gap:15px;margin-bottom:15px}
.form-control{padding:10px;border:1px solid #ddd;border-radius:6px}

.button-group{display:flex;justify-content:center;gap:10px;margin-top:20px}

.btn{padding:8px 18px;border:none;border-radius:6px;color:#fff;cursor:pointer}
.btn-submit{background:#38a169}
.btn-reset{background:#dd6b20}
.btn-back{background:#f59e0b}
</style>