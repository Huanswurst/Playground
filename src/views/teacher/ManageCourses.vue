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
          <h1 class="header-title">课程管理</h1>
          <el-button
            type="danger"
            class="logout-button"
            @click="handleLogout"
          >
            退出登录
          </el-button>
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

        <!-- 课程管理表格 -->
        <el-card class="course-table" shadow="hover">
          <h2>课程列表</h2>

          <!-- 搜索和操作按钮 -->
          <div class="table-actions">
            <el-form :inline="true" :model="filterParams" class="filter-form">
              <el-form-item label="课程名称">
                <el-input
                  v-model="filterParams.courseName"
                  placeholder="输入课程名称"
                  clearable
                  style="width: 120px"
                />
              </el-form-item>
              
              <el-form-item label="基础学年">
                <el-date-picker
                  v-model="filterParams.baseYear"
                  type="year"
                  value-format="YYYY"
                  placeholder="选择基础学年"
                  style="width: 120px"
                />
              </el-form-item>

              <el-form-item label="目标学年">
                <el-date-picker
                  v-model="filterParams.targetYear"
                  type="year"
                  value-format="YYYY"
                  placeholder="选择目标学年"
                  style="width: 120px"
                />
              </el-form-item>

              <el-form-item label="学期">
                <el-select
                  v-model="filterParams.semester"
                  placeholder="选择学期"
                  clearable
                  style="width: 100px"
                >
                  <el-option label="春季" value="spring" />
                  <el-option label="秋季" value="fall" />
                </el-select>
              </el-form-item>

              <el-form-item label=" ">
                <el-checkbox v-model="filterParams.isRecurring">重复课程</el-checkbox>
                <el-checkbox v-model="filterParams.showAll">显示历史</el-checkbox>
              </el-form-item>
            </el-form>

            <div class="action-buttons">
              <el-button type="primary" @click="handleSearch">搜索</el-button>
              <el-button @click="resetFilters">重置</el-button>
              <el-button type="primary" @click="handleAddCourse">新建课程</el-button>
            </div>
          </div>

          <!-- 表格 -->
          <el-table
            :data="filteredCourses"
            stripe
            style="width: 100%"
            :default-sort="{ prop: 'courseName', order: 'ascending' }"
            v-loading="loading"
          >
            <el-table-column prop="courseCode" label="课程代码" width="120" sortable />
            <el-table-column prop="courseName" label="课程名称" width="180" sortable>
              <template #default="{row}">
                {{ row?.courseName || '-' }}
              </template>
            </el-table-column>
            <el-table-column prop="academicYear" label="学年" width="100" sortable />
            <el-table-column prop="semester" label="学期" width="100" sortable />
            <el-table-column label="授课教师" width="140" sortable>
              <template #default="{row}">
                <el-tag v-if="row.teacherName === userStore.user.name" type="success">{{ row.teacherName }}</el-tag>
                <span v-else>{{ row.teacherName }}</span>
              </template>
            </el-table-column>
            <el-table-column label="学生人数" width="120" sortable>
              <template #default="{row}">
                <el-statistic :value="row.studentCount || 0">
                  <template #suffix>人</template>
                </el-statistic>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200">
              <template #default="{ row }">
                <el-button type="primary" @click="handleViewStudents(row)">管理学生</el-button>
                <el-button type="primary" @click="handleViewAttendance(row)">查看考勤</el-button>
                <el-button type="danger" @click="handleDeleteCourse(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>

        <!-- 学生管理对话框 -->
        <el-dialog
          v-model="studentDialogVisible"
          :title="selectedCourse ? `${selectedCourse.courseName} - 学生管理` : '学生管理'"
          width="60%"
        >
          <StudentManagement
            v-if="studentDialogVisible"
            :course="selectedCourse"
            @close="studentDialogVisible = false"
          />
        </el-dialog>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { Menu as IconMenu, Setting, Expand, Fold } from '@element-plus/icons-vue'
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import StudentManagement from './StudentManagement.vue'

const isSidebarCollapsed = ref(true)
const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

const handleLogout = () => {
  router.push('/login')
}

const router = useRouter()
const isMobile = ref(false)
const searchQuery = ref('')
const courseCount = ref(0)
const studentCount = ref(0)
const courses = ref([])
const loading = ref(false)

// 学生管理相关状态
const studentDialogVisible = ref(false)
const selectedCourse = ref(null)

// 计算属性
const filteredCourses = computed(() => {
  return courses.value.filter((item) =>
    item.courseName.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// 获取课程列表
const fetchCourses = async () => {
  try {
    loading.value = true
    const response = await axios.get('/api/teacher_courses/')
    courses.value = response.data
    courseCount.value = courses.value.length
    studentCount.value = courses.value.reduce((sum, course) => sum + course.studentCount, 0)
  } catch (error) {
    console.error('获取课程列表失败:', error)
  } finally {
    loading.value = false
  }
}

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

const handleSearch = () => {
  // 搜索逻辑已在 computed 中实现
}

const handleAddCourse = () => {
  console.log('添加课程功能待实现')
}

const handleDeleteCourse = async (row) => {
  try {
    await axios.delete(`/api/courses/${row.id}/`)
    await fetchCourses()
  } catch (error) {
    console.error('删除课程失败:', error)
  }
}

const handleViewAttendance = (row) => {
  router.push({ name: 'CourseAttendance', params: { courseId: row.id } })
}

const handleViewStudents = (row) => {
  selectedCourse.value = row
  studentDialogVisible.value = true
}

// 生命周期钩子
onMounted(() => {
  checkDevice()
  window.addEventListener('resize', checkDevice)
  fetchCourses()
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', checkDevice)
})
</script>

<style scoped>
/* 复用 Dashboard 的样式 */
@import './Dashboard.css';

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
</style>
