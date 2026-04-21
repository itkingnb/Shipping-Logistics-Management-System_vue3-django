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
        <li><router-link to="/assign_orders"><i class="fas fa-clipboard-check"></i><span>订单指派</span></router-link></li>
        <li><router-link to="/task_management"><i class="fas fa-tasks"></i><span>任务管理</span></router-link></li>
        <li><router-link to="/fault"><i class="fas fa-exclamation-triangle"></i><span>通知中心</span></router-link></li>
        <li><router-link to="/appointer_profile" class="active"><i class="fas fa-cog"></i><span>个人设置</span></router-link></li>
      </ul>
    </div>

    <!-- main -->
    <div class="main-content">

      <div class="header">
        <h1>指派员信息维护</h1>

        <div class="user-info">
          <img :src="user.avatar || defaultAvatar" />
          <div>
            <div>{{ user.username || '指派员' }}</div>
            <div class="role">指派员</div>
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

          <!-- 表单 -->
          <div class="form-group">
            <label>用户ID</label>
            <input class="form-control" v-model="user.id" readonly />
          </div>

          <div class="form-group">
            <label>角色</label>
            <input class="form-control" value="指派员" readonly />
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
import { api, fixAvatar } from "../utils/common.js"
const router = useRouter()

const user = ref({})
const file = ref(null)
const preview = ref('')
const defaultAvatar = '/avatar.png'
const fileInput = ref(null)
 

/* 加载用户信息（改接口） */
const load = async () => {
  const res = await api.get('/api/appointer_get_profile/')
  if (res.data.success) {
    user.value = fixAvatar(res.data.data)
  }
}

/* 头像上传 */
const triggerFile = () => fileInput.value.click()

const onFileChange = (e) => {
  file.value = e.target.files[0]
  preview.value = URL.createObjectURL(file.value)
}

/* 提交修改（改接口） */
const submit = async () => {
  const form = new FormData()
  form.append('username', user.value.username)
  form.append('phone', user.value.phone)
  form.append('email', user.value.email)

  if (file.value) {
    form.append('avatar', file.value)
  }

  const res = await api.post('/api/appointer_update_profile/', form)

  if (res.data.success) {
    alert('更新成功')
    load()
  } else {
    alert(res.data.message)
  }
}

/* 退出 */
const logout = () => {
  localStorage.removeItem('user')
  router.push('/')
}

onMounted(load)
</script>