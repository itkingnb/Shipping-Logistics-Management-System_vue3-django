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
    <div class="main">

      <!-- Header -->
      <div class="header">
        <h2>订单详情</h2>

        <div class="user">
          <img :src="user.avatar || defaultAvatar">
          <div>
            <div>{{ user.name }}</div>
            <small>{{ user.role }}</small>
          </div>
        </div>
      </div>

      <!-- ===== 卡片 ===== -->
      <div class="card">

        <!-- 基本信息 -->
        <div class="section">
          <h3>基本信息</h3>

          <div class="grid">
            <div><b>订单编号：</b>{{ order.order_id }}</div>
            <div><b>客户：</b>{{ order.customer }}</div>
            <div><b>起点：</b>{{ order.origin_port }}</div>
            <div><b>终点：</b>{{ order.destination_port }}</div>
            <div><b>创建时间：</b>{{ order.created_at }}</div>
          </div>
        </div>

        <!-- 任务 -->
        <div class="section" v-if="order.task_id">
          <h3>所属任务</h3>

          <div class="grid">
            <div><b>任务ID：</b>{{ order.task_id }}</div>
            <div>
              <b>状态：</b>
              <span :class="statusClass(order.task_status)">
                {{ order.task_status }}
              </span>
            </div>
          </div>
        </div>

        <!-- 货物 -->
        <div class="section">
          <h3>货物清单</h3>

          <table class="table">
            <thead>
              <tr>
                <th>名称</th>
                <th>类型</th>
                <th>重量</th>
                <th>体积</th>
                <th>数量</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="(c, i) in cargos" :key="i">
                <td>{{ c.name }}</td>
                <td>{{ c.type }}</td>
                <td>{{ c.weight || '-' }}</td>
                <td>{{ c.volume || '-' }}</td>
                <td>{{ c.quantity }}</td>
              </tr>

              <tr v-if="cargos.length === 0">
                <td colspan="5">暂无货物</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 按钮 -->
        <div class="actions">
          <button @click="goBack">返回任务</button>
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

const order = reactive({})
const cargos = ref([])
const user = reactive({})

const defaultAvatar = '/avatar.png'

// ===== 加载数据 =====
const loadData = async () => {
  const id = route.params.id
  const res = await api.get(`/api/transporter_show_order/${id}/`)

  Object.assign(order, res.data.order)
  cargos.value = res.data.cargos || []
}

// ===== 用户 =====
const loadUser = async () => {
  const res = await api.get('/api/user_info/')
  Object.assign(user, fixAvatar(res.data))
}

// ===== 状态颜色 =====
const statusClass = (s) => {
  if (s === '已完成') return 'badge done'
  if (s === '运输中') return 'badge running'
  return 'badge pending'
}

// ===== 返回 =====
const goBack = () => {
  if (order.task_id) {
    router.push(`/task_detail/${order.task_id}`)
  } else {
    router.push('/task_center')
  }
}

onMounted(() => {
  loadData()
  loadUser()
})
</script>

<style scoped>
.layout {
  display: flex;
}

/* ===== 侧边栏 ===== */
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

/* ===== 主体 ===== */
.main {
  flex: 1;
  padding: 20px;
  background: #f4f7fb;
}

/* header */
.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.user {
  display: flex;
  align-items: center;
}

.user img {
  width: 36px;
  border-radius: 50%;
  margin-right: 10px;
}

/* 卡片 */
.card {
  background: white;
  padding: 20px;
  border-radius: 12px;
}

/* 分区 */
.section {
  margin-bottom: 25px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

/* 表格 */
.table {
  width: 100%;
}

.table th, .table td {
  padding: 10px;
  text-align: center;
}

/* 状态 */
.badge {
  padding: 4px 10px;
  border-radius: 20px;
}

.done { background: #c6f6d5; }
.running { background: #bee3f8; }
.pending { background: #faf089; }

/* 按钮 */
.actions {
  text-align: right;
}

button {
  padding: 8px 16px;
  background: #3182ce;
  color: white;
  border: none;
  border-radius: 6px;
}
</style>