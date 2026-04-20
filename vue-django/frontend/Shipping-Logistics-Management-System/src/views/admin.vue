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
        <li><router-link to="/admin" class="active"><i class="fas fa-tachometer-alt"></i><span class="link-text">数据统计</span></router-link></li>
        <li><router-link to="/user_management"><i class="fas fa-user-tag"></i><span class="link-text">用户管理</span></router-link></li>
        <li><router-link to="/administrator_update_profile"><i class="fas fa-cog"></i><span class="link-text">系统设置</span></router-link></li>
      </ul>
    </div>
    

    <!-- 主内容 -->
    <div class="main-content">
      <div class="header">
        <h1>系统管理控制台</h1>
        <div class="user-info">
          <img :src="user.avatar || '/avatar.png'" />
          <div>
            <div>{{ user.name }}</div>
            <div class="role-text">{{ user.role }}</div>
          </div>
        </div>
      </div>

      <!-- KPI -->
      <div class="card">
        <div class="card-header">
          <h2><i class="fas fa-chart-line"></i> 数据统计</h2>
        </div>

        <div class="card-body">
          <div class="kpi-container">
            <div class="kpi-card">
              <div class="kpi-title">历史订单总数</div>
              <div class="kpi-value">{{ kpi.total_orders }}</div>
            </div>

            <div class="kpi-card">
              <div class="kpi-title">货物总价值</div>
              <div class="kpi-value">¥{{ kpi.total_value }}</div>
            </div>

            <div class="kpi-card">
              <div class="kpi-title">在途任务</div>
              <div class="kpi-value warn">{{ kpi.in_transit }}</div>
            </div>

            <div class="kpi-card">
              <div class="kpi-title">完成率</div>
              <div class="kpi-value">{{ kpi.rate }}%</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 图表 -->
      <div class="card" style="margin-top:20px;">
        <div class="card-header">
          <h2><i class="fas fa-chart-area"></i> 数据分析</h2>
        </div>

        <div class="card-body">
          <div class="chart-row">
            <div>
              <h3>订单趋势</h3>
              <div ref="trendRef" class="chart"></div>
            </div>

            <div>
              <h3>订单状态</h3>
              <div ref="pieRef" class="chart"></div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import * as echarts from 'echarts'
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { api,fixAvatar } from "../utils/common.js"
const router = useRouter()

// ===== 用户 =====
const user = ref({
  name: '',
  role: '',
  avatar: ''
})

// 页面加载时读取
const loadUser = async () => {
  const userRes = await api.get('/api/user_info/')
  user.value = fixAvatar(userRes.data)
  Object.assign(user, userRes.data)
  console.log(user)
}

// 本地默认头像（避免外链报错）
// const defaultAvatar = '/logo.png'
onMounted(() => {
  loadUser()
  loadData()
})

// ===== KPI =====
const kpi = ref({
  total_orders: 0,
  total_value: 0,
  in_transit: 0,
  rate: 0
})

// ===== 图表 DOM =====
const trendRef = ref(null)
const pieRef = ref(null)

// ===== 跳转 =====
const go = (path) => {
  router.push(path)
}

// ===== 初始化图表 =====
const initCharts = (data) => {
  if (!data) return

  // ===== 折线图（订单趋势）=====
  if (trendRef.value && data.monthly_orders) {
    const months = data.monthly_orders.map(i => i.month)
    const orders = data.monthly_orders.map(i => i.count)

    const trendChart = echarts.init(trendRef.value)
    trendChart.setOption({
      tooltip: {},
      xAxis: { type: 'category', data: months },
      yAxis: { type: 'value' },
      series: [{
        data: orders,
        type: 'line',
        smooth: true,
        areaStyle: {}
      }]
    })
  }

  // ===== 饼图（订单状态）=====
  if (pieRef.value && data.order_status_count) {
    const status = data.order_status_count.map(i => ({
      name: i.order_status,
      value: i.count
    }))

    const pieChart = echarts.init(pieRef.value)
    pieChart.setOption({
      tooltip: {},
      series: [{
        type: 'pie',
        radius: ['40%', '70%'],
        data: status
      }]
    })
  }
}

// ===== 获取数据 =====
const loadData = async () => {
  try {
    const res = await api.get('http://127.0.0.1:8000/api/dashboard/')

    if (res.data.success) {
      const data = res.data.data

      // ===== KPI 映射 =====
      kpi.value.total_orders = data.total_orders
      kpi.value.total_value = data.cargo_total_amount

      const transit = data.order_status_count.find(i => i.order_status === '运输中')
      kpi.value.in_transit = transit ? transit.count : 0

      const total = data.total_orders || 1
      const done = data.order_status_count.find(i => i.order_status === '已完成')
      kpi.value.rate = done ? Math.round((done.count / total) * 100) : 0

      // ===== 图表 =====
      await nextTick()
      initCharts(data)
    }

  } catch (e) {
    console.error('接口错误', e)
  }
}

onMounted(() => {
  loadData()
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

.main-content{margin-left:250px;padding:20px}

.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;border-bottom:1px solid #ddd;padding-bottom:10px}
.header h1{color:var(--primary)}

.user-info{display:flex;align-items:center}
.user-info img{width:40px;height:40px;border-radius:50%;margin-right:10px;border:2px solid var(--accent)}
.role-text{font-size:12px;color:var(--gray)}

.card{background:#fff;border-radius:10px;box-shadow:0 4px 10px rgba(0,0,0,.05)}
.card-header{padding:15px;border-bottom:1px solid #eee}
.card-header h2{color:var(--primary)}
.card-body{padding:15px}

/* KPI */
.kpi-container{display:grid;grid-template-columns:repeat(4,1fr);gap:15px}
.kpi-card{background:var(--light);padding:15px;border-radius:8px;text-align:center}
.kpi-title{color:var(--gray);font-size:14px}
.kpi-value{font-size:22px;font-weight:bold;color:var(--dark)}
.warn{color:orange}

/* 图表 */
.chart-row{display:grid;grid-template-columns:2fr 1fr;gap:20px}
.chart{height:300px}
</style>