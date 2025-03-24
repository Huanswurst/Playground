<template>
  <div class="layout-container">
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
          <el-menu-item index="/student/dashboard">
            <el-icon><House /></el-icon>
            <span>首页</span>
          </el-menu-item>

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
            <el-menu-item index="/student/course-schedule">课程表</el-menu-item>
              <!-- <el-menu-item index="/student/course/materials">课程资料</el-menu-item> -->
            <!-- <el-menu-item index="/student/course/assignments">作业提交</el-menu-item> -->
          </el-sub-menu>

          <el-sub-menu index="4">
            <template #title>
              <el-icon><user /></el-icon>
              <span>个人中心</span>
            </template>
            <el-menu-item index="/student/profile">个人信息</el-menu-item>
            <el-menu-item index="/student/password">修改密码</el-menu-item>
          </el-sub-menu>
        </el-menu>
      </el-aside>

      <el-container>
        <el-header class="dashboard-header">
          <div class="header-content">
            <el-button
              type="text"
              class="toggle-button"
              @click="toggleSidebar"
              aria-label="Toggle menu"
            >
              <el-icon :size="24" style="vertical-align: middle;">
                <component :is="isSidebarCollapsed ? Expand : Fold" />
              </el-icon>
            </el-button>
            <h1 class="header-title">{{ title }}</h1>
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
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  Expand,
  Fold,
  Calendar,
  Notebook,
  User,
  House
} from '@element-plus/icons-vue'

defineProps({
  title: {
    type: String,
    default: '学生首页'
  }
})

const router = useRouter()
const isSidebarCollapsed = ref(true)

const handleLogout = () => {
  router.push('/login')
}

const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
  display: flex;
}

.el-container {
  flex: 1;
}

.el-main {
  flex: 1;
  min-height: calc(100vh - 60px);
  overflow: auto;
  padding: 20px;
}

.attendance-sidebar {
  transition: width 0.3s ease;
}

.dashboard-header {
  background-color: #409eff;
  color: white;
  border-radius: 8px;
  margin-bottom: 20px;
  padding: 0 20px;
}

.header-content {
  display: flex;
  align-items: center;
  height: 100%;
}

.header-title {
  flex: 1;
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  margin: 0;
  font-family: system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, sans-serif;
}

.toggle-button {
  color: #409eff;
  padding: 0;
  margin-right: 16px;
}

.logout-button {
  margin-left: auto;
  margin-right: 16px;
}
</style>
