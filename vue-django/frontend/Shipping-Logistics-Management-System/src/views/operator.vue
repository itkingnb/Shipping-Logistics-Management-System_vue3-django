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
        <li><router-link to="/operator"class="active"><i class="fas fa-user-tag"></i><span class="link-text">报表统计</span></router-link></li>
        <li><router-link to="/customer"><i class="fas fa-user-tag"></i><span class="link-text">客户管理</span></router-link></li>
        <li><router-link to="/port"><i class="fas fa-anchor"></i><span class="link-text">港口管理</span></router-link></li>
        <li><router-link to="/cargo"><i class="fas fa-box"></i><span class="link-text">货物管理</span></router-link></li>
        <li><router-link to="/order"><i class="fas fa-file-invoice"></i><span class="link-text">订单管理</span></router-link></li>
        <li><router-link to="/operator_update_profile"><i class="fas fa-cog"></i><span class="link-text">系统设置</span></router-link></li>
      </ul>
    </div>

    <!-- 主内容 -->
    <div class="main-content">
      <!-- 顶部栏 -->
      <div class="header">
        <h1>报表数据统计</h1>
        <div class="user-info">
          <img :src="user.avatar || defaultAvatar" />
          <div>
            <div>{{ user.name }}</div>
            <div class="role">{{ user.role || '操作员' }}</div>
          </div>
        </div>
      </div>

      <!-- KPI -->
      <div class="kpi-container">
        <div class="kpi-card"><div class="kpi-title">用户总数</div><div class="kpi-value">{{ kpi.users }}</div></div>
        <div class="kpi-card"><div class="kpi-title">订单总数</div><div class="kpi-value">{{ kpi.orders }}</div></div>
        <div class="kpi-card"><div class="kpi-title">货物种类</div><div class="kpi-value">{{ kpi.cargo }}</div></div>
        <div class="kpi-card"><div class="kpi-title">任务总数</div><div class="kpi-value">{{ kpi.tasks }}</div></div>
      </div>

      <!-- 图表 -->
      <div class="card">
        <div class="card-header"><h2>订单状态分布</h2></div>
        <div class="card-body"><div ref="pieRef" class="chart"></div></div>
      </div>

      <div class="card">
        <div class="card-header"><h2>月度订单趋势</h2></div>
        <div class="card-body"><div ref="lineRef" class="chart"></div></div>
      </div>

      <div class="card">
        <div class="card-header"><h2>货物 TOP5</h2></div>
        <div class="card-body"><div ref="barRef" class="chart"></div></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import axios from 'axios'
import * as echarts from 'echarts'
const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  withCredentials: true,
})
const pieRef = ref(null)
const lineRef = ref(null)
const barRef = ref(null)

const defaultAvatar = 'https://via.placeholder.com/40'

const user = reactive({ name: '', role: '', avatar: '' })
const kpi = reactive({ users: 0, orders: 0, cargo: 0, tasks: 0 })

let pieChart = null
let lineChart = null
let barChart = null

function initCharts(data) {
  const tryInit = () => {
    const pieEl = pieRef.value
    const lineEl = lineRef.value
    const barEl = barRef.value

    // ⚠️ 关键：必须等 DOM 有尺寸
    if (!pieEl || pieEl.clientWidth === 0) {
      requestAnimationFrame(tryInit)
      return
    }

    // ===== PIE =====
    pieChart?.dispose()
    pieChart = echarts.init(pieEl)
    pieChart.setOption({
      tooltip: { trigger: 'item' },
      series: [{
        type: 'pie',
        radius: ['40%', '70%'],
        data: data.order_status.map(i => ({
          value: i.count,
          name: i.order_status
        }))
      }]
    })

    // ===== LINE =====
    lineChart?.dispose()
    lineChart = echarts.init(lineEl)
    lineChart.setOption({
      xAxis: {
        type: 'category',
        data: data.monthly_orders.map(i => i.month)
      },
      yAxis: { type: 'value' },
      series: [{
        type: 'line',
        smooth: true,
        data: data.monthly_orders.map(i => i.count)
      }]
    })

    // ===== BAR =====
    barChart?.dispose()
    barChart = echarts.init(barEl)
    barChart.setOption({
      xAxis: {
        type: 'category',
        data: data.cargo_top.map(i => i.cargo_name)
      },
      yAxis: { type: 'value' },
      series: [{
        type: 'bar',
        data: data.cargo_top.map(i => i.total)
      }]
    })

    // resize
    window.addEventListener('resize', () => {
      pieChart?.resize()
      lineChart?.resize()
      barChart?.resize()
    })
  }

  requestAnimationFrame(tryInit)
}
const fixAvatar = (u) => { 
  u.avatar = 'http://127.0.0.1:8000/' + u.avatar
  return u
}
onMounted(async () => {
  const res = await api.get('/operator/report')
  const data = res.data

  Object.assign(kpi, data.kpi)

  await nextTick()
  initCharts(data)

  const userRes = await api.get('/api/user_info/')
  user.value = fixAvatar(userRes.data)
  Object.assign(user, userRes.data)
  
  console.log(user)
})
</script>

<style scoped>


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
/* *{margin:0;padding:0;box-sizing:border-box;font-family:'Segoe UI','Microsoft YaHei',sans-serif} */
:root{--primary:#1a3a5f;--accent:#3182ce;--light:#f7fafc;--dark:#2d3748;--success:#38a169;--danger:#e53e3e;--gray:#a0aec0}
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
* { margin:0; padding:0; box-sizing:border-box }

.layout { display:flex }

.sidebar {
  width:250px;
  background:#1a3a5f;
  color:white;
  height:100vh;
}

.main-content {
  flex:1;
  padding:20px;
  margin-left:250px;
}

.header {
  display:flex;
  justify-content:space-between;
  margin-bottom:20px;
}

.user-info {
  display:flex;
  align-items:center;
}

.user-info img {
  width:40px;
  height:40px;
  border-radius:50%;
  margin-right:10px;
}

.role { font-size:12px; color:#aaa }

.kpi-container {
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(200px,1fr));
  gap:10px;
}

.kpi-card {
  background:white;
  padding:15px;
  border-left:4px solid #3182ce;
}

.card {
  background:white;
  margin-top:20px;
  border-radius:8px;
}

.card-header {
  padding:10px;
  border-bottom:1px solid #eee;
}

.card-body { padding:10px }

.chart {
  height:350px;
  width:100%;
}
</style>