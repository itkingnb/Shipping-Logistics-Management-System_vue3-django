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
        <li>
          <a href="javascript:void(0)" @click="go('/admin')">
            <i class="fas fa-tachometer-alt"></i>
            <span>数据统计</span>
          </a>
        </li>

        <li>
          <a href="javascript:void(0)" class="active">
            <i class="fas fa-user-tag"></i>
            <span>用户管理</span>
          </a>
        </li>

        <li>
          <a href="javascript:void(0)" @click="go('/administrator_update_profile')">
            <i class="fas fa-cog"></i>
            <span>系统设置</span>
          </a>
        </li>
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

const router = useRouter()

axios.defaults.baseURL = 'http://127.0.0.1:8000'
axios.defaults.withCredentials = true
const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  withCredentials: true,
})
const users = ref([])
const keyword = ref('')

const pagination = ref({
  current_page: 1,
  total_pages: 1,
  has_next: false,
  has_previous: false
})

const user = ref({
  name: '管理员',
  role: '系统管理员',
  avatar: '/avatar.png'
})

const go = (path) => {
  router.push(path)
}

const loadUser = () => {
  const u = localStorage.getItem('user')
  if (u) {
    const parsed = JSON.parse(u)
    if (parsed.avatar) {
      parsed.avatar = 'http://127.0.0.1:8000/' + parsed.avatar
    }
    user.value = parsed
  }
  // console.log(user)
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
*{margin:0;padding:0;box-sizing:border-box;font-family:'Segoe UI','Microsoft YaHei',sans-serif}
:root{--primary:#1a3a5f;--accent:#3182ce;--light:#f7fafc;--dark:#2d3748;--success:#38a169;--danger:#e53e3e;--gray:#a0aec0}
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
.logo-container{padding:20px;border-bottom:1px solid rgba(255,255,255,.1)}
.logo{display:flex;align-items:center;font-weight:700;white-space: nowrap;  }
.logo i{margin-right:10px;color:var(--accent)}

.nav-links a{display:flex;align-items:center;padding:12px 20px;color:rgba(255,255,255,.8);text-decoration:none}
.nav-links a:hover,.nav-links a.active{background:rgba(255,255,255,.1);color:#fff;border-left:4px solid var(--accent)}
.nav-links i{margin-right:10px}

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
  gap: 10px;           /* ⭐给一点间距 */
}

.card-header h2 {
  font-size: 18px;
  white-space: nowrap;
  flex-shrink: 0;      /* ⭐不允许被压缩 */
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