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
        <li><router-link to="/transporter"><i class="fas fa-home"></i><span>运输报表</span></router-link></li>
        <li><router-link to="/task_center" class="active"><i class="fas fa-clipboard-check"></i><span>任务中心</span></router-link></li>
        <li><router-link to="/report_location"><i class="fas fa-tasks"></i><span>位置上报</span></router-link></li>
        <li><router-link to="/fault_center"><i class="fas fa-exclamation-triangle"></i><span>故障上报</span></router-link></li>
        <li><router-link to="/transporter_update_profile"><i class="fas fa-cog"></i><span class="link-text">系统设置</span></router-link></li>
      </ul>
    </div>

    <!-- ===== 主体 ===== -->
    <div class="main-content">

      <!-- header -->
      <div class="header">
        <h1>任务详情</h1>
        <div class="user-info">
          <img :src="user.avatar || defaultAvatar" />
          <div>
            <div>{{ user.name }}</div>
            <div class="role">{{ user.role }}</div>
          </div>
        </div>
      </div>

      <!-- ===== 任务信息 ===== -->
      <div class="card">
        <h3>任务 {{ task.task_id }}</h3>

        <table class="info-table">
          <tr><th>指派人</th><td>{{ task.assigned_by }}</td></tr>
          <tr><th>执行人</th><td>{{ task.assigned_to }}</td></tr>

          <tr>
            <th>状态</th>
            <td>
              <span :class="statusClass(task.status)">
                {{ task.status }}
              </span>
            </td>
          </tr>

          <tr><th>始发港</th><td>{{ task.origin_port }}</td></tr>
          <tr><th>目的港</th><td>{{ task.destination_port }}</td></tr>
          <tr><th>指派时间</th><td>{{ task.assigned_time }}</td></tr>
          <tr><th>开始时间</th><td>{{ task.start_time }}</td></tr>
        </table>
      </div>

      <!-- ===== 订单 ===== -->
      <div class="card">
        <h3>订单列表</h3>

        <table class="table">
          <thead>
            <tr>
              <th>订单ID</th>
              <th>客户</th>
              <th>起点</th>
              <th>终点</th>
              <th>状态</th>
              <th>金额</th>
              <th>操作</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="o in orders" :key="o.order_id">
              <td>{{ o.order_id }}</td>
              <td>{{ o.customer }}</td>
              <td>{{ o.origin_port }}</td>
              <td>{{ o.destination_port }}</td>

              <td>
                <span :class="orderStatusClass(o.status)">
                  {{ o.status }}
                </span>
              </td>

              <td>{{ o.total_amount }}</td>

              <td>
                <button class="btn primary" @click="viewOrder(o.order_id)">
                  查看
                </button>
              </td>
            </tr>

            <tr v-if="orders.length === 0">
              <td colspan="7" class="empty">暂无订单</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- ===== 轨迹 ===== -->
      <div class="card">
        <h3>轨迹记录</h3>

        <table class="table">
          <thead>
            <tr>
              <th>#</th>
              <th>时间</th>
              <th>纬度</th>
              <th>经度</th>
              <th>操作</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="(t, i) in tracks" :key="t.track_id">
              <td>{{ i + 1 }}</td>
              <td>{{ t.recorded_at }}</td>
              <td>{{ t.latitude }}</td>
              <td>{{ t.longitude }}</td>

              <td>
                <button class="btn danger" @click="removeTrack(t.track_id)">
                  撤销
                </button>
              </td>
            </tr>

            <tr v-if="tracks.length === 0">
              <td colspan="5" class="empty">暂无轨迹</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- ===== 操作按钮 ===== -->
      <div class="actions">
        <button class="btn" @click="router.push('/task_center')">
          返回
        </button>

        <button
          v-if="task.status === '运输中'"
          @click="confirm"
          class="btn primary"
        >
          确认送达
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api, fixAvatar } from "../utils/common.js"

const route = useRoute()
const router = useRouter()

const task = reactive({})
const orders = ref([])
const tracks = ref([])
const user = reactive({ name: '', role: '', avatar: '' })

const defaultAvatar = '/avatar.png'

// ===== 用户 =====
const loadUser = async () => {
  const res = await api.get('/api/user_info/')
  Object.assign(user, fixAvatar(res.data))
}

// ===== 数据 =====
const loadData = async () => {
  const id = route.params.id
  const res = await api.get(`/api/transporter_show_task/${id}/`)

  Object.assign(task, res.data.task)
  orders.value = res.data.orders || []
  tracks.value = res.data.tracks || []
}

// ===== 状态 =====
const statusClass = (s) => {
  if (s === '运输中') return 'badge running'
  if (s === '已完成') return 'badge done'
  if (s === '待处理') return 'badge pending'
  return 'badge'
}

const orderStatusClass = (s) => {
  if (s === '已完成') return 'badge done'
  if (s === '待配送') return 'badge pending'
  return 'badge'
}

// ===== 操作 =====
const viewOrder = (id) => {
  router.push(`/transporter_show_order/${id}`)
}

const removeTrack = async (id) => {
  await api.post(`/api/delete_track/${id}/`)
  loadData()
}

const confirm = async () => {
  await api.post(`/api/confirm_delivery/${task.task_id}/`)
  loadData()
}

onMounted(() => {
  loadUser()
  loadData()
})
</script>

<style scoped>
.layout {
  display: flex;
  background: #f4f7fb;
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

/* ===== main ===== */
.main-content {
  margin-left: 240px;
  padding: 20px;
  width: 100%;
}

/* ===== header ===== */
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
  width: 36px;
  border-radius: 50%;
  margin-right: 10px;
}

/* ===== card ===== */
.card {
  background: #fff;
  padding: 18px;
  margin-bottom: 20px;
  border-radius: 12px;
  box-shadow: 0 6px 18px rgba(0,0,0,0.06);
}

.card h3 {
  margin-bottom: 10px;
  border-left: 4px solid #3182ce;
  padding-left: 8px;
}

/* ===== table ===== */
.table {
  width: 100%;
  border-spacing: 0 6px;
}

.table td, .table th {
  padding: 10px;
  text-align: center;
}

.table tbody tr {
  background: #f9fafc;
}

.table tbody tr:hover {
  background: #edf2f7;
}

/* ===== info table ===== */
.info-table th {
  width: 120px;
  text-align: left;
}

/* ===== badge ===== */
.badge {
  padding: 4px 10px;
  border-radius: 20px;
}

.running {
  background: #e6f0ff;
  color: #2b6cb0;
}

.done {
  background: #e6fffa;
  color: #2f855a;
}

.pending {
  background: #fff7cc;
  color: #b7791f;
}

/* ===== btn ===== */
.btn {
  padding: 6px 12px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
}

.primary {
  background: #3182ce;
  color: white;
}

.danger {
  background: #e53e3e;
  color: white;
}

/* ===== actions ===== */
.actions {
  display: flex;
  gap: 10px;
}

.empty {
  color: gray;
}
</style>