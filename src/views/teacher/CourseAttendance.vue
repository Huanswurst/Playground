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
        <el-menu-item index="1">
          <el-icon><icon-menu /></el-icon>
          <span>考勤管理</span>
        </el-menu-item>
        <el-menu-item index="2">
          <el-icon><setting /></el-icon>
          <span>课程管理</span>
        </el-menu-item>
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
          <h1 class="header-title">{{ course.courseName }} 考勤详情</h1>
        </div>
      </el-header>
      <el-main>
          <!-- 统计卡片 -->
          <el-row :gutter="isMobile ? 10 : 20">
            <el-col :span="isMobile ? 24 : 8">
              <el-card class="stat-card" shadow="hover">
                <h3>总考勤率</h3>
                <p class="stat-value">{{ overallAttendanceRate }}%</p>
                <p class="stat-description">本课程的平均考勤率</p>
              </el-card>
            </el-col>
            <el-col :span="isMobile ? 24 : 8">
              <el-card class="stat-card" shadow="hover">
                <h3>缺勤人数</h3>
                <p class="stat-value">{{ totalAbsentCount }} 人</p>
                <p class="stat-description">本课程的缺勤总人数</p>
              </el-card>
            </el-col>
            <el-col :span="isMobile ? 24 : 8">
              <el-card class="stat-card" shadow="hover">
                <h3>迟到人数</h3>
                <p class="stat-value">{{ totalLateCount }} 人</p>
                <p class="stat-description">本课程的迟到总人数</p>
              </el-card>
            </el-col>
          </el-row>

          <!-- 考勤表格 -->
          <el-card class="attendance-table" shadow="hover">
            <h2>考勤记录</h2>

            <!-- 搜索和操作按钮 -->
            <div class="table-actions">
              <el-input
                v-model="searchQuery"
                placeholder="搜索日期或班级"
                clearable
                style="width: 200px; margin-right: 10px;"
                @clear="handleSearch"
                @input="handleSearch"
              />
              <el-button type="primary" @click="handlePublishAttendance">发布考勤</el-button>
            </div>

            <!-- 表格 -->
            <el-table
              :data="filteredAttendance"
              stripe
              style="width: 100%"
              :default-sort="{ prop: 'date', order: 'descending' }"
            >
              <el-table-column prop="date" label="日期" sortable />
              <el-table-column prop="class" label="班级" sortable />
              <el-table-column prop="attendanceRate" label="出勤率" sortable>
                <template #default="{ row }">
                  <el-progress
                    :percentage="row.attendanceRate"
                    :color="getProgressColor(row.attendanceRate)"
                    :stroke-width="12"
                  />
                </template>
              </el-table-column>
              <el-table-column prop="absentCount" label="缺勤人数" sortable />
              <el-table-column prop="lateCount" label="迟到人数" sortable />
            </el-table>
          </el-card>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { Menu as IconMenu, Setting, Expand, Fold } from '@element-plus/icons-vue'
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'

const isSidebarCollapsed = ref(false)
const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

const isMobile = ref(false)
const searchQuery = ref('')
const course = ref({
  id: 1,
  courseName: '数学',
  teacherName: '张老师',
  studentCount: 50,
})
const attendanceData = ref([
  {
    date: '2023-10-01',
    class: '高一（1）班',
    attendanceRate: 95,
    absentCount: 2,
    lateCount: 1,
  },
  {
    date: '2023-10-02',
    class: '高一（2）班',
    attendanceRate: 90,
    absentCount: 3,
    lateCount: 2,
  },
  {
    date: '2023-10-03',
    class: '高二（1）班',
    attendanceRate: 85,
    absentCount: 5,
    lateCount: 3,
  },
])

// 计算属性
const overallAttendanceRate = computed(() => {
  const total = attendanceData.value.reduce((sum, item) => sum + item.attendanceRate, 0)
  return (total / attendanceData.value.length).toFixed(2)
})

const totalAbsentCount = computed(() => {
  return attendanceData.value.reduce((sum, item) => sum + item.absentCount, 0)
})

const totalLateCount = computed(() => {
  return attendanceData.value.reduce((sum, item) => sum + item.lateCount, 0)
})

const filteredAttendance = computed(() => {
  return attendanceData.value.filter(
    (item) =>
      item.date.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      item.class.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// 方法
const checkDevice = () => {
  isMobile.value = window.innerWidth <= 768
}

const fetchCourseData = async (courseId) => {
  try {
    console.log('课程数据加载成功')
  } catch (error) {
    console.error('课程数据加载失败')
  }
}

const handleSearch = () => {
  // 搜索逻辑已在 computed 中实现
}

const handlePublishAttendance = () => {
  console.log('考勤发布成功')
}

const getProgressColor = (attendanceRate) => {
  if (attendanceRate >= 90) return '#67c23a' // 绿色
  if (attendanceRate >= 70) return '#e6a23c' // 橙色
  return '#f56c6c' // 红色
}

// 生命周期钩子
onMounted(() => {
  checkDevice()
  window.addEventListener('resize', checkDevice)
  const courseId = useRoute().params.courseId
  fetchCourseData(courseId)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', checkDevice)
})
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

/* 复用 Dashboard 的样式 */
@import './Dashboard.css';
</style>
