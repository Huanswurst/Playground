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
          <h1 class="header-title">修改密码</h1>
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
              <h2>修改密码</h2>
            </div>
          </template>
          
          <el-form label-width="120px">
            <el-form-item label="旧密码">
              <el-input v-model="form.oldPassword" type="password" />
            </el-form-item>
            <el-form-item label="新密码">
              <el-input v-model="form.newPassword" type="password" />
            </el-form-item>
            <el-form-item label="确认密码">
              <el-input v-model="form.confirmPassword" type="password" />
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
import axios from 'axios'

const form = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})
const loading = ref(true)

const fetchUserInfo = async () => {
  try {
    await axios.get('/api/user/me')
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
    await axios.post('/api/user/change-password', form.value)
    // TODO: 显示成功提示
  } catch (error) {
    console.error('修改密码失败:', error)
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