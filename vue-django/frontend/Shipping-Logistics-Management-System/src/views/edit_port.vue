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
        <li><router-link to="/customer"><i class="fas fa-user-tag"></i><span class="link-text">客户管理</span></router-link></li>
        <li><router-link to="/port" class="active"><i class="fas fa-user-tag"></i><span class="link-text">港口管理</span></router-link></li>
        <li><router-link to="/cargo"><i class="fas fa-box"></i><span class="link-text">货物管理</span></router-link></li>
        <li><router-link to="/order"><i class="fas fa-file-invoice"></i><span class="link-text">订单管理</span></router-link></li>
        <li><router-link to="/operator_update_profile"><i class="fas fa-cog"></i><span class="link-text">系统设置</span></router-link></li>
      </ul>
    </div>

    <!-- main -->
    <div class="main-content">
      <div class="header">
        <h1>编辑港口</h1>
        <div class="user-info">
            <img :src="user.avatar || defaultAvatar" />
            <div>
            <div>{{ user.name }}</div>
            <div style="font-size:12px;color:#999">{{ user.role }}</div>
            </div>
        </div>
      </div>
      
        

      <div class="card">
        <div class="card-body">

          <!-- 表单 -->
          <div class="form-row">
            <input v-model="form.port_code" placeholder="港口代码" />
            <input v-model="form.port_name" placeholder="港口中文名" />
          </div>

          <div class="form-row">
            <input v-model="form.port_name_en" placeholder="英文名" />
            <input v-model="form.city" placeholder="城市" />
          </div>

          <div class="form-row">
            <input v-model="form.country" placeholder="国家" />
            <input v-model="form.longitude" placeholder="经度" />
          </div>

          <div class="form-row">
            <input v-model="form.latitude" placeholder="纬度" />
            <input v-model="form.contact_person" placeholder="联系人" />
          </div>

          <div class="form-row">
            <input v-model="form.contact_phone" placeholder="电话" />
            <select v-model="form.status">
              <option value="启用">启用</option>
              <option value="停用">停用</option>
            </select>
          </div>

          <!-- 按钮 -->
          <div class="btn-group">
            <button class="btn btn-success" @click="submit">提交</button>
            <button class="btn btn-danger" @click="remove">删除</button>
            <button class="btn btn-warning" @click="back">返回</button>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { reactive, onMounted } from "vue"
import axios from "axios"
import { useRoute, useRouter } from "vue-router"
import { api,fixAvatar } from "../utils/common.js"
const route = useRoute()
const router = useRouter()
const user = reactive({ name: '', role: '', avatar: '' })
const id = route.params.id

const form = reactive({
  port_code: "",
  port_name: "",
  port_name_en: "",
  city: "",
  country: "",
  longitude: "",
  latitude: "",
  contact_person: "",
  contact_phone: "",
  status: "启用"
})

/* ===== CSRF 工具 ===== */
function getCookie(name) {
  let value = null
  document.cookie.split(";").forEach(c => {
    const cookie = c.trim()
    if (cookie.startsWith(name + "=")) {
      value = decodeURIComponent(cookie.substring(name.length + 1))
    }
  })
  return value
}

/* ===== 加载数据 ===== */
const loadData = async () => {
  const res = await api.get(`/api/edit-ports/${id}/`)
  Object.assign(form, res.data)
}

/* ===== 提交 ===== */
const submit = async () => {
  try {
    await api.put(`/api/edit-ports/${id}/`, form, {
      headers: {
        "X-CSRFToken": getCookie("csrftoken")
      },
      withCredentials: true
    })
    alert("修改成功")
    router.push("/port")
  } catch (e) {
    alert("修改失败")
  }
}

/* ===== 删除 ===== */
const remove = async () => {
  if (!confirm("确定删除？")) return

  try {
    await api.delete(`/api/delete-port/${id}/`, {
      headers: {
        "X-CSRFToken": getCookie("csrftoken")
      },
      withCredentials: true
    })
    alert("删除成功")
    router.push("/port")
  } catch (e) {
    alert("删除失败")
  }
}

/* ===== 返回 ===== */
const back = () => {
  router.push("/port")
}

onMounted(async () => {
  await loadData()
  const userRes = await api.get('/api/user_info/')
  user.value = fixAvatar(userRes.data)
  Object.assign(user, userRes.data)
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
/**/

/* main */
.main-content {
  flex: 1;
  padding: 20px;
  background: #edf2f7;
}

/* card */
.card {
  background: white;
  border-radius: 10px;
  padding: 20px;
}

/* form */
.form-row {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

input, select {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
}

/* buttons */
.btn-group {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  color: white;
  cursor: pointer;
}

.btn-success { background: #38a169; }
.btn-danger { background: #e53e3e; }
.btn-warning { background: #d69e2e; }
</style>