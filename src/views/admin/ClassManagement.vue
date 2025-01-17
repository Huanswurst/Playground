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
          <el-menu-item index="1-1" route="/admin/attendance">考勤记录</el-menu-item>
          <el-menu-item index="1-2" route="/admin/attendance/statistics">考勤统计</el-menu-item>
          <el-menu-item index="1-3" route="/admin/attendance/settings">考勤设置</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="2">
          <template #title>
            <el-icon><lock /></el-icon>
            <span>权限管理</span>
          </template>
          <el-menu-item index="2-1" route="/admin/permission/roles">角色管理</el-menu-item>
          <el-menu-item index="2-2" route="/admin/permission/users">用户权限</el-menu-item>
          <el-menu-item index="2-3" route="/admin/permission/audit">权限审计</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="3">
          <template #title>
            <el-icon><document /></el-icon>
            <span>日志管理</span>
          </template>
          <el-menu-item index="3-1" route="/admin/log/login">登录日志</el-menu-item>
          <el-menu-item index="3-2" route="/admin/log/operation">操作日志</el-menu-item>
          <el-menu-item index="3-3" route="/admin/log/error">错误日志</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="4">
          <template #title>
            <el-icon><data-line /></el-icon>
            <span>数据统计</span>
          </template>
          <el-menu-item index="4-1" route="/admin/statistics/attendance">考勤统计</el-menu-item>
          <el-menu-item index="4-2" route="/admin/statistics/course">课程统计</el-menu-item>
          <el-menu-item index="4-3" route="/admin/statistics/user">用户统计</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="5">
          <template #title>
            <el-icon><notebook /></el-icon>
            <span>课程管理</span>
          </template>
          <el-menu-item index="5-1" route="/admin/course/schedule">课程安排</el-menu-item>
          <el-menu-item index="5-2" route="/admin/course/teacher">教师分配</el-menu-item>
          <el-menu-item index="5-3" route="/admin/course/student">学生选课</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="6">
          <template #title>
            <el-icon><school /></el-icon>
            <span>班级管理</span>
          </template>
          <el-menu-item index="6-1" route="/admin/class/student">学生管理</el-menu-item>
          <el-menu-item index="6-2" route="/admin/class/teacher">教师管理</el-menu-item>
          <el-menu-item index="6-3" route="/admin/class/schedule">课表管理</el-menu-item>
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
          <h1 class="header-title">班级管理系统</h1>
        </div>
      </el-header>
      <el-main>
        <!-- 搜索和操作区域 -->
        <div class="filter-container">
          <el-form :inline="true">
            <el-form-item>
              <el-input v-model="searchQuery" placeholder="搜索班级名称"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSearch">查询</el-button>
            </el-form-item>
            <el-form-item>
              <el-button type="success" @click="addClass">添加班级</el-button>
            </el-form-item>
          </el-form>
        </div>

        <!-- 班级表格 -->
        <el-table :data="classes" style="width: 100%">
          <el-table-column prop="id" label="ID" width="80"></el-table-column>
          <el-table-column prop="name" label="班级名称"></el-table-column>
          <el-table-column prop="grade" label="年级"></el-table-column>
          <el-table-column prop="major" label="专业"></el-table-column>
          <el-table-column prop="headTeacher" label="班主任"></el-table-column>
          <el-table-column prop="studentCount" label="学生人数"></el-table-column>
          <el-table-column label="操作" width="150">
            <template #default="scope">
              <el-button type="text" size="small" @click="editClass(scope.row)">编辑</el-button>
              <el-button type="text" size="small" @click="deleteClass(scope.row)">删除</el-button>
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

        <!-- 班级编辑对话框 -->
        <el-dialog :title="dialogTitle" v-model="dialogVisible">
          <el-form :model="currentClass">
            <el-form-item label="班级名称">
              <el-input v-model="currentClass.name"></el-input>
            </el-form-item>
            <el-form-item label="年级">
              <el-select v-model="currentClass.grade" placeholder="请选择">
                <el-option label="2021级" value="2021级"></el-option>
                <el-option label="2022级" value="2022级"></el-option>
                <el-option label="2023级" value="2023级"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="专业">
              <el-select v-model="currentClass.major" placeholder="请选择">
                <el-option label="计算机科学与技术" value="计算机科学与技术"></el-option>
                <el-option label="软件工程" value="软件工程"></el-option>
                <el-option label="网络空间安全" value="网络空间安全"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="班主任">
              <el-select v-model="currentClass.headTeacher" placeholder="请选择">
                <el-option label="张三" value="张三"></el-option>
                <el-option label="李四" value="李四"></el-option>
                <el-option label="王五" value="王五"></el-option>
              </el-select>
            </el-form-item>
          </el-form>
          <template #footer>
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="confirmClass">确定</el-button>
          </template>
        </el-dialog>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { Menu as IconMenu, Setting, Expand, Fold, User, Avatar, Calendar } from '@element-plus/icons-vue'
import { ref } from 'vue'
import { ElMessageBox } from 'element-plus'

const isSidebarCollapsed = ref(false)
const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

const searchQuery = ref('')
const classes = ref([
  {
    id: 1,
    name: '计算机1班',
    grade: '2021级',
    major: '计算机科学与技术',
    headTeacher: '张三',
    studentCount: 45
  },
  {
    id: 2,
    name: '软件工程2班',
    grade: '2022级',
    major: '软件工程',
    headTeacher: '李四',
    studentCount: 50
  },
  {
    id: 3,
    name: '网络安全3班',
    grade: '2023级',
    major: '网络空间安全',
    headTeacher: '王五',
    studentCount: 40
  }
])
const total = ref(100)
const pageSize = ref(10)
const dialogVisible = ref(false)
const dialogTitle = ref('添加班级')
const currentClass = ref({
  id: null,
  name: '',
  grade: '',
  major: '',
  headTeacher: '',
  studentCount: 0
})

const handleSearch = () => {
  console.log('搜索班级', searchQuery.value)
}

const addClass = () => {
  currentClass.value = {
    id: null,
    name: '',
    grade: '',
    major: '',
    headTeacher: '',
    studentCount: 0
  }
  dialogTitle.value = '添加班级'
  dialogVisible.value = true
}

const editClass = (cls) => {
  currentClass.value = { ...cls }
  dialogTitle.value = '编辑班级'
  dialogVisible.value = true
}

const deleteClass = (cls) => {
  ElMessageBox.confirm('确定删除该班级吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    classes.value = classes.value.filter(c => c.id !== cls.id)
  })
}

const confirmClass = () => {
  if (currentClass.value.id) {
    // 编辑班级
    const index = classes.value.findIndex(c => c.id === currentClass.value.id)
    classes.value.splice(index, 1, currentClass.value)
  } else {
    // 添加班级
    currentClass.value.id = classes.value.length + 1
    classes.value.push(currentClass.value)
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
  color: #409eff;
  padding: 0;
  margin-right: 16px;
}

.filter-container {
  margin-bottom: 20px;
}
</style>
