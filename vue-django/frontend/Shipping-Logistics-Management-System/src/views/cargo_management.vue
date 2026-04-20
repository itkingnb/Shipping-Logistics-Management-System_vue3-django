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
        <li><router-link to="/port"><i class="fas fa-anchor"></i><span class="link-text">港口管理</span></router-link></li>
        <li><router-link to="/cargo" class="active"><i class="fas fa-box"></i><span class="link-text">货物管理</span></router-link></li>
        <li><router-link to="/order"><i class="fas fa-file-invoice"></i><span class="link-text">订单管理</span></router-link></li>
        <li><router-link to="/operator_update_profile"><i class="fas fa-cog"></i><span class="link-text">系统设置</span></router-link></li>
      </ul>
    </div>

    <!-- main -->
    <div class="main-content">
      <!-- header -->
      <div class="header">
        <h1>货物管理</h1>
        <div class="user-info">
          <img :src="user.avatar || defaultAvatar" />
          <div>
            <div>{{ user.name }}</div>
            <div class="role">{{ user.role }}</div>
          </div>
        </div>
      </div>

      <!-- 搜索 -->
      <div class="search-container">
        <input v-model="keyword" class="search-input" placeholder="搜索货物..." />
        <button class="search-btn" @click="loadData(1)">搜索</button>
        <button class="btn-menu" @click="go('/create-cargo')">创建货物</button>
      </div>

      <!-- 表格 -->
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>名称</th>
            <th>类型</th>
            <th>重量</th>
            <th>体积</th>
            <th>单价</th>
            <th>库存</th>
            <th>操作</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="c in list" :key="c.cargo_id">
            <td>{{ c.cargo_id }}</td>
            <td>{{ c.cargo_name }}</td>
            <td>{{ c.cargo_type }}</td>
            <td>{{ c.cargo_weight || '-' }}</td>
            <td>{{ c.cargo_volume || '-' }}</td>
            <td>{{ c.cargo_amount || '-' }}</td>
            <td>{{ c.inventory }}</td>
            <td>
              <button class="btn-edit" @click="edit(c.cargo_id)">编辑</button>
              <button class="btn-delete" @click="remove(c.cargo_id)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- 分页 -->
      <div class="pagination">
        <button v-if="hasPrevious" @click="loadData(page-1)">上一页</button>

        <button
          v-for="n in totalPages"
          :key="n"
          :class="{ active: n === page }"
          @click="loadData(n)"
        >
          {{ n }}
        </button>

        <button v-if="hasNext" @click="loadData(page+1)">下一页</button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue"
import axios from "axios"
import { useRouter } from "vue-router"

const router = useRouter()

const list = ref([])
const keyword = ref("")
const page = ref(1)
const totalPages = ref(1)
const hasNext = ref(false)
const hasPrevious = ref(false)

const user = reactive({ name: '', role: '', avatar: '' })
const defaultAvatar = "https://via.placeholder.com/40"
const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  withCredentials: true,
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
const loadData = async (p = 1) => {
  const res = await api.get("/api/cargos/", {
    params: {
      page: p,
      keyword: keyword.value
    }
  })

  list.value = res.data.list
  page.value = res.data.page
  totalPages.value = res.data.total_pages
  hasNext.value = res.data.has_next
  hasPrevious.value = res.data.has_previous
}

/* ===== 删除 ===== */
const remove = async (id) => {
  if (!confirm("确定删除？")) return

  try {
    await api.delete(`/api/delete-cargo/${id}/`, {
      headers: {
        "X-CSRFToken": getCookie("csrftoken")
      },
      withCredentials: true
    })
    alert("删除成功")
    loadData(page.value)
  } catch (e) {
    alert("删除失败")
  }
}

/* ===== 编辑 ===== */
const edit = (id) => {
  router.push(`/cargo/edit/${id}`)
}

const go = (path) => {
  router.push(path)
}

onMounted(async () => {
  await loadData(1)
  const res = await api.get("/api/user_info/")
  user.value = fixAvatar(res.data)
  Object.assign(user, res.data)
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

.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-info img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.role { font-size: 12px; color: #999 }

/* 搜索 */
.search-container {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.search-input {
  flex: 1;
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #ddd;
}

.search-btn {
  background: #74b9ff;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 6px;
}

.btn-menu {
  background: #0984e3;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 6px;
}

/* table */
table {
  width: 100%;
  background: white;
  border-collapse: collapse;
}

th, td {
  padding: 10px;
  border-bottom: 1px solid #eee;
}

/* buttons */
.btn-edit {
  background: #007bff;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  margin-right: 5px;
}

.btn-delete {
  background: #e53e3e;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
}

/* pagination */
.pagination {
  margin-top: 15px;
  text-align: center;
}

.pagination button {
  margin: 3px;
  padding: 6px 10px;
}

.pagination .active {
  background: #007bff;
  color: white;
}
</style>