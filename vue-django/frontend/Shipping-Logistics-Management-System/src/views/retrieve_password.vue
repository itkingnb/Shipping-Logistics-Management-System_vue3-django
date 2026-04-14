<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

const username = ref('')
const password = ref('')
const password2 = ref('')
const msg = ref('')

const show1 = ref(false)
const show2 = ref(false)

const handleSubmit = async () => {
  if (password.value !== password2.value) {
    msg.value = '两次密码不一致'
    return
  }

  try {
    const res = await axios.post('http://127.0.0.1:8000/api/retrieve_password/', {
      username: username.value,
      password: password.value,
      password2: password2.value
    })

    if (res.data.success) {
      alert('修改成功')
      router.push('/')
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
    <!-- 波浪 -->
    <div class="wave"></div>
    <div class="wave wave2"></div>
    <div class="wave wave3"></div>

    <!-- 船 -->
    <div class="ship-icon">⛵</div>

    <!-- 卡片 -->
    <div class="login-container">
      <div class="login-header">
        <h1>
          <span class="icon">🚢</span>
          航运物流公司管理系统
        </h1>
        <p>修改密码</p>
      </div>

      <div v-if="msg" class="alert">
        {{ msg }}
      </div>

      <!-- 用户名 -->
      <div class="form-group">
        <label>用户名 / 邮箱</label>
        <input v-model="username" class="form-control" />
      </div>

      <!-- 密码 -->
      <div class="form-group">
        <label>新密码</label>
        <input
          :type="show1 ? 'text' : 'password'"
          v-model="password"
          class="form-control"
        />
        <span class="toggle" @click="show1 = !show1">
          {{ show1 ? '🔒' : '👁️' }}
        </span>
      </div>

      <!-- 确认密码 -->
      <div class="form-group">
        <label>确认密码</label>
        <input
          :type="show2 ? 'text' : 'password'"
          v-model="password2"
          class="form-control"
        />
        <span class="toggle" @click="show2 = !show2">
          {{ show2 ? '🔒' : '👁️' }}
        </span>
      </div>

      <!-- 按钮 -->
      <div class="btn-group">
        <button class="back-btn" @click="router.push('/')">返回</button>
        <button class="login-btn" @click="handleSubmit">修改密码</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page {
  position: relative;
  height: 100vh;
  background: linear-gradient(135deg, #1a2980, #26d0ce);
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.wave {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 100px;
  background: rgba(0, 123, 255, 0.2);
}

.wave2 {
  bottom: 10px;
  opacity: 0.5;
}

.wave3 {
  bottom: 20px;
  opacity: 0.3;
}

/* 🚢 船 */
.ship-icon {
  position: absolute;
  bottom: 50px;
  left: -100px;
  font-size: 36px;
  opacity: 0.7;
  animation: ship 25s linear infinite;
}

@keyframes ship {
  from { left: -100px; }
  to { left: 100%; }
}

/* 卡片 */
.login-container {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  width: 360px;
  padding: 35px 28px;
  box-shadow: 0 15px 30px rgba(0,0,0,0.2);
}

/* 标题 */
.login-header {
  text-align: center;
  margin-bottom: 25px;
}

.login-header h1 {
  font-size: 24px;  
  color: #1a2980;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin-bottom: 5px;
}

.login-header .icon {
  font-size: 26px;
}

.login-header p {
  font-size: 13px;
  color: #666;
}

/* 输入框 */
.form-group {
  margin-bottom: 18px;  /*更紧凑 */
  position: relative;
}

.form-group label {
  font-size: 14px;
  color: #555;
  margin-bottom: 6px;
  display: block;
}

.form-control {
  width: 100%;
  padding: 11px 12px;
  border-radius: 8px;
  border: 1px solid #ddd;
  font-size: 14px;
}

.form-control:focus {
  border-color: #1a2980;
  box-shadow: 0 0 0 2px rgba(26,41,128,0.2);
}

/* 👁 */
.toggle {
  position: absolute;
  right: 10px;
  top: 34px;
  cursor: pointer;
}

/* 按钮 */
.btn-group {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.login-btn {
  flex: 1;
  padding: 11px;
  background: linear-gradient(to right, #1a2980, #26d0ce);
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 14px;
  cursor: pointer;
}

.back-btn {
  flex: 1;
  padding: 11px;
  background: #ddd;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

/* 提示 */
.alert {
  background: #ffecec;
  padding: 8px;
  margin-bottom: 12px;
  border-radius: 6px;
  font-size: 13px;
  text-align: center;
}
</style>