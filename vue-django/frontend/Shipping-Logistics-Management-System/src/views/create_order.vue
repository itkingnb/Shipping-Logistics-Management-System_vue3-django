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
      <div class="header card-shadow">
        <h2>创建订单</h2>
        <div class="user">
          <img :src="user.avatar || defaultAvatar" />
          <div>
            <div>{{ user.name }}</div>
            <small>{{ user.role }}</small>
          </div>
        </div>
      </div>

      <div class="card form-card">
        <div class="card-header">订单信息填写</div>
        <div class="card-body">

          <div class="block">
            <div class="block-title">基础信息</div>
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
                  <input v-model="originPortText" @focus="onFocusPort('origin')"
                    @input="onSearchPort" @blur="onBlurPort('origin')"
                    placeholder="输入港口名搜索" autocomplete="off" />
                  <ul v-if="showOriginList" class="search-list">
                    <li v-for="p in portResults" :key="p.port_id"
                        @mousedown.prevent="selectPort('origin', p)">{{ p.port_name }}</li>
                    <li v-if="portResults.length===0" class="empty">无匹配港口</li>
                  </ul>
                </div>
              </div>

              <!-- 目标港口 - 搜索 -->
              <div class="form-group">
                <label>目标港口</label>
                <div class="search-wrap">
                  <input v-model="destPortText" @focus="onFocusPort('dest')"
                    @input="onSearchPort" @blur="onBlurPort('dest')"
                    placeholder="输入港口名搜索" autocomplete="off" />
                  <ul v-if="showDestList" class="search-list">
                    <li v-for="p in portResults" :key="p.port_id"
                        @mousedown.prevent="selectPort('dest', p)">{{ p.port_name }}</li>
                    <li v-if="portResults.length===0" class="empty">无匹配港口</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <div class="block">
            <div class="block-title">货物管理</div>
            <div class="form-row">
              <div class="form-group full">
                <div class="search-wrap">
                  <input v-model="cargoText" @focus="showCargoList=true"
                    @input="onSearchCargo" @blur="onBlurCargo"
                    placeholder="输入货物名搜索" autocomplete="off" />
                  <ul v-if="showCargoList" class="search-list">
                    <li v-for="c in cargoResults" :key="c.cargo_id"
                        @mousedown.prevent="selectCargo(c)">{{ c.cargo_name }}</li>
                    <li v-if="cargoResults.length===0" class="empty">无匹配货物</li>
                  </ul>
                </div>
              </div>
            </div>

            <button class="btn primary" @click="addCargo">+ 添加货物</button>

            <table class="table modern">
              <thead><tr><th>货物名称</th><th>数量</th><th>操作</th></tr></thead>
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
          </div>

          <div class="actions">
            <button class="btn gray" @click="submit(true)">保存草稿</button>
            <button class="btn success" @click="submit(false)">提交订单</button>
            <button class="btn warning" @click="reset">重置</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api, fixAvatar } from '../utils/common'

const router = useRouter()
const user = reactive({})
const defaultAvatar = '/avatar.png'

const customers = ref([])
const cargoList = ref([])
const form = ref({ customer: '', origin_port: '', destination_port: '' })

// 港口搜索
const originPortText = ref('')
const destPortText = ref('')
const portResults = ref([])
const showOriginList = ref(false)
const showDestList = ref(false)
let portTimer = null

// 货物搜索
const cargoText = ref('')
const cargoResults = ref([])
const showCargoList = ref(false)
let cargoTimer = null

const loadUser = async () => {
  const res = await api.get('/api/user_info/')
  Object.assign(user, fixAvatar(res.data))
}

const loadInit = async () => {
  const c = await api.get('/api/customers/')
  customers.value = c.data.data.customers
}

// ===== 港口搜索 =====
const onSearchPort = () => {
  clearTimeout(portTimer)
  const val = (showOriginList.value ? originPortText.value : destPortText.value) || ''
  portTimer = setTimeout(async () => {
    const res = await api.get('/api/ports/', { params: { keyword: val } })
    portResults.value = res.data.list || []
  }, 200)
}

const onFocusPort = (which) => {
  if (which === 'origin') showOriginList.value = true
  else showDestList.value = true
  if (portResults.value.length === 0) onSearchPort()
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
  if (exist) { alert('已添加'); return }
  const qty = prompt('输入数量', '1')
  if (!qty || isNaN(qty)) return
  cargoList.value.push({
    cargo_id: c.cargo_id,
    cargo_name: c.cargo_name,
    quantity: Number(qty)
  })
  cargoText.value = ''
  showCargoList.value = false
}

const addCargo = () => {}

const removeCargo = (i) => { cargoList.value.splice(i, 1) }

const submit = async (isDraft) => {
  if (!form.value.customer) return alert('请选择客户')
  if (!form.value.origin_port) return alert('请选择出发港口')
  if (!form.value.destination_port) return alert('请选择目标港口')
  if (form.value.origin_port === form.value.destination_port) return alert('始发港和目的港不能相同')
  if (cargoList.value.length === 0) return alert('请添加货物')

  try {
    await api.post('/api/create_order/', {
      customer: form.value.customer,
      origin_port: form.value.origin_port,
      destination_port: form.value.destination_port,
      cargo_list: cargoList.value,
      is_draft: isDraft
    })
    alert('创建成功')
    router.push('/order')
  } catch (err) {
    alert(err.response?.data?.error || '服务器错误')
  }
}

const reset = () => {
  form.value = { customer: '', origin_port: '', destination_port: '' }
  originPortText.value = ''
  destPortText.value = ''
  cargoList.value = []
}

onMounted(() => {
  loadUser()
  loadInit()
})
</script>

<style scoped>
.main { margin-left: 240px; padding: 30px; background: #f4f7fb; }
.header { display: flex; justify-content: space-between; margin-bottom: 25px; }
.card-shadow { background: white; padding: 15px 20px; border-radius: 12px; box-shadow: 0 6px 18px rgba(0,0,0,0.06); }
.user { display: flex; align-items: center; }
.user img { width: 40px; height: 40px; border-radius: 50%; margin-right: 10px; }

.form-card { background: white; border-radius: 14px; box-shadow: 0 12px 35px rgba(0,0,0,0.06); }
.card-header { padding: 18px 25px; background: linear-gradient(135deg,#3182ce,#2b6cb0); color: white; font-weight: 600; }
.card-body { padding: 25px; }

.block { margin-bottom: 30px; }
.block-title { font-weight: 600; margin-bottom: 10px; border-left: 4px solid #3182ce; padding-left: 8px; }

.form-row { display: flex; gap: 20px; margin-bottom: 15px; }
.form-group { flex: 1; position: relative; }
.full { flex: 100%; }
.form-group label { display: block; margin-bottom: 4px; font-size: 14px; color: #333; }

select, .search-wrap input {
  width: 100%; padding: 10px; border-radius: 8px; border: 1px solid #e2e8f0;
  font-size: 14px; box-sizing: border-box;
}

.search-wrap { position: relative; }
.search-list {
  position: absolute; top: 100%; left: 0; right: 0; z-index: 99;
  max-height: 200px; overflow-y: auto;
  background: #fff; border: 1px solid #ddd; border-radius: 0 0 4px 4px;
  list-style: none; margin: 0; padding: 0; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.search-list li { padding: 8px 12px; cursor: pointer; font-size: 14px; }
.search-list li:hover { background: #edf2f7; }
.search-list li.empty { color: #999; cursor: default; }

.table { width: 100%; margin-top: 15px; border-collapse: collapse; }
.table th, .table td { padding: 10px; text-align: center; }

.btn { padding: 8px 16px; border-radius: 8px; border: none; cursor: pointer; }
.primary { background:#3182ce;color:white }
.success { background:#38a169;color:white }
.warning { background:#ed8936;color:white }
.gray { background:#718096;color:white }
.delete { background:#e53e3e;color:white }
.actions { text-align: center; margin-top: 20px; }
.empty { text-align: center; color: #999; }
</style>
