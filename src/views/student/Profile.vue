<template>
  <el-container>
    <el-aside
      :class="{ 'attendance-sidebar': true, collapsed: isSidebarCollapsed }"
      :style="{ width: isSidebarCollapsed ? '0' : '200px' }"
    >
      <el-menu
        default-active="1"
        class="el-menu-vertical-demo"
        v-if="!isSidebarCollapsed"
        router
      >
        <el-sub-menu index="1">
          <template #title>
            <el-icon><calendar /></el-icon>
            <span>考勤管理</span>
          </template>
          <el-menu-item index="/student/attendance">考勤记录</el-menu-item>
          <el-menu-item index="/student/attendance/statistics">考勤统计</el-menu-item>
          <el-menu-item index="/student/attendance/apply">考勤申诉</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="2">
          <template #title>
            <el-icon><notebook /></el-icon>
            <span>课程信息</span>
          </template>
          <el-menu-item index="/student/course/schedule">课程表</el-menu-item>
          <el-menu-item index="/student/course/materials">课程资料</el-menu-item>
          <el-menu-item index="/student/course/assignments">作业提交</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="4">
          <template #title>
            <el-icon><user /></el-icon>
            <span>个人中心</span>
          </template>
          <el-menu-item index="/student/profile">个人信息</el-menu-item>
          <el-menu-item index="/student/password">修改密码</el-menu-item>
          <el-menu-item index="/student/notification">消息通知</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>
    
    <el-container>
      <el-header class="dashboard-header">
        <div class="header-content">
          <el-button
            type="link"
            class="toggle-button"
            @click="toggleSidebar"
            aria-label="Toggle menu"
          >
            <el-icon :size="24" style="vertical-align: middle;">
              <component :is="isSidebarCollapsed ? Expand : Fold" />
            </el-icon>
          </el-button>
          <h1 class="header-title">个人信息</h1>
          <el-button
            type="danger"
            class="logout-button"
            @click="handleLogout"
            style="margin-left: 15px"
          >
            退出登录
          </el-button>
        </div>
      </el-header>
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
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Expand, Fold } from '@element-plus/icons-vue'
import { Calendar, Notebook, User } from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()
const isSidebarCollapsed = ref(false)
const loading = ref(true)

const form = ref({
  name: '',
  studentId: '',
  email: ''
})

const fetchUserInfo = async () => {
  try {
    const response = await axios.get('/api/user/me')
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

const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
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
