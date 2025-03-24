<template>
  <el-card class="profile-card">
          <template #header>
            <div class="card-header">
              <h2>修改密码</h2>
            </div>
          </template>
          
          <div class="user-info">
            <el-text>当前用户：{{ userInfo.username }}</el-text>
            <el-text type="info" style="margin-left: 20px;">学号：{{ userInfo.student_number }}</el-text>
          </div>
          
          <el-form label-width="120px">
            <el-form-item label="旧密码">
              <el-input v-model="form.old_password" type="password" />
            </el-form-item>
            <el-form-item label="新密码">
              <el-input v-model="form.new_password" type="password" />
            </el-form-item>
            <el-form-item label="确认密码">
              <el-input v-model="form.confirm_password" type="password" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="onSubmit">保存</el-button>
            </el-form-item>
          </el-form>
        </el-card>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loading = ref(false)

const userInfo = ref({
  username: '',
  student_number: ''
})

const form = ref({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

const fetchUserInfo = async () => {
  try {
    const userId = localStorage.getItem('userId')
    const token = localStorage.getItem('authToken')
    const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
    
    const response = await fetch(`${baseURL}/api/users/${userId}/`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (!response.ok) {
      throw new Error('获取用户信息失败')
    }
    
    const data = await response.json()
    userInfo.value = {
      username: data.user.username,
      student_number: data.student_number
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
    ElMessage.error('获取用户信息失败')
  }
}

fetchUserInfo()

const onSubmit = async () => {
  try {
    loading.value = true
    
    const userId = localStorage.getItem('userId')
    const token = localStorage.getItem('authToken')
    
    if (!userId || !token) {
      ElMessage.error('请先登录')
      await router.push('/login')
      return
    }
    
    const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
    
    const response = await fetch(`${baseURL}/api/users/change-password/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        old_password: form.value.old_password,
        new_password: form.value.new_password
      })
    })
    
    if (response.status === 401) {
      localStorage.clear()
      ElMessage.error('登录已过期，请重新登录')
      await router.push('/login')
      return
    }
    
    if (!response.ok) {
      const responseClone = response.clone() // 克隆响应以多次读取
      let errorMessage = '修改密码失败'
      try {
        const errorData = await responseClone.json()
        errorMessage = errorData.detail || errorData.message || errorMessage
      } catch (e) {
        // 处理非 JSON 响应
        const text = await responseClone.text()
        errorMessage = text.includes('<!DOCTYPE') ? '服务器错误' : text
      }
      throw new Error(errorMessage)
    }
    
    ElMessage.success('密码修改成功')
    form.value = {
      old_password: '',
      new_password: '',
      confirm_password: ''
    }
  } catch (error) {
    console.error('修改密码失败:', error)
    ElMessage.error(error.message || '修改密码失败，请稍后重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.profile-card {
  margin: 20px;
  max-width: 800px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.profile-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.2);
}

.dashboard-header {
  background-color: #fff;
  border-bottom: 1px solid #e4e7ed;
  padding: 0 20px;
  height: 60px;
  display: flex;
  align-items: center;
}

.header-content {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-title {
  margin: 0;
  font-size: 20px;
  font-weight: 500;
  color: #303133;
}

.toggle-button {
  margin-right: 20px;
  padding: 0;
  border: none;
  background: none;
  cursor: pointer;
}

.logout-button {
  margin-left: auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: bold;
  color: #409eff;
}

.el-form-item:last-child {
  text-align: right;
}

.el-button {
  transition: all 0.3s ease;
}

.el-button:hover {
  transform: scale(1.05);
}
</style>
