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
        <li><router-link to="/transporter"><i class="fas fa-home"></i><span>运输报表</span></router-link></li>
        <li><router-link to="/task_center"><i class="fas fa-clipboard-check"></i><span>任务中心</span></router-link></li>
        <li><router-link to="/report_location"><i class="fas fa-tasks"></i><span>位置上报</span></router-link></li>
        <li><router-link to="/fault_center"><i class="fas fa-exclamation-triangle"></i><span>故障上报</span></router-link></li>
        <li><router-link to="/transporter_update_profile" class="active"><i class="fas fa-cog"></i><span class="link-text">系统设置</span></router-link></li>
      </ul>
    </div>

    <!-- ===== 主内容 ===== -->
    <div class="main-content">
      <div class="header">
        <h1>运输员个人信息</h1>
        <div class="user-info">
          <img :src="preview || user.avatar || defaultAvatar" />
          <div>
            <div>{{ user.name || '运输员' }}</div>
            <div class="role">{{ user.role || '运输员' }}</div>
          </div>
        </div>
      </div>

      <!-- 卡片 -->
      <div class="card">
        <div class="card-header">
          <h2><i class="fas fa-id-card"></i> 基本信息</h2>
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

          <!-- 表单 -->
          <div class="form-group">
            <label>用户ID</label>
            <input class="form-control" v-model="users.id" readonly />
          </div>

          <div class="form-group">
            <label>角色</label>
            <input class="form-control" v-model="users.role" readonly />
          </div>

          <div class="form-group">
            <label>姓名 *</label>
            <input class="form-control" v-model="users.username" />
          </div>

          <div class="form-group">
            <label>联系电话 *</label>
            <input class="form-control" v-model="users.phone" />
          </div>

          <div class="form-group">
            <label>邮箱 *</label>
            <input class="form-control" v-model="users.email" />
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
import { ref,reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api, fixAvatar } from "../utils/common.js"

const router = useRouter()

const user = reactive({ name: '', role: '', avatar: '' })
const users = ref({
  id: '',
  role: '',
  username: '',
  phone: '',
  email: '',
  avatar: ''
})
const file = ref(null)
const preview = ref('')
const defaultAvatar = '/avatar.png'
const fileInput = ref(null)

const loadUser = async () => {
  const res = await api.get('/api/user_info/')
  const fixed = fixAvatar(res.data)
  Object.assign(user, fixed)
  console.log(user)
}
// 加载用户信息（运输员接口）
const load = async () => {
  const res = await api.get('/api/transporter_get_profile/')
  if (res.data.success) {
    users.value = fixAvatar(res.data.data)
  }
  console.log(users)
}

// 上传头像
const triggerFile = () => fileInput.value.click()

const onFileChange = (e) => {
  file.value = e.target.files[0]
  preview.value = URL.createObjectURL(file.value)
}

// 提交修改（改成运输员接口）
const submit = async () => {
  const form = new FormData()
  form.append('username', users.value.username)
  form.append('phone', users.value.phone)
  form.append('email', users.value.email)

  if (file.value) {
    form.append('avatar', file.value)
  }

  const res = await api.post('/api/transporter_update_profile/', form)

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

onMounted(() => {
  load()
  loadUser()
})
</script>