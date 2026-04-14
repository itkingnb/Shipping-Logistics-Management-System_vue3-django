<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
axios.defaults.baseURL = 'http://127.0.0.1:8000'
axios.defaults.withCredentials = true
const router = useRouter()
const username = ref('')
const password = ref('')
const remember = ref(false)
const msg = ref('')
const showPassword = ref(false)

// 登录
const handleLogin = async () => {
  try {
    const res = await axios.post('/api/login/', {
      username: username.value,
      password: password.value,
      remember: remember.value,
    }, {
      withCredentials: true
    })

    if (res.data.success) {
      msg.value = '登录成功'

      const role = res.data.user.role
      const user = res.data.user
      localStorage.setItem('user', JSON.stringify(user))

      if (role === '管理员') {
        router.push('/admin')
      } else if (role === '操作员') {
        router.push('/operator')
      } else if (role === '指派员') {
        router.push('/appointer')
      } else if (role === '运输员') {
        router.push('/transporter')
      } else {
        msg.value = '未知角色'
      }

    } else {
      msg.value = res.data.msg
    }

  } catch (e) {
    msg.value = '请求失败'
  }
}
</script>

<template>
  <div class="page">
    <!-- 波浪背景 -->
    <div class="wave"></div>
    <div class="wave wave2"></div>
    <div class="wave wave3"></div>

    <!-- 船 -->
    <div class="ship">⛵</div>

    <div class="login-container">
      <div class="login-header">
        <h1>🚢 航运物流公司管理系统</h1>
        <p>Shipping Logistics Management System</p>
      </div>

      <div v-if="msg" class="alert">
        {{ msg }}
      </div>

      <!-- 用户名 -->
      <div class="form-group">
        <input v-model="username" required />
        <label>用户名 / 邮箱</label>
      </div>

      <!-- 密码 -->
      <div class="form-group">
        <input
          :type="showPassword ? 'text' : 'password'"
          v-model="password"
          required
        />
        <label>密码</label>
        <span class="toggle" @click="showPassword = !showPassword">
          {{ showPassword ? '🔒' : '👁️' }}
        </span>
      </div>

      <!-- 选项 -->
      <div class="options">
        <label>
          <input type="checkbox" v-model="remember" />
          记住我
        </label>
        <router-link to="/retrieve">忘记密码?</router-link>
      </div>

      <!-- 按钮 -->
      <button type="button" class="login-btn" @click="handleLogin">
        登录系统
      </button>

      <div class="footer">
        还没有账户？<a href="#">注册</a>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 背景 */
.page {
  position: relative;
  height: 100vh;
  background: linear-gradient(135deg, #1a2980, #26d0ce);
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

/* 波浪 */
.wave {
  position: absolute;
  bottom: 0;
  width: 200%;
  height: 120px;
  background: rgba(255,255,255,0.15);
  border-radius: 40%;
  animation: wave 12s linear infinite;
}

.wave2 {
  bottom: 10px;
  opacity: 0.5;
  animation-duration: 18s;
}

.wave3 {
  bottom: 20px;
  opacity: 0.3;
  animation-duration: 25s;
}

@keyframes wave {
  from { transform: translateX(0); }
  to { transform: translateX(-50%); }
}

/* 船 */
.ship {
  position: absolute;
  bottom: 70px;
  left: -100px;
  font-size: 40px;
  animation: shipMove 20s linear infinite;
}

@keyframes shipMove {
  from { left: -100px; }
  to { left: 100%; }
}

/* 登录卡片 */
.login-container {
  background: rgba(255,255,255,0.95);
  border-radius: 16px;
  padding: 40px;
  width: 380px;
  box-shadow: 0 15px 40px rgba(0,0,0,0.2);
}

/* 标题 */
.login-header {
  text-align: center;
  margin-bottom: 25px;
}

.login-header h1 {
  color: #1a2980;
  font-size: 26px;
}

.login-header p {
  font-size: 13px;
  color: #666;
}

/* 输入框 */
.form-group {
  position: relative;
  margin-bottom: 25px;
}

.form-group input {
  width: 100%;
  padding: 16px 10px 6px;
  border: none;
  border-bottom: 2px solid #ccc;
  outline: none;
  font-size: 15px;
}

.form-group label {
  position: absolute;
  left: 8px;
  top: 14px;
  background: white;
  padding: 0 4px;
  font-size: 14px;
  color: #666;
  transition: 0.3s;
}

.form-group input:focus + label,
.form-group input:valid + label {
  top: -8px;
  font-size: 12px;
  color: #1a2980;
}

.form-group input:focus {
  border-bottom: 2px solid #1a2980;
}

/* 密码按钮 */
.toggle {
  position: absolute;
  right: 10px;
  top: 12px;
  cursor: pointer;
}

/* 选项 */
.options {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  margin-bottom: 20px;
}

.options a {
  color: #1a2980;
}

/* 按钮 */
.login-btn {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 8px;
  background: linear-gradient(to right, #1a2980, #26d0ce);
  color: white;
  font-size: 16px;
  cursor: pointer;
  transition: 0.3s;
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}

/* 提示 */
.alert {
  background: #e3f2fd;
  padding: 10px;
  border-radius: 6px;
  margin-bottom: 15px;
  text-align: center;
}

/* 底部 */
.footer {
  text-align: center;
  margin-top: 15px;
  font-size: 13px;
}

.footer a {
  color: #1a2980;
}
</style>