<template>
  <div class="layout">

    <div class="sidebar">
      <div class="logo-container">
        <div class="logo">
          <i class="fas fa-ship"></i>
          <span class="logo-text">航运物流公司管理系统</span>
        </div>
      </div>
      <ul class="nav-links">
        <li><router-link to="/operator"><i class="fas fa-user-tag"></i><span class="link-text">报表统计</span></router-link></li>
        <li><router-link to="/customer"><i class="fas fa-user-tag"></i><span class="link-text">客户管理</span></router-link></li>
        <li><router-link to="/port"><i class="fas fa-anchor"></i><span class="link-text">港口管理</span></router-link></li>
        <li><router-link to="/cargo"><i class="fas fa-box"></i><span class="link-text">货物管理</span></router-link></li>
        <li><router-link to="/order" class="active"><i class="fas fa-file-invoice"></i><span class="link-text">订单管理</span></router-link></li>
        <li><router-link to="/operator_update_profile"><i class="fas fa-cog"></i><span class="link-text">系统设置</span></router-link></li>
      </ul>
    </div>

    <div class="main">
      <div class="header">
        <h2>编辑订单</h2>
        <div class="user">
          <img :src="user.avatar" />
          <div>
            <div>{{ user.name }}</div>
            <small>{{ user.role }}</small>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="form-row">
          <div class="form-group">
            <label>客户</label>
            <select v-model="form.customer">
              <option value="">请选择</option>
              <option v-for="c in customers" :key="c.customer_id" :value="c.customer_id">
                {{ c.customer_name }}
              </option>
            </select>
          </div>

          <!-- 出发港口 - 搜索 -->
          <div class="form-group">
            <label>出发港口</label>
            <div class="search-wrap">
              <input
                v-model="originPortText"
                @focus="onFocusPort('origin')"
                @input="onSearchPort('origin')"
                @blur="onBlurPort('origin')"
                placeholder="输入港口名搜索"
                autocomplete="off"
              />
              <ul v-if="showOriginList" class="search-list">
                <li v-for="p in portResults" :key="p.port_id"
                    @mousedown.prevent="selectPort('origin', p)">
                  {{ p.port_name }}
                </li>
                <li v-if="portResults.length===0" class="empty">无匹配港口</li>
              </ul>
            </div>
          </div>

          <!-- 目标港口 - 搜索 -->
          <div class="form-group">
            <label>目标港口</label>
            <div class="search-wrap">
              <input
                v-model="destPortText"
                @focus="onFocusPort('dest')"
                @input="onSearchPort('dest')"
                @blur="onBlurPort('dest')"
                placeholder="输入港口名搜索"
                autocomplete="off"
              />
              <ul v-if="showDestList" class="search-list">
                <li v-for="p in portResults" :key="p.port_id"
                    @mousedown.prevent="selectPort('dest', p)">
                  {{ p.port_name }}
                </li>
                <li v-if="portResults.length===0" class="empty">无匹配港口</li>
              </ul>
            </div>
          </div>
        </div>

        <!-- 货物选择 - 搜索 -->
        <div class="form-row">
          <div class="form-group full">
            <label>选择货物</label>
            <div class="search-wrap">
              <input
                v-model="cargoText"
                @focus="showCargoList=true"
                @input="onSearchCargo"
                @blur="onBlurCargo"
                placeholder="输入货物名搜索"
                autocomplete="off"
              />
              <ul v-if="showCargoList" class="search-list">
                <li v-for="c in cargoResults" :key="c.cargo_id"
                    @mousedown.prevent="selectCargo(c)">
                  {{ c.cargo_name }}
                </li>
                <li v-if="cargoResults.length===0" class="empty">无匹配货物</li>
              </ul>
            </div>
          </div>
        </div>

        <button class="btn primary" @click="addCargo">+ 添加货物</button>

        <table class="table">
          <thead>
            <tr><th>货物名称</th><th>数量</th><th>操作</th></tr>
          </thead>
          <tbody>
            <tr v-for="(c, i) in cargoList" :key="i">
              <td>{{ c.cargo_name }}</td>
              <td>{{ c.quantity }}</td>
              <td><button class="btn delete" @click="removeCargo(i)">删除</button></td>
            </tr>
            <tr v-if="cargoList.length === 0">
              <td colspan="3" class="empty">暂无货物</td>
            </tr>
          </tbody>
        </table>

        <div class="actions">
          <button class="btn gray" @click="submit(true)">保存草稿</button>
          <button class="btn success" @click="submit(false)">提交</button>
          <button class="btn warning" @click="go('/order')">取消</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { api, fixAvatar } from "../utils/common.js"

const route = useRoute()
const router = useRouter()
const orderId = route.params.id

const user = reactive({ name: "", role: "", avatar: "" })
const customers = ref([])
const cargoList = ref([])
const form = ref({ customer: "", origin_port: "", destination_port: "" })
// 港口搜索
const originPortText = ref("")
const destPortText = ref("")
const portResults = ref([])
const showOriginList = ref(false)
const showDestList = ref(false)
let portTimer = null
let portFocus = null

// 货物搜索
const cargoText = ref("")
const cargoResults = ref([])
const showCargoList = ref(false)
let cargoTimer = null

const loadUser = async () => {
  const userRes = await api.get('/api/user_info/')
  user.value = fixAvatar(userRes.data)
  Object.assign(user, userRes.data)
}

const loadInit = async () => {
  const [o, c] = await Promise.all([
    api.get(`/api/order/${orderId}/`),
    api.get("/api/customers/")
  ])
  const order = o.data
  customers.value = c.data.data.customers

  // 补齐当前客户
  if (order.customer && !customers.value.find(x => x.customer_id === order.customer)) {
    customers.value.push({
      customer_id: order.customer,
      customer_name: order.customer_name || '客户#' + order.customer
    })
  }

  form.value.customer = order.customer
  form.value.origin_port = order.origin_port
  form.value.destination_port = order.destination_port

  // 显示当前港口名
  originPortText.value = order.origin_port_name || ''
  destPortText.value = order.destination_port_name || ''

  cargoList.value = order.cargo_list || []
}

// ===== 港口搜索 =====
const onSearchPort = (which) => {
  clearTimeout(portTimer)
  const val = which === 'origin' ? originPortText.value : destPortText.value
  portTimer = setTimeout(async () => {
    const res = await api.get('/api/ports/', { params: { keyword: val || '' } })
    portResults.value = res.data.list || []
    if (which === 'origin') showOriginList.value = true
    else showDestList.value = true
  }, 200)
}

const onFocusPort = (which) => {
  portFocus = which
  if (portResults.value.length === 0) onSearchPort(which)
  else if (which === 'origin') showOriginList.value = true
  else showDestList.value = true
}

const onBlurPort = (which) => {
  setTimeout(() => {
    if (which === 'origin') showOriginList.value = false
    else showDestList.value = false
  }, 150)
}

const selectPort = (which, p) => {
  if (which === 'origin') {
    originPortText.value = p.port_name
    form.value.origin_port = p.port_id
    showOriginList.value = false
  } else {
    destPortText.value = p.port_name
    form.value.destination_port = p.port_id
    showDestList.value = false
  }
}

// ===== 货物搜索 =====
const onSearchCargo = () => {
  clearTimeout(cargoTimer)
  cargoTimer = setTimeout(async () => {
    const res = await api.get('/api/cargos/', { params: { keyword: cargoText.value || '' } })
    cargoResults.value = res.data.list || []
    showCargoList.value = true
  }, 200)
}

const onBlurCargo = () => {
  setTimeout(() => { showCargoList.value = false }, 150)
}

const selectCargo = (c) => {
  const exist = cargoList.value.find(x => x.cargo_id === c.cargo_id)
  if (exist) { alert("已添加"); return }
  const qty = prompt("请输入数量", "1")
  if (!qty || isNaN(qty)) return
  cargoList.value.push({
    cargo_id: c.cargo_id,
    cargo_name: c.cargo_name,
    quantity: Number(qty)
  })
  cargoText.value = ''
  showCargoList.value = false
}

const addCargo = () => { }  // 由搜索选择替代

const removeCargo = (i) => { cargoList.value.splice(i, 1) }

const submit = async (isDraft) => {
  if (!form.value.customer) return alert("请选择客户")
  if (!form.value.origin_port) return alert("请选择出发港口")
  if (!form.value.destination_port) return alert("请选择目标港口")
  if (form.value.origin_port === form.value.destination_port) return alert("始发港和目的港不能相同")
  if (cargoList.value.length === 0) return alert("请添加货物")

  try {
    await api.post(`/api/order/update/${orderId}/`, {
      ...form.value,
      cargo_list: cargoList.value,
      is_draft: isDraft
    })
    alert("修改成功")
    router.push("/order")
  } catch (e) {
    alert(e.response?.data?.error || "失败")
  }
}

const go = (p) => router.push(p)

onMounted(() => {
  loadUser()
  loadInit()
})
</script>

<style scoped>
html, body { margin: 0; padding: 0; }

.sidebar {
  position: fixed; left: 0; top: 0; width: 240px; height: 100vh;
  background: #1a3a5f; color: #fff; display: flex; flex-direction: column;
}
.logo-container { padding: 20px; border-bottom: 1px solid rgba(255,255,255,0.1); }
.logo { display: flex; align-items: center; font-weight: bold; }
.logo i { margin-right: 10px; color: #3182ce; }

.nav-links { list-style: none; padding: 10px 0; margin: 0; }
.nav-links li { width: 100%; }
.nav-links a {
  display: flex; align-items: center; justify-content: center;
  width: 100%; height: 48px; color: rgba(255,255,255,0.8);
  text-decoration: none; transition: all 0.2s;
}
.nav-links i { margin-right: 8px; }
.nav-links a:hover { background: rgba(255,255,255,0.1); color: #fff; }
.nav-links a.active { background: rgba(255,255,255,0.15); color: #fff; border-left: 4px solid #3182ce; }

.main { margin-left: 220px; flex: 1; padding: 20px; background: #f5f7fa; }
.header { display: flex; justify-content: space-between; }
.user { display: flex; align-items: center; }
.user img { width: 40px; height: 40px; border-radius: 50%; margin-right: 10px; }

.form-row { display: flex; gap: 20px; margin-bottom: 15px; }
.form-group { flex: 1; position: relative; }
.full { flex: 100%; }
.form-group label { display: block; margin-bottom: 4px; font-size: 14px; color: #333; }

select, .search-wrap input {
  width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px;
  box-sizing: border-box;
}

/* 搜索下拉 */
.search-wrap { position: relative; }
.search-list {
  position: absolute; top: 100%; left: 0; right: 0; z-index: 99;
  max-height: 200px; overflow-y: auto;
  background: #fff; border: 1px solid #ddd; border-radius: 0 0 4px 4px;
  list-style: none; margin: 0; padding: 0; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.search-list li {
  padding: 8px 12px; cursor: pointer; font-size: 14px;
}
.search-list li:hover { background: #edf2f7; }
.search-list li.empty { color: #999; cursor: default; }

.table { width: 100%; background: white; margin-top: 20px; border-collapse: collapse; }
th, td { padding: 10px; border-bottom: 1px solid #eee; text-align: center; }

.btn { padding: 8px 14px; border-radius: 6px; border: none; cursor: pointer; }
.primary { background: #3182ce; color: white; }
.success { background: #38a169; color: white; }
.warning { background: #d69e2e; color: white; }
.gray { background: #718096; color: white; }
.delete { background: #e53e3e; color: white; }
.actions { margin-top: 20px; text-align: center; }
.empty { text-align: center; color: #999; }
</style>