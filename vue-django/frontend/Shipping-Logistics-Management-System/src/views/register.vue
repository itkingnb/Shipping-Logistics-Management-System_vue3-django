<template>
  <div class="container">

    <div class="register-box">

      <h1>🚢 航运物流公司管理系统</h1>

      <form @submit.prevent="handleRegister">

        <!-- 用户名 -->
        <div class="form-group">
          <label>用户名</label>
          <input
            v-model="form.username"
            type="text"
            placeholder="请输入用户名"
          >
        </div>

        <!-- 电话 -->
        <div class="form-group">
          <label>电话</label>
          <input
            v-model="form.telephone"
            type="text"
            placeholder="请输入电话"
          >
        </div>

        <!-- 邮箱 -->
        <div class="form-group">
          <label>邮箱</label>
          <input
            v-model="form.email"
            type="text"
            placeholder="请输入邮箱"
          >
        </div>

        <!-- 角色 -->
        <div class="form-group">
          <label>角色</label>

          <select v-model="form.role">
            <option value="">请选择角色</option>

            <option
              v-for="item in roles"
              :key="item"
              :value="item"
            >
              {{ item }}
            </option>

          </select>
        </div>

        <!-- 密码 -->
        <div class="form-group">
          <label>密码</label>

          <div class="password-box">
            <input
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="请输入密码"
            >

            <span
              class="toggle-btn"
              @click="showPassword = !showPassword"
            >
              {{ showPassword ? '🙈' : '👁️' }}
            </span>
          </div>
        </div>

        <!-- 确认密码 -->
        <div class="form-group">
          <label>确认密码</label>

          <div class="password-box">
            <input
              v-model="form.password2"
              :type="showPassword2 ? 'text' : 'password'"
              placeholder="请再次输入密码"
            >

            <span
              class="toggle-btn"
              @click="showPassword2 = !showPassword2"
            >
              {{ showPassword2 ? '🙈' : '👁️' }}
            </span>
          </div>
        </div>

        <!-- 按钮 -->
        <div class="btn-group">

          <button
            type="button"
            class="back-btn"
            @click="router.push('/')"
          >
            返回登录
          </button>

          <button type="submit">
            注册
          </button>

        </div>

      </form>

      <!-- 错误提示 -->
      <div
        class="error-box"
        v-if="errors.length"
      >

        <div
          class="error-item"
          v-for="(item,index) in errors"
          :key="index"
        >
          {{ item }}
        </div>

      </div>

    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../utils/common'

const router = useRouter()

const roles = ref([
  '管理员',
  '操作员',
  '指派员',
  '运输员'
])

const showPassword = ref(false)
const showPassword2 = ref(false)

const errors = ref([])
const form = ref({
  username: '',
  telephone: '',
  email: '',
  role: '',
  password: '',
  password2: ''
})

const handleRegister = async () => {
  errors.value = []
  try {
    const res = await api.post(
      'http://127.0.0.1:8000/api/register/',
      form.value
    )
    alert(res.data.message)
    router.push('/')
  } catch (err) {
    if (err.response) {
      errors.value = err.response.data.errors
    } else {
      errors.value = ['服务器异常']
    }
  }
}
</script>

<style scoped>

.container{
  width:100%;
  height:100vh;
  display:flex;
  justify-content:center;
  align-items:center;
  background: linear-gradient(135deg,#1a2980,#26d0ce);
  padding:20px;
}

.register-box{
  width:420px;
  background:white;
  padding:35px;
  border-radius:15px;
  box-shadow:0 10px 30px rgba(0,0,0,0.2);
}

h1{
  text-align:center;
  margin-bottom:25px;
  color:#1a2980;
  font-size:28px;
}

.form-group{
  margin-bottom:18px;
}

.form-group label{
  display:block;
  margin-bottom:8px;
  color:#555;
  font-weight:600;
}

input,
select{
  width:100%;
  padding:12px;
  border:1px solid #ddd;
  border-radius:8px;
  font-size:15px;
  transition:0.3s;
}

input:focus,
select:focus{
  border-color:#1a2980;
  outline:none;
  box-shadow:0 0 5px rgba(26,41,128,0.3);
}

/* 密码框 */
.password-box{
  position:relative;
}

.toggle-btn{
  position:absolute;
  right:12px;
  top:50%;
  transform:translateY(-50%);
  cursor:pointer;
  user-select:none;
}

/* 按钮区域 */
.btn-group{
  display:flex;
  gap:15px;
  margin-top:25px;
}

.btn-group button{
  flex:1;
  padding:12px;
  border:none;
  border-radius:8px;
  color:white;
  font-size:16px;
  cursor:pointer;
  transition:0.3s;
}

.btn-group button:hover{
  transform:translateY(-2px);
}

/* 返回按钮 */
.back-btn{
  background:#888;
}

/* 注册按钮 */
button[type="submit"]{
  background:linear-gradient(to right,#1a2980,#26d0ce);
}

/* 错误提示 */
.error-box{
  margin-top:20px;
  background:#ffecec;
  padding:12px;
  border-radius:8px;
}

.error-item{
  color:red;
  margin-bottom:5px;
  font-size:14px;
}

@media (max-width:480px){

  .register-box{
    width:100%;
    padding:25px;
  }

  h1{
    font-size:22px;
  }

}

</style>