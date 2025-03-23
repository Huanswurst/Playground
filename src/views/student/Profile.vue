<template>
  <StudentLayout title="个人信息">
    <el-main>
        <el-card class="profile-card">
          <template #header>
            <div class="card-header">
              <h2>个人信息</h2>
            </div>
          </template>
          
          <el-form label-width="120px">
            <el-form-item label="姓名">
              <el-input v-model="form.name" />
            </el-form-item>
            <el-form-item label="学号">
              <el-input v-model="form.studentId" disabled />
            </el-form-item>
            <el-form-item label="邮箱">
              <el-input v-model="form.email" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="onSubmit">保存</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-main>
  </StudentLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import StudentLayout from '@/layouts/StudentLayout.vue'
import axios from 'axios'

const router = useRouter()
const loading = ref(true)

const form = ref({
  name: '',
  studentId: '',
  email: ''
})

const fetchUserInfo = async () => {
  try {
    const userId = sessionStorage.getItem('userId')
    const response = await axios.get(`/api/user/${userId}`)
    form.value = response.data
  } catch (error) {
    console.error('获取用户信息失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchUserInfo()
})

const onSubmit = async () => {
  try {
    await axios.put('/api/user/me', form.value)
    // TODO: 显示成功提示
  } catch (error) {
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
