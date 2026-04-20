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
        <li><router-link to="/operator"><i class="fas fa-user-tag"></i><span class="link-text">报表统计</span></router-link></li>
        <li><router-link to="/customer"><i class="fas fa-user-tag"></i><span class="link-text">客户管理</span></router-link></li>
        <li><router-link to="/port"><i class="fas fa-anchor"></i><span class="link-text">港口管理</span></router-link></li>
        <li><router-link to="/cargo"><i class="fas fa-box"></i><span class="link-text">货物管理</span></router-link></li>
        <li><router-link to="/order" class="active"><i class="fas fa-file-invoice"></i><span class="link-text">订单管理</span></router-link></li>
        <li><router-link to="/operator_update_profile"><i class="fas fa-cog"></i><span class="link-text">系统设置</span></router-link></li>
      </ul>
    </div>

    <!-- ===== 主体 ===== -->
    <div class="main">

      <!-- header -->
      <div class="header">
        <h2>编辑订单</h2>

        <div class="user">
          <img :src="user.avatar" />
          <div>
            <div>{{ user.name }}</div>
            <small>{{ user.role }}</small>
          </div>
        </div>
      </div>

      <!-- 表单 -->
      <div class="card">

        <!-- 基本信息 -->
        <div class="form-row">
          <div class="form-group">
            <label>客户</label>
            <select v-model="form.customer">
              <option value="">请选择</option>
              <option v-for="c in customers" :key="c.customer_id" :value="c.customer_id">
                {{ c.customer_name }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label>出发港口</label>
            <select v-model="form.origin_port">
              <option value="">请选择</option>
              <option v-for="p in ports" :key="p.port_id" :value="p.port_id">
                {{ p.port_name }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label>目标港口</label>
            <select v-model="form.destination_port">
              <option value="">请选择</option>
              <option v-for="p in ports" :key="p.port_id" :value="p.port_id">
                {{ p.port_name }}
              </option>
            </select>
          </div>
        </div>

        <!-- 货物选择 -->
        <div class="form-row">
          <div class="form-group full">
            <label>选择货物</label>
            <select v-model="selectedCargo">
              <option :value="null">请选择货物</option>
              <option v-for="c in cargos" :key="c.cargo_id" :value="c">
                {{ c.cargo_name }}
              </option>
            </select>
          </div>
        </div>

        <button class="btn primary" @click="addCargo">
          + 添加货物
        </button>

        <!-- 货物表 -->
        <table class="table">
          <thead>
            <tr>
              <th>货物名称</th>
              <th>数量</th>
              <th>操作</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="(c, i) in cargoList" :key="i">
              <td>{{ c.cargo_name }}</td>
              <td>{{ c.quantity }}</td>
              <td>
                <button class="btn delete" @click="removeCargo(i)">删除</button>
              </td>
            </tr>

            <tr v-if="cargoList.length === 0">
              <td colspan="3" class="empty">暂无货物</td>
            </tr>
          </tbody>
        </table>

        <!-- 操作 -->
        <div class="actions">
          <button class="btn gray" @click="submit(true)">保存草稿</button>
          <button class="btn success" @click="submit(false)">提交</button>
          <button class="btn warning" @click="go('/order')">取消</button>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from "vue"
import axios from "axios"
import { useRoute, useRouter } from "vue-router"
import { api,fixAvatar } from "../utils/common.js"
const route = useRoute()
const router = useRouter()

const orderId = route.params.id

const user = reactive({ name: "", role: "", avatar: "" })

const customers = ref([])
const ports = ref([])
const cargos = ref([])

const selectedCargo = ref(null)
const cargoList = ref([])

const form = ref({
  customer: "",
  origin_port: "",
  destination_port: ""
})



/* ===== 用户 ===== */
const loadUser = async () => {
  const userRes = await api.get('/api/user_info/')
  user.value = fixAvatar(userRes.data)
  Object.assign(user, userRes.data)
  console.log(user)
}

/* ===== 初始化 ===== */
const loadInit = async () => {
  const [o, c, p, g] = await Promise.all([
    api.get(`/api/order/${orderId}/`),
    api.get("/api/customers/"),
    api.get("/api/ports/"),
    api.get("/api/cargos/")
  ])

  const order = o.data

  // ===== 列表 =====
  customers.value = c.data.data.customers
  ports.value = p.data.list
  cargos.value = g.data.list

  // ===== 👇 关键：补“当前值” =====

  // 客户
  if (order.customer && !customers.value.find(x => x.customer_id === order.customer)) {
    customers.value.push({
      customer_id: order.customer,
      customer_name: order.customer_name || `客户#${order.customer}`
    })
  }

  // 出发港口
  if (order.origin_port && !ports.value.find(x => x.port_id === order.origin_port)) {
    ports.value.push({
      port_id: order.origin_port,
      port_name: order.origin_port_name || `港口#${order.origin_port}`
    })
  }

  // 目标港口
  if (order.destination_port && !ports.value.find(x => x.port_id === order.destination_port)) {
    ports.value.push({
      port_id: order.destination_port,
      port_name: order.destination_port_name || `港口#${order.destination_port}`
    })
  }

  // ===== 等DOM更新 =====
  await nextTick()

  // ===== 回填 =====
  form.value.customer = order.customer
  form.value.origin_port = order.origin_port
  form.value.destination_port = order.destination_port

  cargoList.value = order.cargo_list || []
}

/* ===== 添加货物 ===== */
const addCargo = () => {
  if (!selectedCargo.value) return alert("请选择货物")

  const exist = cargoList.value.find(
    x => x.cargo_id === selectedCargo.value.cargo_id
  )
  if (exist) return alert("已添加")

  const qty = prompt("请输入数量", "1")
  if (!qty || isNaN(qty)) return

  cargoList.value.push({
    cargo_id: selectedCargo.value.cargo_id,
    cargo_name: selectedCargo.value.cargo_name,
    quantity: Number(qty)
  })
}

/* ===== 删除 ===== */
const removeCargo = (i) => {
  cargoList.value.splice(i, 1)
}

/* ===== 提交 ===== */
const submit = async (isDraft) => {
  try {
    await api.post(`/api/order/update/${orderId}/`, {
      ...form.value,
      cargo_list: cargoList.value,
      is_draft: isDraft
    })

    alert("修改成功")
    router.push("/order")

  } catch (e) {
    alert(e.response?.data?.error || "失败")
  }
}

/* ===== 重置 ===== */
// const reset = () => {
//   cargoList.value = []
// }

/* ===== 跳转 ===== */
const go = (p) => router.push(p)

onMounted(() => {
  loadUser()
  loadInit()
})
</script>

<style scoped>
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

.main {
  margin-left: 220px;
  flex: 1;
  padding: 20px;
  background: #f5f7fa;
}

.header {
  display: flex;
  justify-content: space-between;
}

.user {
  display: flex;
  align-items: center;
}

.user img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

/* 表单 */
.form-row {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
}

.form-group { flex: 1; }
.full { flex: 100%; }

select {
  width: 100%;
  padding: 8px;
}

/* 表格 */
.table {
  width: 100%;
  background: white;
  margin-top: 20px;
}

th, td {
  padding: 10px;
  border-bottom: 1px solid #eee;
}

/* 按钮 */
.btn {
  padding: 8px 14px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
}

.primary { background: #3182ce; color: white; }
.success { background: #38a169; color: white; }
.warning { background: #d69e2e; color: white; }
.gray { background: #718096; color: white; }
.delete { background: #e53e3e; color: white; }

.actions {
  margin-top: 20px;
  text-align: center;
}

.empty {
  text-align: center;
}
</style>