<template>
    <div class="app">
    <!-- 侧边栏 -->
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
        <h1>客户管理</h1>

        <div class="user-info">
          <img :src="user.avatar || defaultAvatar" />
          <div>
            <div>{{ user.name }}</div>
            <div style="font-size:12px;color:#999">{{ user.role }}</div>
          </div>
        </div>
      </div>

      <!-- 搜索 -->
      <div class="search-container">
        <input v-model="keyword" class="search-input" placeholder="搜索港口..." />
        <button class="search-btn" @click="loadData(1)">搜索</button>
        <button class="btn-menu" @click="go('/create-port')">创建港口</button>
      </div>

      <!-- 表格 -->
      <table class="port-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>代码</th>
            <th>中文名</th>
            <th>英文名</th>
            <th>国家</th>
            <th>城市</th>
            <th>操作</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="p in list" :key="p.port_id">
            <td>{{ p.port_id }}</td>
            <td>{{ p.port_code }}</td>
            <td>{{ p.port_name }}</td>
            <td>{{ p.port_name_en }}</td>
            <td>{{ p.country }}</td>
            <td>{{ p.city }}</td>
            <td>
              <button class="btn-edit" @click="edit(p.port_id)">编辑</button>
              <button class="btn-delete" @click="remove(p.port_id)">删除</button>
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
import { ref, reactive, onMounted } from 'vue'
import axios from "axios"
import { useRouter } from "vue-router"
import { api,fixAvatar } from "../utils/common.js"
const router = useRouter()
const list = ref([])
const keyword = ref("")
const page = ref(1)
const totalPages = ref(1)
const hasNext = ref(false)
const hasPrevious = ref(false)
const user = reactive({ name: '', role: '', avatar: '' })
const loadData = async (p = 1) => {
  const res = await api.get("/api/ports/", {
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
const edit = (id) => {
  router.push(`/port/edit/${id}`)
}
const remove = async (id) => {
  if (!confirm("确定删除该港口吗？")) return

  try {
    await api.delete(`/api/delete-port/${id}/`)
    alert("删除成功")
    if (list.value.length === 1 && page.value > 1) {
        loadData(page.value - 1)
    } else {
        loadData(page.value)
    }
  } catch (err) {
    console.error(err)
    alert("删除失败")
  }
}

const go = (path) => {
  router.push(path)
}

onMounted(async () => {
  await loadData(1)
  const userRes = await api.get('/api/user_info/')
  user.value = fixAvatar(userRes.data)
  Object.assign(user, userRes.data)
})
</script>

<style>
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
  justify-content: center;   /*  文字整体居中 */

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

.main-content {
  flex:1;
  padding:20px;
  margin-left:250px;
}

/* ===== header ===== */
.header {
  display:flex;
  justify-content:space-between;
  margin-bottom:20px;
}
.header h1 {
  color: #1a3a5f;
}

/* ===== search ===== */
.search-container {
  display: flex;
  gap: 10px;
  background: #f8f9fa;
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 20px;
}

.search-input {
  flex: 1;
  padding: 10px;
  /* border-radius: 8px; */
  border: 1px solid #ddd;
}

.search-btn {
  background: #74b9ff;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 8px;
}

/* ===== buttons ===== */
.btn-menu {
  background: linear-gradient(135deg, #74b9ff, #0984e3);
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 8px;
}

.btn-edit {
  background: #007bff;
  color: white;
  border: none;
  padding: 6px 10px;
  border-radius: 5px;
}
.btn-delete {
  background: #e53e3e;
  color: white;
  border: none;
  padding: 6px 10px;
  border-radius: 5px;
  margin-left: 6px;
  cursor: pointer;
  transition: 0.2s;
}

.btn-delete:hover {
  background: #c53030;
}

/* ===== table ===== */
.port-table {
  width: 100%;
  background: white;
  border-collapse: collapse;
  border-radius: 10px;
  overflow: hidden;
}

.port-table th,
.port-table td {
  padding: 12px;
  border-bottom: 1px solid #eee;
}

.port-table tr:hover {
  background: #f8fbff;
}

/* ===== pagination ===== */
.pagination {
  margin-top: 15px;
  text-align: center;
}

.pagination button {
  margin: 4px;
  padding: 6px 12px;
  border: 1px solid #ddd;
  background: white;
  color: #333;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

/* hover效果 */
.pagination button:hover {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

/* 当前页 */
.pagination .active {
  background: #007bff;
  color: white;
  border-color: #007bff;
  cursor: default;
}
</style>