<template>
  <div class="app">

    <!-- ===== 侧边栏（完全不动） ===== -->
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

    <!-- ===== 主体（美化重点） ===== -->
    <div class="main-content">

      <!-- Header -->
      <div class="header card">
        <h1>📊 系统管理控制台</h1>

        <div class="user-info">
          <img :src="user.avatar || '/avatar.png'" />
          <div>
            <div class="name">{{ user.name }}</div>
            <div class="role-text">{{ user.role }}</div>
          </div>
        </div>
      </div>

      <!-- KPI -->
      <div class="kpi-container">
        <div class="kpi-card blue">
          <div>历史订单</div>
          <h2>{{ kpi.total_orders }}</h2>
        </div>

        <div class="kpi-card green">
          <div>货物总价值</div>
          <h2>¥{{ kpi.total_value }}</h2>
        </div>

        <div class="kpi-card orange">
          <div>在途任务</div>
          <h2>{{ kpi.in_transit }}</h2>
        </div>

        <div class="kpi-card purple">
          <div>完成率</div>
          <h2>{{ kpi.rate }}%</h2>
        </div>
      </div>

      <!-- 图表 -->
      <div class="card chart-card">
        <div class="chart-row">
          <div>
            <h3>📈 订单趋势</h3>
            <div ref="trendRef" class="chart"></div>
          </div>

          <div>
            <h3>📊 状态分布</h3>
            <div ref="pieRef" class="chart"></div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import * as echarts from 'echarts'
import { ref, onMounted, nextTick } from 'vue'
import { api, fixAvatar } from "../utils/common.js"

const user = ref({})
const kpi = ref({
  total_orders: 0,
  total_value: 0,
  in_transit: 0,
  rate: 0
})

const trendRef = ref(null)
const pieRef = ref(null)

/* ===== 用户 ===== */
const loadUser = async () => {
  const res = await api.get('/api/user_info/')
  Object.assign(user.value, fixAvatar(res.data))
}

/* ===== 图表美化 ===== */
const initCharts = (data) => {

  // 折线图（高级版）
  const trendChart = echarts.init(trendRef.value)
  trendChart.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: data.monthly_orders.map(i => i.month),
      axisLine: { lineStyle: { color: '#ccc' } }
    },
    yAxis: { type: 'value' },
    series: [{
      data: data.monthly_orders.map(i => i.count),
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 8,
      lineStyle: { width: 3 },
      areaStyle: {
        opacity: 0.2
      }
    }]
  })

  // 饼图（环形 + 动效）
  const pieChart = echarts.init(pieRef.value)
  pieChart.setOption({
    tooltip: { trigger: 'item' },
    legend: { bottom: 0 },
    series: [{
      type: 'pie',
      radius: ['50%', '75%'],
      itemStyle: {
        borderRadius: 8,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: { show: true, formatter: '{b}: {d}%' },
      data: data.order_status_count.map(i => ({
        name: i.order_status,
        value: i.count
      }))
    }]
  })
}

/* ===== 数据 ===== */
const loadData = async () => {
  const res = await api.get('/api/dashboard/')
  const d = res.data.data

  kpi.value.total_orders = d.total_orders
  kpi.value.total_value = d.cargo_total_amount

  const done = d.order_status_count.find(i => i.order_status === '已完成')
  const total = d.total_orders || 1
  kpi.value.rate = done ? Math.round(done.count / total * 100) : 0

  const transit = d.order_status_count.find(i => i.order_status === '运输中')
  kpi.value.in_transit = transit ? transit.count : 0

  await nextTick()
  initCharts(d)
}

onMounted(() => {
  loadUser()
  loadData()
})
</script>

<style scoped>
/* ===== 主体背景 ===== */
.main-content {
  margin-left: 250px;
  padding: 25px;
  background: #f4f7fb;
}

/* ===== Header 卡片 ===== */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding: 15px 20px;
}

/* 用户 */
.user-info {
  display: flex;
  align-items: center;
}
.user-info img {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  margin-right: 10px;
}
.name { font-weight: 600 }
.role-text { font-size: 12px; color: #888 }

/* ===== KPI ===== */
.kpi-container {
  display: grid;
  grid-template-columns: repeat(4,1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.kpi-card {
  padding: 20px;
  border-radius: 14px;
  color: white;
  transition: all 0.25s;
}

.kpi-card h2 {
  margin-top: 10px;
  font-size: 26px;
}

.kpi-card:hover {
  transform: translateY(-5px);
}

/* 渐变色 */
.blue { background: linear-gradient(135deg,#3b82f6,#1e40af) }
.green { background: linear-gradient(135deg,#10b981,#047857) }
.orange { background: linear-gradient(135deg,#f59e0b,#b45309) }
.purple { background: linear-gradient(135deg,#8b5cf6,#5b21b6) }

/* ===== 卡片 ===== */
.card {
  background: white;
  border-radius: 14px;
  box-shadow: 0 8px 25px rgba(0,0,0,0.05);
}

/* ===== 图表 ===== */
.chart-card {
  padding: 20px;
}

.chart-row {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
}

.chart {
  height: 320px;
}
</style>