<template>
  <div class="layout">

    <!-- ===== 侧边栏（不动） ===== -->
    <div class="sidebar">
      <div class="logo-container">
        <div class="logo">
          <i class="fas fa-ship"></i>
          <span class="logo-text">航运物流公司管理系统</span>
        </div>
      </div>

      <ul class="nav-links">
        <li><router-link to="/transporter"><i class="fas fa-home"></i><span>运输报表</span></router-link></li>
        <li><router-link to="/task_center"><i class="fas fa-clipboard-check"></i><span>任务中心</span></router-link></li>
        <li><router-link to="/report_location"><i class="fas fa-tasks"></i><span>位置上报</span></router-link></li>
        <li><router-link to="/fault_center" class="active"><i class="fas fa-exclamation-triangle"></i><span>故障上报</span></router-link></li>
        <li><router-link to="/transporter_update_profile"><i class="fas fa-cog"></i><span>系统设置</span></router-link></li>
      </ul>
    </div>

    <!-- ===== 主体 ===== -->
    <div class="main">

      <!-- Header -->
      <div class="header card-shadow">
        <h2>故障上报</h2>

        <div class="user">
          <img :src="user.avatar || defaultAvatar" />
          <div>
            <div class="name">{{ user.name }}</div>
            <small>{{ user.role }}</small>
          </div>
        </div>
      </div>

      <!-- 标题 -->
      <div class="top-bar">
        <h3>📋 已上报的故障</h3>
        <button class="primary" @click="router.push('/report_fault')">
          + 新增故障
        </button>
      </div>

      <!-- 表格 -->
      <div class="card table-card">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>时间</th>
              <th>描述</th>
              <th>状态</th>
              <th>操作</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="r in reports" :key="r.report_id">
              <td>#{{ r.report_id }}</td>
              <td>{{ r.reported_at }}</td>

              <td class="desc" :title="r.description">
                {{ r.description }}
              </td>

              <td>
                <span :class="statusClass(r.status)">
                  {{ r.status }}
                </span>
              </td>

              <td>
                <button class="btn-view" @click="view(r.report_id)">
                  查看
                </button>
                  <button
                  v-if="r.status !== '已处理'"
                  class="btn-cancel"
                  @click="cancel(r.report_id)"
                >
                  撤销
                </button>
              </td>
            </tr>

            <tr v-if="reports.length === 0">
              <td colspan="5" class="empty">
                📭 暂无故障记录
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <button class="back" @click="router.push('/transporter')">
        ← 返回
      </button>

    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api, fixAvatar } from '../utils/common'

const router = useRouter()

const reports = ref([])
const user = reactive({})
const defaultAvatar = '/avatar.png'

// 用户
const loadUser = async () => {
  const res = await api.get('/api/user_info/')
  Object.assign(user, fixAvatar(res.data))
}

// 数据
const loadReports = async () => {
  const res = await api.get('/api/fault_reports/')
  reports.value = res.data.data || []
}

// 状态颜色
const statusClass = (s) => {
  if (s === '已处理') return 'badge done'
  if (s === '处理中') return 'badge running'
  return 'badge pending'
}
const cancel = async (id) => {
if (!confirm("确定撤销该故障上报？")) return

const res = await api.post(`/api/fault_cancel/${id}/`)

if (res.data.success) {
  alert("撤销成功")
  loadReports() // 刷新
} else {
  alert(res.data.message || "操作失败")
}
}
const view = (id) => {
  router.push(`/fault_detail/${id}`)
}

onMounted(() => {
  loadUser()
  loadReports()
})
</script>

<style scoped>

/* ===== 主体 ===== */
.main {
  margin-left: 240px;
  padding: 25px;
  background: #f4f7fb;
}

/* ===== 卡片阴影统一 ===== */
.card-shadow {
  background: white;
  padding: 15px 20px;
  border-radius: 12px;
  box-shadow: 0 6px 18px rgba(0,0,0,0.06);
}

/* ===== Header ===== */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.header h2 {
  font-weight: 600;
  color: #1a3a5f;
}

.user {
  display: flex;
  align-items: center;
  background: #f8fafc;
  padding: 6px 12px;
  border-radius: 20px;
}

.user img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.name {
  font-weight: 500;
}

/* ===== 顶部 ===== */
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.top-bar h3 {
  color: #2d3748;
}

/* ===== 表格卡片 ===== */
.table-card {
  padding: 15px;
  border-radius: 12px;
  background: white;
  box-shadow: 0 8px 25px rgba(0,0,0,0.05);
}

/* ===== 表格 ===== */
table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: #f1f5f9;
}

th {
  padding: 12px;
  font-size: 14px;
  color: #475569;
}

td {
  padding: 12px;
  font-size: 14px;
}

tbody tr {
  transition: all 0.2s;
}

tbody tr:hover {
  background: #f8fafc;
  transform: scale(1.01);
}

/* 描述截断 */
.desc {
  max-width: 240px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* ===== 状态 ===== */
.badge {
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.pending {
  background: #fff3cd;
  color: #856404;
}

.running {
  background: #dbeafe;
  color: #1d4ed8;
}

.done {
  background: #dcfce7;
  color: #166534;
}

/* ===== 按钮 ===== */
button {
  cursor: pointer;
  border: none;
  border-radius: 8px;
  padding: 6px 14px;
  transition: all 0.2s;
}

/* 主按钮 */
.primary {
  background: #3182ce;
  color: white;
}

.primary:hover {
  background: #2b6cb0;
  transform: translateY(-1px);
}

/* 查看按钮 */
.btn-view {
  background: #edf2f7;
}

.btn-view:hover {
  background: #e2e8f0;
}
.btn-cancel {
  background: #fee2e2;
  color: #b91c1c;
  margin-left: 6px;
}

.btn-cancel:hover {
  background: #fecaca;
}
/* 返回按钮 */
.back {
  margin-top: 20px;
  background: #e2e8f0;
}

.back:hover {
  background: #cbd5e0;
}

/* ===== 空状态 ===== */
.empty {
  text-align: center;
  padding: 30px;
  color: #94a3b8;
}

</style>