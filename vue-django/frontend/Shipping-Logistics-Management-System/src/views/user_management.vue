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
        <li><router-link to="/admin"><i class="fas fa-tachometer-alt"></i><span class="link-text">数据统计</span></router-link></li>
        <li><router-link to="/user_management" class="active"><i class="fas fa-user-tag"></i><span class="link-text">用户管理</span></router-link></li>
        <li><router-link to="/administrator_update_profile"><i class="fas fa-cog"></i><span class="link-text">系统设置</span></router-link></li>
      </ul>
    </div>

    <!-- 主内容 -->
    <div class="main-content">
      <div class="header">
        <h1>系统管理控制台</h1>
        <div class="user-info">
          <img :src="user.avatar" />
          <div>
            <div>{{ user.name }}</div>
            <div class="role-text">{{ user.role }}</div>
          </div>
        </div>
      </div>

      <!-- 用户管理 -->
      <div class="card">
        <div class="card-header">
          <h2><i class="fas fa-users"></i> 用户管理</h2>
          <input
            v-model="keyword"
            @keyup.enter="search"
            placeholder="搜索用户名或角色"
            class="form-control"
          />
        </div>

        <div class="card-body">
          <table class="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>用户名</th>
                <th>角色</th>
                <th>手机号</th>
                <th>邮箱</th>
                <th>状态</th>
                <th>操作</th>
              </tr>
            </thead>

            <tbody>
              <tr v-if="users.length === 0">
                <td colspan="7">暂无数据</td>
              </tr>

              <tr v-else v-for="u in users" :key="u.id">
                <td>{{ u.id }}</td>
                <td>{{ u.username }}</td>
                <td>{{ u.role }}</td>
                <td>{{ u.phone }}</td>
                <td>{{ u.email }}</td>

                <td>
                  <span :class="statusClass(u.status)">
                    {{ u.status }}
                  </span>
                </td>

                <td>
                  <button
                    class="btn btn-primary btn-sm"
                    v-if="u.status === '已禁用'"
                    @click="toggle(u, '启用')"
                  >
                    启用
                  </button>

                  <button
                    class="btn btn-danger btn-sm"
                    v-else
                    @click="toggle(u, '禁用')"
                  >
                    禁用
                  </button>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- 分页 -->
          <div class="pagination" v-if="pagination.total_pages > 1">
            <button
              @click="fetchUsers(pagination.current_page - 1)"
              :disabled="!pagination.has_previous"
            >
              上一页
            </button>

            <span>
              {{ pagination.current_page }} / {{ pagination.total_pages }}
            </span>

            <button
              @click="fetchUsers(pagination.current_page + 1)"
              :disabled="!pagination.has_next"
            >
              下一页
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { api,fixAvatar } from "../utils/common.js"
const router = useRouter()
const users = ref([])
const keyword = ref('')

const pagination = ref({
  current_page: 1,
  total_pages: 1,
  has_next: false,
  has_previous: false
})

const user = ref({name: '',role: '',avatar: ''})

const go = (path) => {
  router.push(path)
}

const loadUser = async () => {
  const userRes = await api.get('/api/user_info/')
  user.value = fixAvatar(userRes.data)
  Object.assign(user, userRes.data)
  console.log(user)
}

const statusClass = (status) => {
  if (status === '已禁用') return 'badge badge-danger'
  if (status === '已启用') return 'badge badge-success'
  return 'badge'
}

const fetchUsers = async (page = 1) => {
  try {
    const res = await api.get('administrator/user_management/', {
      params: { keyword: keyword.value, page }
    })
    if (res.data.success) {
      users.value = res.data.data.users
      pagination.value = res.data.data.pagination
    }
  } catch (err) {
    alert('请求出错')
  }
}

const search = () => fetchUsers(1)

const toggle = async (u, action) => {
  if (!confirm(`确定要${action}用户 ${u.username} 吗？`)) return
  try {
    const res = await api.post(
      `/administrator/toggle_user_status/${u.id}/`,
      { action }
    )
    if (res.data.success) {
      alert(res.data.message)
      fetchUsers(pagination.value.current_page)
    }
  } catch {
    alert('请求出错')
  }
}

onMounted(() => {
  fetchUsers()
  loadUser()
})
</script>

<style>
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

.main-content{margin-left:250px;padding:20px}
.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;border-bottom:1px solid #ddd;padding-bottom:10px}
.header h1{color:var(--primary)}
.user-info{display:flex;align-items:center}
.user-info img{width:40px;height:40px;border-radius:50%;margin-right:10px;border:2px solid var(--accent)}
.role-text{font-size:12px;color:var(--gray)}

.card{background:#fff;border-radius:10px;box-shadow:0 4px 10px rgba(0,0,0,.05)}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;           /* 给一点间距 */
}

.card-header h2 {
  font-size: 18px;
  white-space: nowrap;
  flex-shrink: 0;   
}

.card-body{padding:15px}

.form-control{padding:8px;border:1px solid #ccc;border-radius:6px;width:200px}

.table{width:100%;border-collapse:collapse}
.table th,.table td{padding:10px;border-bottom:1px solid #eee;text-align:center}
.table th{background:var(--light)}

.badge{padding:4px 8px;border-radius:4px;font-size:12px}
.badge-success{background:#c6f6d5;color:#22543d}
.badge-danger{background:#fed7d7;color:#742a2a}

.btn{padding:5px 10px;border:none;border-radius:5px;cursor:pointer}
.btn-primary{background:var(--accent);color:#fff}
.btn-danger{background:var(--danger);color:#fff}

.pagination{margin-top:10px;text-align:center}
.pagination button{margin:0 5px;padding:5px 10px;border:none;border-radius:4px;background:var(--accent);color:#fff}
.pagination button:disabled{background:#ccc}
</style>