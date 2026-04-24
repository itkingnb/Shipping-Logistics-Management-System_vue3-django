<template>
  <div class="layout">

    <!-- ===== 侧边栏（保持不变） ===== -->
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

    <!-- ===== 主体 ===== -->
    <div class="main">

      <!-- header -->
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

      <!-- ===== 卡片 ===== -->
      <div class="card form-card">

        <div class="card-header">
          订单信息填写
        </div>

        <div class="card-body">

          <!-- 基础信息 -->
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

              <div class="form-group">
                <label>出发港口</label>
                <select v-model="form.origin_port">
                  <option value="">请选择</option>
                  <option v-for="p in ports" :key="p.port_id" :value="p.port_id">
                    {{ p.port_name }}
                  </option>
                </select>
              </div>

              <div class="form-group">
                <label>目标港口</label>
                <select v-model="form.destination_port">
                  <option value="">请选择</option>
                  <option v-for="p in ports" :key="p.port_id" :value="p.port_id">
                    {{ p.port_name }}
                  </option>
                </select>
              </div>
            </div>
          </div>

          <!-- 货物 -->
          <div class="block">
            <div class="block-title">货物管理</div>

            <div class="form-row">
              <div class="form-group full">
                <select v-model="selectedCargo">
                  <option value="">请选择货物</option>
                  <option v-for="c in cargos" :key="c.cargo_id" :value="c">
                    {{ c.cargo_name }}
                  </option>
                </select>
              </div>
            </div>

            <button class="btn primary" @click="addCargo">
              + 添加货物
            </button>

            <table class="table modern">
              <thead>
                <tr>
                  <th>货物名称</th>
                  <th>数量</th>
                  <th>操作</th>
                </tr>
              </thead>

              <tbody>
                <tr v-for="(c, i) in cargoList" :key="i">
                  <td>{{ c.cargo_name }}</td>
                  <td>{{ c.quantity }}</td>
                  <td>
                    <button class="btn delete" @click="removeCargo(i)">删除</button>
                  </td>
                </tr>

                <tr v-if="cargoList.length === 0">
                  <td colspan="3" class="empty">暂无货物</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- 操作 -->
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
const ports = ref([])
const cargos = ref([])

const selectedCargo = ref('')
const cargoList = ref([])

const form = ref({
  customer: '',
  origin_port: '',
  destination_port: ''
})

const loadUser = async () => {
  const res = await api.get('/api/user_info/')
  Object.assign(user, fixAvatar(res.data))
}

const loadInit = async () => {
  const [c, p, g] = await Promise.all([
    api.get('/api/customers/'),
    api.get('/api/ports/'),
    api.get('/api/cargos/')
  ])

  customers.value = c.data.data.customers
  ports.value = p.data.list
  cargos.value = g.data.list
}

const addCargo = () => {
  if (!selectedCargo.value) return alert('请选择货物')

  const exist = cargoList.value.find(
    x => x.cargo_id === selectedCargo.value.cargo_id
  )
  if (exist) return alert('已添加')

  const qty = prompt('输入数量', '1')
  if (!qty || isNaN(qty)) return

  cargoList.value.push({
    cargo_id: selectedCargo.value.cargo_id,
    cargo_name: selectedCargo.value.cargo_name,
    quantity: Number(qty)
  })
}

const removeCargo = (i) => {
  cargoList.value.splice(i, 1)
}

const submit = async (isDraft) => {
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
  form.value = {
    customer: '',
    origin_port: '',
    destination_port: ''
  }
  cargoList.value = []
}

onMounted(() => {
  loadUser()
  loadInit()
})
</script>

<style scoped>

/* ===== 主体 ===== */
.main {
  margin-left: 240px;
  padding: 30px;
  background: #f4f7fb;
}

/* ===== Header ===== */
.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 25px;
}

.card-shadow {
  background: white;
  padding: 15px 20px;
  border-radius: 12px;
  box-shadow: 0 6px 18px rgba(0,0,0,0.06);
}

/* ===== 用户 ===== */
.user {
  display: flex;
  align-items: center;
}
.user img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

/* ===== 卡片 ===== */
.form-card {
  background: white;
  border-radius: 14px;
  box-shadow: 0 12px 35px rgba(0,0,0,0.06);
}

.card-header {
  padding: 18px 25px;
  background: linear-gradient(135deg,#3182ce,#2b6cb0);
  color: white;
  font-weight: 600;
}

.card-body {
  padding: 25px;
}

/* ===== 分块 ===== */
.block {
  margin-bottom: 30px;
}
.block-title {
  font-weight: 600;
  margin-bottom: 10px;
  border-left: 4px solid #3182ce;
  padding-left: 8px;
}

/* ===== 表单 ===== */
.form-row {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
}
.form-group { flex: 1 }
.full { flex: 100% }

select {
  width: 100%;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

/* ===== 表格 ===== */
.table {
  width: 100%;
  margin-top: 15px;
}
.table th, .table td {
  padding: 10px;
}

/* ===== 按钮 ===== */
.btn {
  padding: 8px 16px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
}
.primary { background:#3182ce;color:white }
.success { background:#38a169;color:white }
.warning { background:#ed8936;color:white }
.gray { background:#718096;color:white }
.delete { background:#e53e3e;color:white }

.actions {
  text-align: center;
  margin-top: 20px;
}

.empty {
  text-align: center;
  color: #999;
}

</style>