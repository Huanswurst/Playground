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
          <el-col :span="isMobile ? 24 : 8">
            <el-card class="stat-card" shadow="hover" @click.native="handleCardClick('attendance')">
              <h3>平均考勤率</h3>
              <p class="stat-value">{{ attendanceRate }}%</p>
              <p class="stat-description">本学期课程平均考勤率</p>
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
            @row-click="(row) => console.log('表格行数据:', row)"
          >
            <el-table-column prop="course_code" label="课程代码" width="120" sortable />
            <el-table-column prop="course_name" label="课程名称" width="180" sortable>
              <template #default="{row}">
                {{ row?.course_name || '-' }}
              </template>
            </el-table-column>
            <el-table-column prop="academic_year" label="学年" width="100" sortable />
            <el-table-column prop="semester" label="学期" width="100" sortable />
            <el-table-column label="操作">
              <template #default="{ row }">
                <el-button type="primary" size="small" @click="handleAddCourse(row)">编辑</el-button>
                <el-button type="primary" size="small" @click="handleViewStudents(row)">学生</el-button>
                <el-button type="primary" size="small" @click="handleViewAttendance(row)">考勤</el-button>
                <el-button type="danger" size="small" @click="handleDeleteCourse(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>

        <!-- 添加/编辑课程对话框 -->
        <el-dialog
          v-model="courseDialogVisible"
          :title="selectedCourse ? '编辑课程' : '新建课程'"
          width="50%"
        >
          <el-form :model="courseForm" label-width="120px">
            <el-form-item label="课程代码" required>
              <el-input v-model="courseForm.courseCode" placeholder="请输入课程代码" />
            </el-form-item>
            <el-form-item label="课程名称" required>
              <el-input v-model="courseForm.courseName" placeholder="请输入课程名称" />
            </el-form-item>
            <el-form-item label="学年" required>
              <el-date-picker
                v-model="courseForm.academicYear"
                type="year"
                value-format="YYYY"
                placeholder="选择学年"
              />
            </el-form-item>
            <el-form-item label="学期" required>
              <el-select v-model="courseForm.semester" placeholder="请选择学期">
                <el-option label="春季" value="spring" />
                <el-option label="秋季" value="fall" />
              </el-select>
            </el-form-item>
            <el-form-item label="课程描述">
              <el-input
                v-model="courseForm.description"
                type="textarea"
                :rows="3"
                placeholder="请输入课程描述"
              />
            </el-form-item>
          </el-form>
          <template #footer>
            <el-button @click="courseDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="handleSaveCourse">保存</el-button>
          </template>
        </el-dialog>

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
import { ElMessageBox, ElMessage } from 'element-plus'
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { apiBaseUrl } from '../../config';
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
const courseCount = ref(0)
const studentCount = ref(0)
const attendanceRate = ref(0)
const courses = ref([])
const loading = ref(false)

// 过滤参数
const filterParams = ref({
  courseName: '',
  baseYear: '',
  targetYear: '',
  semester: '',
  isRecurring: false,
  showAll: false
})

// 对话框相关状态
const studentDialogVisible = ref(false)
const courseDialogVisible = ref(false)
const selectedCourse = ref(null)
const courseForm = ref({
  courseCode: '',
  courseName: '',
  academicYear: '',
  semester: 'spring',
  description: ''
})

// 计算属性
const filteredCourses = computed(() => {
  console.log('原始课程数据:', courses.value)
  console.log('过滤参数:', filterParams.value)
  
  // 简化过滤逻辑，先确保所有数据都能显示
  const result = courses.value.filter(item => {
    if (!item || typeof item !== 'object') return false
    
    // 仅保留课程名称过滤作为基本过滤条件
    const name = item.courseName || ''
    const nameQuery = filterParams.value.courseName || ''
    if (nameQuery && !name.toLowerCase().includes(nameQuery.toLowerCase())) {
      return false
    }
    
    return true
  })
  
  console.log('过滤后的课程数据:', result)
  return result
})

// 获取课程列表
const fetchCourses = async () => {
  try {
    loading.value = true
    const token = localStorage.getItem('authToken')
    if (!token) {
      throw new Error('请先登录')
    }

    const response = await axios.get(`${apiBaseUrl}/api/teacher/courses`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    console.log('API响应数据:', response.data)
    if (response.data && Array.isArray(response.data)) {
      // 确保数据包含所有必要字段
      courses.value = response.data.map(item => ({
        ...item,
        studentCount: item.studentCount || 0,
        teacherName: item.teacherName || '未知教师'
      }))
      console.log('处理后的课程数据:', courses.value)
      courseCount.value = courses.value.length
      studentCount.value = courses.value.reduce((sum, course) => sum + course.studentCount, 0)
      // 计算平均考勤率
      const totalAttendance = courses.value.reduce((sum, course) => sum + (course.attendanceRate || 0), 0)
      attendanceRate.value = courses.value.length > 0 ? Math.round(totalAttendance / courses.value.length) : 0
    } else {
      throw new Error('API返回数据格式不正确')
    }
  } catch (error) {
    console.error('获取课程列表失败:', error)
    if (error.response?.status === 401) {
      localStorage.clear()
      ElMessage.error('登录已过期，请重新登录')
      await router.push('/login')
    } else {
      ElMessage.error(error.response?.data?.detail || error.message || '获取课程列表失败')
    }
    courses.value = []
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

const handleSearch = async () => {
  try {
    loading.value = true
    const params = new URLSearchParams()
    if (filterParams.value.courseName) params.append('courseName', filterParams.value.courseName)
    if (filterParams.value.baseYear) params.append('baseYear', filterParams.value.baseYear)
    if (filterParams.value.targetYear) params.append('targetYear', filterParams.value.targetYear)
    if (filterParams.value.semester) params.append('semester', filterParams.value.semester)
    params.append('isRecurring', filterParams.value.isRecurring)
    params.append('showAll', filterParams.value.showAll)
    
    const token = localStorage.getItem('authToken')
    if (!token) {
      throw new Error('请先登录')
    }

    const response = await fetch(`${apiBaseUrl}/api/teacher/courses`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || '搜索课程失败')
    }

    const data = await response.json()
    if (data && Array.isArray(data)) {
      courses.value = data
      courseCount.value = courses.value.length
      studentCount.value = courses.value.reduce((sum, course) => sum + (course.studentCount || 0), 0)
    } else {
      throw new Error('API返回数据格式不正确')
    }
  } catch (error) {
    console.error('搜索课程失败:', error)
    ElMessage.error(error.message || '搜索课程失败')
  } finally {
    loading.value = false
  }
}

const resetFilters = () => {
  filterParams.value = {
    courseName: '',
    baseYear: '',
    targetYear: '',
    semester: '',
    isRecurring: false,
    showAll: false
  }
}

const handleAddCourse = (course = null) => {
  // 明确设置selectedCourse状态
  selectedCourse.value = course
  
  // 统一表单初始化逻辑
  courseForm.value = {
    courseCode: course?.courseCode || '',
    courseName: course?.courseName || '',
    academicYear: course?.academicYear || '',
    semester: course?.semester || 'spring',
    description: course?.description || ''
  }
  
  courseDialogVisible.value = true
}

const handleDeleteCourse = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除课程"${row.courseName}"吗? 此操作不可恢复。`,
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await axios.delete(`/api/teacher/courses/${row.id}/`)
    await fetchCourses()
    ElMessage.success('删除成功')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除课程失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

const handleViewAttendance = (row) => {
  router.push({ name: 'CourseAttendance', params: { courseId: row.id } })
}

const handleSaveCourse = async () => {
  try {
    const token = localStorage.getItem('authToken')
    if (!token) {
      throw new Error('请先登录')
    }

    // 更严格的编辑模式判断
    const isEditMode = selectedCourse.value !== null
      && selectedCourse.value !== undefined
      && selectedCourse.value.id
      && typeof selectedCourse.value.id === 'number'
    
    if (isEditMode) {
      // 编辑现有课程
      await axios.put(`${apiBaseUrl}/api/teacher/courses/${selectedCourse.value.id}/`, courseForm.value, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      ElMessage.success('课程更新成功')
    } else {
      // 创建新课程
      await axios.post(`${apiBaseUrl}/api/teacher/courses/`, courseForm.value, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      ElMessage.success('课程创建成功')
    }
    
    // 重置状态
    courseDialogVisible.value = false
    selectedCourse.value = null
    await fetchCourses()
  } catch (error) {
    console.error('保存课程失败:', error)
    if (error.response?.status === 401) {
      localStorage.clear()
      ElMessage.error('登录已过期，请重新登录')
      await router.push('/login')
    } else {
      ElMessage.error(error.response?.data?.detail || error.message || '保存课程失败')
    }
  }
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

/* 表格样式修复 */
.el-table {
  width: 100%;
}
.el-table__header-wrapper,
.el-table__body-wrapper {
  width: 100% !important;
}
.el-table__cell {
  padding: 8px 0;
}
.el-table th.el-table__cell {
  background-color: #f5f7fa;
}
.el-table .cell {
  padding: 0 8px;
  white-space: nowrap;
}

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
