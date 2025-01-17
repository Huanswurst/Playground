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
          <h1 class="header-title">课程管理</h1>
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
            <el-input
              v-model="searchQuery"
              placeholder="搜索课程名称"
              clearable
              style="width: 200px; margin-right: 10px;"
              @clear="handleSearch"
              @input="handleSearch"
            />
            <el-button type="primary" @click="handleAddCourse">添加课程</el-button>
          </div>

          <!-- 表格 -->
          <el-table
            :data="filteredCourses"
            stripe
            style="width: 100%"
            :default-sort="{ prop: 'courseName', order: 'ascending' }"
          >
            <el-table-column prop="courseName" label="课程名称" sortable />
            <el-table-column prop="teacherName" label="授课教师" sortable />
            <el-table-column prop="studentCount" label="学生人数" sortable />
            <el-table-column label="操作" width="200">
              <template #default="{ row }">
                <el-button type="primary" @click="handleViewAttendance(row)">查看考勤</el-button>
                <el-button type="danger" @click="handleDeleteCourse(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { Menu as IconMenu, Setting, Expand, Fold } from '@element-plus/icons-vue'
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'

const isSidebarCollapsed = ref(false)
const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

const router = useRouter()
const isMobile = ref(false)
const searchQuery = ref('')
const courseCount = ref(5)
const studentCount = ref(120)
const courses = ref([
  {
    id: 1,
    courseName: '数学',
    teacherName: '张老师',
    studentCount: 50,
  },
  {
    id: 2,
    courseName: '英语',
    teacherName: '李老师',
    studentCount: 45,
  },
  {
    id: 3,
    courseName: '物理',
    teacherName: '王老师',
    studentCount: 40,
  },
  {
    id: 4,
    courseName: '化学',
    teacherName: '赵老师',
    studentCount: 35,
  },
])

// 计算属性
const filteredCourses = computed(() => {
  return courses.value.filter((item) =>
    item.courseName.toLowerCase().includes(searchQuery.value.toLowerCase())
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

const handleSearch = () => {
  // 搜索逻辑已在 computed 中实现
}

const handleAddCourse = () => {
  console.log('添加课程功能待实现')
}

const handleDeleteCourse = (row) => {
  courses.value = courses.value.filter((course) => course !== row)
  console.log('删除课程成功')
}

const handleViewAttendance = (row) => {
  router.push({ name: 'CourseAttendance', params: { courseId: row.id } })
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
  color: #409eff;
  padding: 0;
  margin-right: 16px;
}

/* 复用 Dashboard 的样式 */
@import './Dashboard.css';
</style>
