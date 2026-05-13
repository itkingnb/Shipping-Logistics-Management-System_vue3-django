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
        <li><router-link to="/task_management" class="active"><i class="fas fa-tasks"></i><span>任务管理</span></router-link></li>
        <li><router-link to="/fault"><i class="fas fa-exclamation-triangle"></i><span>通知中心</span></router-link></li>
        <li><router-link to="/appointer_update_profile"><i class="fas fa-cog"></i><span>系统设置</span></router-link></li>
      </ul>
    </div>

    <!-- main -->
    <div class="main">
      <div class="content">

        <div class="header">
          <h1>轨迹信息</h1>
          <div class="user">
            <img :src="user.avatar || '/avatar.png'">
            <div>{{ user.name }}</div>
            <small>{{ user.role }}</small>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            任务 {{ taskId }} 的轨迹记录
          </div>

          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>纬度</th>
                <th>经度</th>
                <th>时间</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="t in tracks" :key="t.index">
                <td>{{ t.index }}</td>
                <td>{{ t.latitude }}</td>
                <td>{{ t.longitude }}</td>
                <td>{{ t.recorded_at }}</td>
              </tr>

              <tr v-if="tracks.length === 0">
                <td colspan="4" class="empty">暂无轨迹记录</td>
              </tr>
            </tbody>
          </table>

          <div class="footer">
            <button class="btn" @click="go('/task_management')">
              ← 返回
            </button>
          </div>

        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref,reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api, fixAvatar } from '../utils/common.js'

const route = useRoute()
const router = useRouter()
const taskId = route.params.id
const tracks = ref([])
const user = reactive({ name: '', role: '', avatar: '' })

const load = async () => {
  const res = await api.get(`/api/track/${taskId}/`)
  if (res.data.success) {
    tracks.value = res.data.tracks
  }
}

const loadUser = async () => {
  const res = await api.get('/api/user_info/')
  Object.assign(user, fixAvatar(res.data))
}

const go = (p) => router.push(p)

onMounted(() => {
  load()
  loadUser()
})
</script>

<style scoped>
html, body {
  margin: 0;
  padding: 0;
}

/* sidebar */
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

.nav-links {
  list-style: none;
  padding: 10px 0;
  margin: 0;
}

.nav-links a {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 48px;
  color: rgba(255,255,255,0.8);
  text-decoration: none;
}

.nav-links a:hover {
  background: rgba(255,255,255,0.1);
}

.nav-links a.active {
  background: rgba(255,255,255,0.15);
  border-left: 4px solid #3182ce;
}


/* main */
.main {
  flex: 1;
  padding: 30px;
}

.content {
  max-width: 1000px;
  margin: auto;
}

.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

/* card */
.card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
}

.card-header {
  padding: 15px;
  font-weight: bold;
}

/* table */
table {
  width: 100%;
}

th, td {
  padding: 12px;
  text-align: center;
}

.empty {
  color: #999;
}

/* footer */
.footer {
  padding: 15px;
  text-align: right;
}

.btn {
  padding: 8px 16px;
  background: #3182ce;
  color: white;
  border: none;
  border-radius: 6px;
}
.user img {
  width: 32px;
  height: 32px;
  border-radius: 50%;
}
</style>