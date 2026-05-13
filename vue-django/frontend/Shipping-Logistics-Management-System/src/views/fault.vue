<template>
  <div>

    <!-- ===== sidebar ===== -->
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
        <li><router-link to="/fault" class="active"><i class="fas fa-exclamation-triangle"></i><span>通知中心</span></router-link></li>
        <li><router-link to="/appointer_update_profile"><i class="fas fa-cog"></i><span>系统设置</span></router-link></li>
      </ul>
    </div>

    <!-- ===== main ===== -->
    <div class="main-content">

      <!-- header -->
      <div class="header">
        <h1>故障上报</h1>

        <div class="user-info">
          <img :src="user.avatar || '/avatar.png'" />
          <div>
            <div>{{ user.name }}</div>
            <small>{{ user.role }}</small>
          </div>
        </div>
      </div>

      <!-- 标题 -->
      <div class="title-bar">
        <h4>
          <i class="fas fa-exclamation-triangle"></i>
          指派的任务故障报告
        </h4>
      </div>

      <!-- 表格 -->
      <div v-if="faults.length > 0" class="table-wrap">
        <table class="table">
          <thead>
            <tr>
              <th>报告编号</th>
              <th>任务编号</th>
              <th>上报人</th>
              <th>上报时间</th>
              <th>故障描述</th>
              <th>状态</th>
              <th>操作</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="f in faults" :key="f.id">
              <td>{{ f.id }}</td>
              <td>{{ f.task_id }}</td>
              <td>{{ f.reported_by }}</td>
              <td>{{ f.reported_at }}</td>

              <td class="desc" :title="f.description">
                {{ f.description.slice(0,30) }}
              </td>

              <td>
                <span v-if="f.status==='已处理'" class="badge success">已处理</span>
                <span v-else-if="f.status==='处理中'" class="badge warning">处理中</span>
                <span v-else class="badge info">未处理</span>
              </td>

              <td>
                <button @click="view(f.id)" class="btn small">
                  查看
                </button>

                <button v-if="f.status==='未处理'"
                        @click="process(f.id)"
                        class="btn warn small">
                  处理
                </button>

                <button v-if="f.status==='处理中'"
                        @click="finish(f.id)"
                        class="btn success small">
                  完成
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 空状态 -->
      <div v-else class="empty">
        暂无故障上报记录
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { api, fixAvatar } from '../utils/common.js'

const router = useRouter()

const faults = ref([])
const user = reactive({name: '',role: '',avatar: ''})

// ===== 加载数据 =====
const load = async () => {
  const res = await api.get('/api/faults/')
  faults.value = res.data.faults
  console.log(res.data.faults)
}

// ===== 用户 =====
const loadUser = async () => {
  const res = await api.get('/api/user_info/')
  Object.assign(user, fixAvatar(res.data))
}

// ===== 操作 =====
const view = (id) => {
  router.push(`/fault/${id}`)
}

const process = async (id) => {
  await api.post(`/api/fault/${id}/process/`)
  load()
}

const finish = async (id) => {
  await api.post(`/api/fault/${id}/finish/`)
  load()
}

onMounted(() => {
  load()
  loadUser()
})
</script>

<style scoped>

/* ===== sidebar（完全照你给的） ===== */
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

/* ===== main ===== */
.main-content {
  margin-left: 240px;
  padding: 25px;
}

/* header */
.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

/* 标题 */
.title-bar {
  margin: 20px 0;
}

/* 表格 */
.table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
}

th, td {
  padding: 10px;
  text-align: center;
  border-bottom: 1px solid #eee;
}

.desc {
  max-width: 200px;
  overflow: hidden;
}

/* 按钮 */
.btn {
  padding: 4px 10px;
  border: none;
  background: #3182ce;
  color: #fff;
  margin: 2px;
  border-radius: 4px;
  cursor: pointer;
}

.btn.warn {
  background: orange;
}

.btn.success {
  background: green;
}

.small {
  font-size: 12px;
}

/* 状态 */
.badge {
  padding: 4px 8px;
  border-radius: 6px;
  color: #fff;
}

.badge.success { background: green; }
.badge.warning { background: orange; }
.badge.info { background: #3182ce; }

/* 空 */
.empty {
  text-align: center;
  margin-top: 50px;
  color: #999;
}
</style>