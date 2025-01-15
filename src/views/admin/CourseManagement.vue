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
        <el-menu-item index="1" @click="$router.push('/admin/course')">
          <el-icon><icon-menu /></el-icon>
          <span>课程列表</span>
        </el-menu-item>
        <el-menu-item index="2" @click="$router.push('/admin/course/add')">
          <el-icon><plus /></el-icon>
          <span>添加课程</span>
        </el-menu-item>
        <el-menu-item index="3" @click="$router.push('/admin/course/category')">
          <el-icon><folder /></el-icon>
          <span>课程分类</span>
        </el-menu-item>
        <el-menu-item index="4" @click="$router.push('/admin/course/teacher')">
          <el-icon><avatar /></el-icon>
          <span>教师分配</span>
        </el-menu-item>
        <el-menu-item index="5" @click="$router.push('/admin/course/material')">
          <el-icon><document /></el-icon>
          <span>课程资料</span>
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
          <h1 class="header-title">课程管理系统</h1>
        </div>
      </el-header>
      <el-main>
        <!-- 搜索和操作区域 -->
        <div class="filter-container">
          <el-form :inline="true">
            <el-form-item>
              <el-input v-model="searchQuery" placeholder="搜索课程名称或代码"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSearch">查询</el-button>
            </el-form-item>
            <el-form-item>
              <el-button type="success" @click="addCourse">添加课程</el-button>
            </el-form-item>
          </el-form>
        </div>

        <!-- 课程表格 -->
        <el-table :data="courses" style="width: 100%">
          <el-table-column prop="id" label="ID" width="80"></el-table-column>
          <el-table-column prop="name" label="课程名称"></el-table-column>
          <el-table-column prop="code" label="课程代码"></el-table-column>
          <el-table-column prop="credit" label="学分"></el-table-column>
          <el-table-column prop="teacher" label="授课教师"></el-table-column>
          <el-table-column prop="time" label="上课时间"></el-table-column>
          <el-table-column label="操作" width="150">
            <template #default="scope">
              <el-button type="text" size="small" @click="editCourse(scope.row)">编辑</el-button>
              <el-button type="text" size="small" @click="deleteCourse(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <el-pagination
          background
          layout="prev, pager, next"
          :total="total"
          :page-size="pageSize"
          @current-change="handlePageChange"
        ></el-pagination>

        <!-- 课程编辑对话框 -->
        <el-dialog :title="dialogTitle" v-model="dialogVisible">
          <el-form :model="currentCourse">
            <el-form-item label="课程名称">
              <el-input v-model="currentCourse.name"></el-input>
            </el-form-item>
            <el-form-item label="课程代码">
              <el-input v-model="currentCourse.code"></el-input>
            </el-form-item>
            <el-form-item label="学分">
              <el-input-number v-model="currentCourse.credit" :min="1" :max="10"></el-input-number>
            </el-form-item>
            <el-form-item label="授课教师">
              <el-select v-model="currentCourse.teacher" placeholder="请选择">
                <el-option label="张三" value="张三"></el-option>
                <el-option label="李四" value="李四"></el-option>
                <el-option label="王五" value="王五"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="上课时间">
              <el-time-picker
                v-model="currentCourse.time"
                format="HH:mm"
                value-format="HH:mm"
                placeholder="选择时间"
              ></el-time-picker>
            </el-form-item>
          </el-form>
          <template #footer>
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="confirmCourse">确定</el-button>
          </template>
        </el-dialog>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { Menu as IconMenu, Setting, Expand, Fold, Plus, Folder, Avatar, Document } from '@element-plus/icons-vue'
import { ref } from 'vue'
import { ElMessageBox } from 'element-plus'

const isSidebarCollapsed = ref(false)
const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

const searchQuery = ref('')
const courses = ref([
  {
    id: 1,
    name: '数据结构',
    code: 'CS101',
    credit: 3,
    teacher: '张三',
    time: '08:00'
  },
  {
    id: 2,
    name: '操作系统',
    code: 'CS102',
    credit: 4,
    teacher: '李四',
    time: '10:00'
  },
  {
    id: 3,
    name: '计算机网络',
    code: 'CS103',
    credit: 3,
    teacher: '王五',
    time: '14:00'
  }
])
const total = ref(100)
const pageSize = ref(10)
const dialogVisible = ref(false)
const dialogTitle = ref('添加课程')
const currentCourse = ref({
  id: null,
  name: '',
  code: '',
  credit: 1,
  teacher: '',
  time: ''
})

const handleSearch = () => {
  console.log('搜索课程', searchQuery.value)
}

const addCourse = () => {
  currentCourse.value = {
    id: null,
    name: '',
    code: '',
    credit: 1,
    teacher: '',
    time: ''
  }
  dialogTitle.value = '添加课程'
  dialogVisible.value = true
}

const editCourse = (course) => {
  currentCourse.value = { ...course }
  dialogTitle.value = '编辑课程'
  dialogVisible.value = true
}

const deleteCourse = (course) => {
  ElMessageBox.confirm('确定删除该课程吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    courses.value = courses.value.filter(c => c.id !== course.id)
  })
}

const confirmCourse = () => {
  if (currentCourse.value.id) {
    // 编辑课程
    const index = courses.value.findIndex(c => c.id === currentCourse.value.id)
    courses.value.splice(index, 1, currentCourse.value)
  } else {
    // 添加课程
    currentCourse.value.id = courses.value.length + 1
    courses.value.push(currentCourse.value)
  }
  dialogVisible.value = false
}

const handlePageChange = (page) => {
  console.log('切换页码', page)
}
</script>

<style scoped>
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
}

.toggle-button {
  color: white;
  padding: 0;
  margin-right: 16px;
}

.filter-container {
  margin-bottom: 20px;
}
</style>
