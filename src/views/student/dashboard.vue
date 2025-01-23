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
      >
        <el-sub-menu index="1">
          <template #title>
            <el-icon><calendar /></el-icon>
            <span>考勤管理</span>
          </template>
          <el-menu-item index="1-1" route="/student/attendance">考勤记录</el-menu-item>
          <el-menu-item index="1-2" route="/student/attendance/statistics">考勤统计</el-menu-item>
          <el-menu-item index="1-3" route="/student/attendance/apply">考勤申诉</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="2">
          <template #title>
            <el-icon><notebook /></el-icon>
            <span>课程信息</span>
          </template>
          <el-menu-item index="2-1" route="/student/course/schedule">课程表</el-menu-item>
          <el-menu-item index="2-2" route="/student/course/materials">课程资料</el-menu-item>
          <el-menu-item index="2-3" route="/student/course/assignments">作业提交</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="4">
          <template #title>
            <el-icon><user /></el-icon>
            <span>个人中心</span>
          </template>
          <el-menu-item index="4-1" route="/student/profile">个人信息</el-menu-item>
          <el-menu-item index="4-2" route="/student/password">修改密码</el-menu-item>
          <el-menu-item index="4-3" route="/student/notification">消息通知</el-menu-item>
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
          <h1 class="header-title">学生首页</h1>
        </div>
      </el-header>
      <el-main>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card class="stat-card" shadow="hover">
              <h3>出勤率</h3>
              <el-progress
                :percentage="attendanceRate"
                :color="attendanceRateColor"
                :stroke-width="16"
              />
              <p class="stat-description">当前出勤率为 {{ attendanceRate }}%</p>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card class="stat-card" shadow="hover">
              <h3>签到次数</h3>
              <p class="stat-value">{{ checkInCount }} 次</p>
              <p class="stat-description">本学期累计签到次数</p>
            </el-card>
          </el-col>
        </el-row>
        <el-card class="attendance-table" shadow="hover">
          <h2>最近考勤记录</h2>
          <el-table :data="recentAttendance" stripe style="width: 100%">
            <el-table-column prop="date" label="日期" width="180" />
            <el-table-column prop="course" label="课程" width="180" />
            <el-table-column prop="status" label="状态">
              <template #default="{ row }">
                <el-tag :type="getStatusTagType(row.status)">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Expand, Fold } from '@element-plus/icons-vue'
import { Calendar, Notebook, User } from '@element-plus/icons-vue'

const isSidebarCollapsed = ref(false)
const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

const attendanceRate = ref(85)
const checkInCount = ref(12)
const recentAttendance = ref([
  { date: '2023-10-01', course: '数学', status: '正常' },
  { date: '2023-10-02', course: '英语', status: '迟到' },
  { date: '2023-10-03', course: '物理', status: '缺勤' },
  { date: '2023-10-04', course: '化学', status: '正常' },
])

const attendanceRateColor = computed(() => {
  if (attendanceRate.value >= 90) return '#67c23a' // 绿色
  if (attendanceRate.value >= 70) return '#e6a23c' // 橙色
  return '#f56c6c' // 红色
})

const getStatusTagType = (status) => {
  switch (status) {
    case '正常':
      return 'success'
    case '迟到':
      return 'warning'
    case '缺勤':
      return 'danger'
    default:
      return 'info'
  }
}
</script>

<style scoped>
.attendance-sidebar {
  transition: width 0.3s ease;
}

.dashboard-container {
  padding: 20px;
  background-color: #f5f7fa;
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
}

.toggle-button {
  color: #409eff;
  padding: 0;
  margin-right: 16px;
}

.stat-card {
  text-align: center;
  border-radius: 8px;
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #409eff;
  margin: 10px 0;
}

.stat-description {
  color: #909399;
  font-size: 14px;
}

.attendance-table {
  margin-top: 20px;
  border-radius: 8px;
}

.el-progress {
  margin: 20px 0;
}

.el-tag {
  font-size: 14px;
}
</style>
