<template>
  <el-card class="profile-card">
          <template #header>
            <div class="card-header">
              <h2>个人信息</h2>
            </div>
          </template>
          
          <el-form label-width="120px">
            <el-form-item label="用户名">
              <el-input v-model="form.user.username" />
            </el-form-item>
            <el-form-item label="学号">
              <el-input v-model="form.student_number" disabled />
            </el-form-item>
            <el-form-item label="邮箱">
              <el-input v-model="form.user.email" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="onSubmit">保存</el-button>
            </el-form-item>
          </el-form>
        </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loading = ref(true)

const form = ref({
  user: {
    username: '',
    email: '',
    role: ''
  },
  student_number: ''
})

    const fetchUserInfo = async () => {
      try {
        console.log('开始获取用户信息...')
        const userId = localStorage.getItem('userId')
        const token = localStorage.getItem('authToken')
        
        if (!userId || !token) {
          console.error('未找到用户凭证')
          localStorage.clear()
          ElMessage.error('请先登录')
          await router.push('/login')
          return
        }
        
        const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
        console.log('API Base URL:', baseURL)
        
        const response = await fetch(`${baseURL}/api/users/${userId}/`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          credentials: 'include'
        })
        
        if (!response.ok) {
          const errorData = await response.json();
          console.error('获取用户信息失败:', errorData);
          
          if (response.status === 401) {
            localStorage.clear();
            ElMessage.error('登录已过期，请重新登录');
            await router.push('/login');
            return;
          }
          
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        
        const data = await response.json()
        console.log('API响应:', response)
        console.log('响应数据:', data)
        
        // 更新表单数据
        form.value = {
          user: data.user,
          student_number: data.student_number
        }
        
        console.log('成功获取用户信息:', form.value)
      } catch (error) {
        console.error('获取用户信息失败:', error)
        ElMessage.error('获取用户信息失败，请稍后重试')
        if (error.message.includes('401')) {
          localStorage.clear()
          await router.push('/login')
        }
      } finally {
        loading.value = false
      }
    }

onMounted(() => {
  fetchUserInfo()
})

const onSubmit = async () => {
  try {
    const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
    console.log('PUT API Base URL:', baseURL)
    const userId = localStorage.getItem('userId')
    const token = localStorage.getItem('authToken')
    
    if (!userId || !token) {
      ElMessage.error('请先登录')
      await router.push('/login')
      return
    }
    
    const response = await fetch(`${baseURL}/api/users/${userId}/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(form.value)
    })
    
    if (response.status === 401) {
      localStorage.clear()
      ElMessage.error('登录已过期，请重新登录')
      await router.push('/login')
      return
    }
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    console.log('用户信息更新成功:', data)
    ElMessage.success('用户信息更新成功')
  } catch (error) {
    console.error('更新用户信息失败:', error)
    ElMessage.error('更新用户信息失败，请稍后重试')
    console.error('更新用户信息失败:', error)
  }
}

const handleLogout = () => {
  router.push('/login')
}
</script>

<style scoped>
.profile-card {
  margin: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.profile-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.2);
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
