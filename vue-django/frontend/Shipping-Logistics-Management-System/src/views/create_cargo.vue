<template>
  <div class="app">
    <!-- ===== sidebar ===== -->
    <div class="sidebar">
      <div class="logo">航运物流公司管理系统</div>

      <ul class="nav-links">
        <li><router-link to="/operator">报表统计</router-link></li>
        <li><router-link to="/customer">客户管理</router-link></li>
        <li><router-link to="/port">港口管理</router-link></li>
        <li><router-link to="/cargo" class="active">货物管理</router-link></li>
        <li><router-link to="/order">订单管理</router-link></li>
        <li><router-link to="/settings">系统设置</router-link></li>
      </ul>
    </div>

    <!-- ===== main ===== -->
    <div class="main-content">

      <!-- header -->
      <div class="header">
        <h1>创建货物</h1>
        <div class="user-info">
          <img :src="user.avatar || defaultAvatar" />
          <div>
            <div>{{ user.name }}</div>
            <div class="role">{{ user.role }}</div>
          </div>
        </div>
      </div>

      <!-- card -->
      <div class="card">
        <h2 class="card-title">
          <i class="fas fa-box"></i> 货物基本信息
        </h2>

        <!-- 表单 -->
        <div class="form-row">
          <div class="form-group">
            <label>货物名称</label>
            <input v-model="form.cargo_name" />
          </div>
          <div class="form-group">
            <label>货物类型</label>
            <input v-model="form.cargo_type" />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>重量 (吨)</label>
            <input v-model="form.cargo_weight" />
          </div>
          <div class="form-group">
            <label>体积 (m³)</label>
            <input v-model="form.cargo_volume" />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>库存量</label>
            <input v-model="form.inventory" />
          </div>
          <div class="form-group">
            <label>单价</label>
            <input v-model="form.cargo_amount" />
          </div>
        </div>

        <!-- 按钮 -->
        <div class="btn-group">
          <button class="btn btn-success" @click="submit">提交</button>
          <button class="btn btn-warning" @click="reset">重置</button>
          <button class="btn btn-back" @click="back">返回</button>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from "vue"
import axios from "axios"
import { useRouter } from "vue-router"

const router = useRouter()

/* ===== 用户 ===== */
const user = reactive({
  name: "",
  role: "",
  avatar: ""
})

const defaultAvatar = "https://via.placeholder.com/40"

/* ===== 表单 ===== */
const form = reactive({
  cargo_name: "",
  cargo_type: "",
  cargo_weight: "",
  cargo_volume: "",
  inventory: "",
  cargo_amount: ""
})

/* ===== CSRF ===== */
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

/* ===== 提交 ===== */
const submit = async () => {
  try {
    await axios.post("/api/create_cargo/", form, {
      headers: {
        "X-CSRFToken": getCookie("csrftoken")
      },
      withCredentials: true
    })

    alert("创建成功")
    router.push("/cargo")

  } catch (e) {
    console.error(e)
    alert("创建失败")
  }
}

/* ===== 重置 ===== */
const reset = () => {
  Object.keys(form).forEach(k => form[k] = "")
}

/* ===== 返回 ===== */
const back = () => {
  router.push("/cargo")
}

/* ===== 用户信息 ===== */
onMounted(async () => {
  try {
    const res = await axios.get("/api/user_info/", {
      withCredentials: true
    })
    Object.assign(user, res.data)
  } catch (e) {
    console.log("用户信息获取失败")
  }
})
</script>

<style scoped>
.app {
  display: flex;
}

/* ===== sidebar ===== */
.sidebar {
  width: 240px;
  background: #1a3a5f;
  color: white;
  padding: 20px;
  height: 100vh;
}

.logo {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 25px;
}

.nav-links {
  list-style: none;
  padding: 0;
}

.nav-links a {
  display: block;
  padding: 12px;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  transition: 0.2s;
}

.nav-links a:hover,
.nav-links a.active {
  background: rgba(255,255,255,0.12);
}

/* ===== main ===== */
.main-content {
  flex: 1;
  padding: 25px;
  background: #edf2f7;
}

/* ===== header ===== */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.header h1 {
  color: #1a3a5f;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-info img {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  margin-right: 10px;
  border: 2px solid #3182ce;
}

.role {
  font-size: 12px;
  color: #888;
}

/* ===== card ===== */
.card {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 6px 16px rgba(0,0,0,0.06);
}

.card-title {
  margin-bottom: 20px;
  color: #1a3a5f;
}

/* ===== form ===== */
.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 18px;
  margin-bottom: 18px;
}

.form-group label {
  font-size: 13px;
  color: #555;
  margin-bottom: 5px;
  display: block;
}

input {
  padding: 12px 14px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.25s;
}

input:focus {
  outline: none;
  border-color: #3182ce;
  box-shadow: 0 0 0 3px rgba(49,130,206,0.15);
}

/* ===== buttons ===== */
.btn-group {
  margin-top: 25px;
  display: flex;
  gap: 12px;
  justify-content: center;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  color: white;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.25s;
}

.btn-success {
  background: linear-gradient(135deg, #38a169, #2f855a);
}

.btn-success:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 10px rgba(56,161,105,0.3);
}

.btn-warning {
  background: linear-gradient(135deg, #d69e2e, #b7791f);
}

.btn-warning:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 10px rgba(214,158,46,0.3);
}

.btn-back {
  background: linear-gradient(135deg, #718096, #4a5568);
}

.btn-back:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 10px rgba(113,128,150,0.3);
}
</style>