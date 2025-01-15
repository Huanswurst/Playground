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
            <el-icon :size="24">
              <component :is="isSidebarCollapsed ? 'Expand' : 'Fold'" />
            </el-icon>
          </el-button>
          <h1 class="header-title">教师首页</h1>
        </div>
      </el-header>
      <el-main>
        <!-- 统计卡片 -->
        <el-row :gutter="isMobile ? 10 : 20">
          <el-col :span="isMobile ? 24 : 8">
            <el-card class="stat-card" shadow="hover" @click.native="handleCardClick('course')">
              <h3>课程总数</h3>
              <p class="stat-value">{{ courseCount }} 门</p>
              <p class="stat-description">本学期开设的课程数量</p>
            </el-card>
          </el-col>
          <el-col :span="isMobile ? 24 : 8">
            <el-card class="stat-card" shadow="hover" @click.native="handleCardClick('student')">
              <h3>学生总数</h3>
              <p class="stat-value">{{ studentCount }} 人</p>
              <p class="stat-description">本学期授课学生总数</p>
            </el-card>
          </el-col>
        </el-row>

        <!-- 近期授课考勤情况表格 -->
        <el-card class="attendance-table" shadow="hover">
          <h2>近期授课考勤情况</h2>

          <!-- 搜索和操作按钮 -->
          <div class="table-actions">
            <el-input
              v-model="searchQuery"
              placeholder="搜索课程或班级"
              clearable
              style="width: 200px; margin-right: 10px;"
              @clear="handleSearch"
              @input="handleSearch"
            />
            <el-button type="primary" @click="handleImport">导入数据</el-button>
            <el-button type="success" @click="handleExport">导出数据</el-button>
          </div>

          <!-- 表格 -->
          <el-table
            :data="filteredAttendance"
            stripe
            style="width: 100%"
            :default-sort="{ prop: 'date', order: 'descending' }"
          >
            <el-table-column prop="date" label="日期" sortable />
            <el-table-column prop="course" label="课程" sortable />
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

const isSidebarCollapsed = ref(false)
const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

const courseCount = ref(5)
const studentCount = ref(120)
const isMobile = ref(false)
const searchQuery = ref('')
const recentAttendance = ref([
  {
    date: '2023-10-01',
    course: '数学',
    class: '高一（1）班',
    attendanceRate: 95,
    absentCount: 2,
    lateCount: 1,
  },
  {
    date: '2023-10-02',
    course: '英语',
    class: '高一（2）班',
    attendanceRate: 90,
    absentCount: 3,
    lateCount: 2,
  },
  {
    date: '2023-10-03',
    course: '物理',
    class: '高二（1）班',
    attendanceRate: 85,
    absentCount: 5,
    lateCount: 3,
  },
  {
    date: '2023-10-04',
    course: '化学',
    class: '高二（2）班',
    attendanceRate: 98,
    absentCount: 1,
    lateCount: 0,
  },
])

// 计算属性
const filteredAttendance = computed(() => {
  return recentAttendance.value.filter(
    (item) =>
      item.course.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      item.class.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// 方法
const checkDevice = () => {
  isMobile.value = window.innerWidth <= 768
}

const handleCardClick = (type) => {
  if (type === 'course') {
    console.log('点击了课程总数卡片')
  } else if (type === 'student') {
    console.log('点击了学生总数卡片')
  }
}

const getProgressColor = (attendanceRate) => {
  if (attendanceRate >= 90) return '#67c23a' // 绿色
  if (attendanceRate >= 70) return '#e6a23c' // 橙色
  return '#f56c6c' // 红色
}

const handleSearch = () => {
  // 搜索逻辑已在 computed 中实现
}

const handleImport = () => {
  console.log('导入数据功能待实现')
}

const handleExport = async () => {
  console.log('导出数据成功')
  const data = filteredAttendance.value
  const headers = ['日期', '课程', '班级', '出勤率', '缺勤人数', '迟到人数']
  const rows = data.map((item) => [
    item.date,
    item.course,
    item.class,
    `${item.attendanceRate}%`,
    item.absentCount,
    item.lateCount,
  ])
  await exportToExcel(headers, rows, '考勤数据')
}

const exportToExcel = async (headers, rows, fileName) => {
  const xlsx = await import('xlsx')
  const worksheet = xlsx.utils.aoa_to_sheet([headers, ...rows])
  const workbook = xlsx.utils.book_new()
  xlsx.utils.book_append_sheet(workbook, worksheet, 'Sheet1')
  xlsx.writeFile(workbook, `${fileName}.xlsx`)
}

// 生命周期钩子
onMounted(() => {
  checkDevice()
  window.addEventListener('resize', checkDevice)
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
  color: white;
  padding: 0;
  margin-right: 16px;
}

/* 复用 Dashboard 的样式 */
@import './Dashboard.css';
</style>
