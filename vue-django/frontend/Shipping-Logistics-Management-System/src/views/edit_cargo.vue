<template>
  <div class="app">

    <!-- sidebar -->
    <div class="sidebar">
      <div class="logo-container">
        <div class="logo">
          <i class="fas fa-ship"></i>
          <span>航运物流公司管理系统</span>
        </div>
      </div>

      <ul class="nav-links">
        <li><router-link to="/operator">报表统计</router-link></li>
        <li><router-link to="/customer">客户管理</router-link></li>
        <li><router-link to="/port">港口管理</router-link></li>
        <li><router-link to="/cargo" class="active">货物管理</router-link></li>
        <li><router-link to="/order">订单管理</router-link></li>
        <li><router-link to="/settings">系统设置</router-link></li>
      </ul>
    </div>

    <!-- main -->
    <div class="main-content">

      <!-- header -->
      <div class="header">
        <h1>编辑货物</h1>

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
        <div class="card-header">
          <h2><i class="fas fa-edit"></i> 货物信息编辑</h2>
        </div>

        <div class="card-body">

          <div class="form-row">
            <input v-model="form.cargo_id" disabled />
            <input v-model="form.cargo_name" placeholder="货物名称" />
          </div>

          <div class="form-row">
            <input v-model="form.cargo_type" placeholder="货物类型" />
            <input v-model="form.cargo_weight" placeholder="重量" />
          </div>

          <div class="form-row">
            <input v-model="form.cargo_volume" placeholder="体积" />
            <input v-model="form.inventory" placeholder="库存" />
          </div>

          <div class="form-row">
            <input v-model="form.cargo_amount" placeholder="单价" />
          </div>

          <!-- 按钮 -->
          <div class="button-group">
            <button class="btn btn-submit" @click="submit">提交</button>
            <button class="btn btn-reset" @click="reset">重置</button>
            <button class="btn btn-back" @click="back">返回</button>
            <button class="btn btn-danger" @click="remove">删除</button>
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

const route = useRoute()
const router = useRouter()
const id = route.params.id

const defaultAvatar = "https://via.placeholder.com/40"

const user = reactive({
  name: "",
  role: "",
  avatar: ""
})

const form = reactive({
  cargo_id: "",
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

/* ===== 加载数据 ===== */
const loadData = async () => {
  const res = await axios.get(`/api/edit-cargo/${id}/`)
  Object.assign(form, res.data)
}

/* ===== 用户信息 ===== */
const loadUser = async () => {
  const res = await axios.get("/api/user_info/")
  Object.assign(user, res.data)
}

/* ===== 提交 ===== */
const submit = async () => {
  try {

    const payload = {
      ...form,
      cargo_weight: Number(form.cargo_weight),
      cargo_volume: Number(form.cargo_volume),
      inventory: Number(form.inventory),
      cargo_amount: Number(form.cargo_amount)
    }

    await axios.put(`/api/edit-cargo/${id}/`, payload, {
      headers: {
        "Content-Type": "application/json"
      }
    })

    alert("修改成功")
    router.push("/cargo")

  } catch (e) {
    console.log("后端返回：", e.response?.data)
    alert(e.response?.data?.error || "修改失败")
  }
}

/* ===== 删除 ===== */
const remove = async () => {
  if (!confirm("确定删除？")) return

  try {
    await axios.delete(`/api/delete-cargo/${id}/`, {
      headers: {
        "X-CSRFToken": getCookie("csrftoken")
      },
      withCredentials: true
    })

    alert("删除成功")
    router.push("/cargo")

  } catch (e) {
    alert("删除失败")
  }
}

/* ===== 重置 ===== */
const reset = () => {
  loadData()
}

/* ===== 返回 ===== */
const back = () => {
  router.push("/cargo")
}

onMounted(() => {
  loadData()
  loadUser()
})
</script>

<style scoped>
.app { display:flex; }

/* sidebar */
.sidebar {
  width:250px;
  background:#1a3a5f;
  color:white;
  height:100vh;
  padding:20px;
}

.logo { font-weight:bold; margin-bottom:20px; }

.nav-links a {
  display:block;
  color:white;
  padding:10px;
  text-decoration:none;
}

.nav-links a.active,
.nav-links a:hover {
  background:rgba(255,255,255,0.1);
}

/* main */
.main-content {
  flex:1;
  padding:20px;
  background:#edf2f7;
}

/* header */
.header {
  display:flex;
  justify-content:space-between;
  margin-bottom:20px;
}

.user-info {
  display:flex;
  align-items:center;
}

.user-info img {
  width:40px;
  height:40px;
  border-radius:50%;
  margin-right:10px;
}

.role { font-size:12px; color:#999 }

/* card */
.card {
  background:white;
  border-radius:10px;
  padding:20px;
}

/* form */
.form-row {
  display:flex;
  gap:10px;
  margin-bottom:10px;
}

input {
  flex:1;
  padding:10px;
  border:1px solid #ddd;
  border-radius:6px;
}

/* buttons */
.button-group {
  margin-top:20px;
  display:flex;
  gap:10px;
}

.btn {
  padding:8px 16px;
  border:none;
  border-radius:6px;
  color:white;
  cursor:pointer;
}

.btn-submit { background:#38a169; }
.btn-reset { background:#dd6b20; }
.btn-back { background:#718096; }
.btn-danger { background:#e53e3e; }
</style>