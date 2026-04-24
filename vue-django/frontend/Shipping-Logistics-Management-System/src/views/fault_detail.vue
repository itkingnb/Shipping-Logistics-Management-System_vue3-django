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
      <div class="header">
        <h2>故障详情</h2>

        <div class="user">
          <img :src="user.avatar || defaultAvatar" />
          <div>
            <div>{{ user.name }}</div>
            <small>{{ user.role }}</small>
          </div>
        </div>
      </div>

      <!-- 内容卡片 -->
      <div class="card">

        <!-- 标题 -->
        <div class="title">
          <i class="fas fa-exclamation-triangle"></i>
          故障报告 #{{ detail.report_id }}
        </div>

        <!-- 信息块 -->
        <div class="info-grid">

          <div class="info-box">
            <span>任务编号</span>
            <strong>{{ detail.task_id || '-' }}</strong>
          </div>

          <div class="info-box">
            <span>上报人</span>
            <strong>{{ detail.reported_by || '-' }}</strong>
          </div>

          <div class="info-box">
            <span>上报时间</span>
            <strong>{{ detail.reported_at }}</strong>
          </div>

          <div class="info-box status-box">
            <span>状态</span>
            <b :class="statusClass(detail.status)">
              {{ detail.status }}
            </b>
          </div>

        </div>

        <!-- 描述 -->
        <div class="desc-card">
          <div class="desc-title">
            <i class="fas fa-info-circle"></i> 故障描述
          </div>
          <p>{{ detail.description }}</p>
        </div>

        <!-- 返回 -->
        <div class="actions">
          <button @click="router.push('/fault_center')">
            ← 返回
          </button>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api, fixAvatar } from '../utils/common'

const route = useRoute()
const router = useRouter()

const user = reactive({})
const detail = reactive({})
const defaultAvatar = '/avatar.png'

// 用户
const loadUser = async () => {
  const res = await api.get('/api/user_info/')
  Object.assign(user, fixAvatar(res.data))
}

// 详情
const loadDetail = async () => {
  const id = route.params.id
  const res = await api.get(`/api/fault_detail/${id}/`)
  Object.assign(detail, res.data.data)
}

// 状态样式
const statusClass = (s) => {
  if (s === '已处理') return 'badge done'
  if (s === '处理中') return 'badge running'
  return 'badge pending'
}

onMounted(() => {
  loadUser()
  loadDetail()
})
</script>

<style scoped>

/* ===== 布局 ===== */
.main {
  margin-left: 240px;
  padding: 25px;
  background: #f4f7fb;
  min-height: 100vh;
}

/* ===== header ===== */
.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.user {
  display: flex;
  align-items: center;
  background: white;
  padding: 6px 12px;
  border-radius: 20px;
}

.user img {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  margin-right: 10px;
}

/* ===== 卡片 ===== */
.card {
  background: white;
  padding: 25px;
  border-radius: 14px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.05);
}

/* 标题 */
.title {
  font-size: 20px;
  font-weight: bold;
  color: #2c5282;
  margin-bottom: 20px;
}

/* 信息网格 */
.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 25px;
}

.info-box {
  background: #f9fafc;
  padding: 18px;
  border-radius: 10px;
  transition: 0.2s;
}

.info-box:hover {
  background: #edf2f7;
}

.info-box span {
  font-size: 13px;
  color: #888;
}

.info-box strong {
  display: block;
  font-size: 18px;
  margin-top: 5px;
}

/* 状态 */
.status-box {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.badge {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 14px;
}

.pending { background: #fff3cd; }
.running { background: #bee3f8; }
.done { background: #c6f6d5; }

/* 描述 */
.desc-card {
  background: #ffffff;
  border: 1px solid #eee;
  padding: 20px;
  border-radius: 12px;
}

.desc-title {
  font-weight: bold;
  margin-bottom: 10px;
  color: #444;
}

/* 按钮 */
.actions {
  margin-top: 20px;
}

button {
  background: #3182ce;
  color: white;
  border: none;
  padding: 8px 18px;
  border-radius: 8px;
  cursor: pointer;
}

button:hover {
  background: #2c5282;
}
</style>