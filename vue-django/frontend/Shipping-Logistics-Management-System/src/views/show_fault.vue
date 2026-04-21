<template>
  <div class="layout">

    <!-- ===== 侧边栏（原封不动）===== -->
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
        <li><router-link to="/appointer_update_profile"><i class="fas fa-user-cog"></i><span>个人设置</span></router-link></li>
      </ul>
    </div>

    <!-- ===== 主内容 ===== -->
    <div class="main-content">

      <!-- 顶部 -->
      <div class="header">
        <h1>故障详情</h1>

        <div class="user-info">
          <img :src="user.avatar" />
          <div>
            <div>{{ user.name }}</div>
            <div style="font-size:12px;color:#a0aec0">
              {{ user.role || '系统管理员' }}
            </div>
          </div>
        </div>
      </div>

      <!-- 内容 -->
      <div class="container my-5" v-if="data">

        <!-- 标题 -->
        <h3 class="mb-5 text-primary">
          <i class="fas fa-exclamation-triangle me-2"></i>
          故障报告 #{{ data.report_id }}
        </h3>

        <!-- 基本信息 -->
        <div class="row g-4 mb-5">
          <div class="col-md-6">
            <div class="info-card">
              <h6>任务编号</h6>
              <p>{{ data.task_id || '-' }}</p>
            </div>
          </div>

          <div class="col-md-6">
            <div class="info-card">
              <h6>上报人</h6>
              <p>{{ data.reported_by || '-' }}</p>
            </div>
          </div>

          <div class="col-md-6">
            <div class="info-card">
              <h6>上报时间</h6>
              <p>{{ data.reported_at }}</p>
            </div>
          </div>

          <div class="col-md-6">
            <div class="info-card status-box">
              <h6>状态</h6>
              <span :class="statusClass(data.status)">
                {{ data.status }}
              </span>
            </div>
          </div>
        </div>

        <!-- 描述 -->
        <div class="desc-box">
          <h6><i class="fas fa-info-circle"></i> 故障描述</h6>
          <p>{{ data.description }}</p>
        </div>

        <!-- 返回 -->
        <div class="back">
          <button @click="go('/fault')">
            <i class="fas fa-arrow-left"></i> 返回
          </button>
        </div>

      </div>

      <div v-else class="loading">
        加载中...
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref,reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api,fixAvatar } from '../utils/common.js'

const route = useRoute()
const router = useRouter()

const data = ref(null)
const user = reactive({
  name: '',
  role: '',
  avatar: ''
})

// ===== 获取详情 =====
const load = async () => {
  const id = route.params.id
  const res = await api.get(`/api/fault/${id}/`)
  data.value = res.data
}
const loadUser = async () => {
  const res = await api.get('/api/user_info/')
  Object.assign(user, fixAvatar(res.data))
}
// ===== 状态样式 =====
const statusClass = (s) => {
  if (s === '已处理') return 'badge success'
  if (s === '处理中') return 'badge warning'
  return 'badge info'
}

const go = (p) => router.push(p)

onMounted(() => {
  load()
  loadUser()
})
</script>

<style scoped>
/* ===== sidebar 原样 ===== */
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  width: 240px;
  height: 100vh;
  background: #1a3a5f;
  color: #fff;
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
}

.nav-links a {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 48px;
  color: rgba(255,255,255,0.8);
}

.nav-links a.active {
  background: rgba(255,255,255,0.15);
  border-left: 4px solid #3182ce;
}

/* ===== 主体 ===== */
.main-content {
  margin-left: 240px;
  padding: 30px;
  background: #f4f7fb;
  min-height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30px;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-info img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

/* ===== 标题优化 ===== */
h3 {
  font-weight: 600;
  color: #1a3a5f;
  border-left: 5px solid #3182ce;
  padding-left: 12px;
}

/* ===== 信息卡片升级 ===== */
.info-card {
  padding: 20px;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 6px 16px rgba(0,0,0,0.06);
  transition: all 0.2s;
}

.info-card:hover {
  transform: translateY(-2px);
}

.info-card h6 {
  color: #718096;
  font-size: 13px;
  margin-bottom: 6px;
}

.info-card p {
  font-size: 20px;
  font-weight: 600;
  color: #2d3748;
  margin: 0;
}

/* 状态盒子右对齐 */
.status-box {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* ===== 状态 badge ===== */
.badge {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
  color: #fff;
}

.success { background: #38a169; }
.warning { background: #d69e2e; }
.info { background: #3182ce; }

/* ===== 描述区域升级 ===== */
.desc-box {
  padding: 25px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 6px 16px rgba(0,0,0,0.06);
  line-height: 1.7;
}

.desc-box h6 {
  margin-bottom: 10px;
  color: #4a5568;
}

.desc-box p {
  font-size: 15px;
  color: #2d3748;
}

/* ===== 返回按钮 ===== */
.back {
  margin-top: 30px;
}

.back button {
  padding: 10px 18px;
  background: #3182ce;
  color: #fff;
  border: none;
  border-radius: 8px;
  transition: all 0.2s;
  cursor: pointer;
}

.back button:hover {
  background: #2c5282;
  transform: translateY(-1px);
}

/* ===== 加载状态 ===== */
.loading {
  text-align: center;
  margin-top: 80px;
  color: #999;
  font-size: 16px;
}
</style>