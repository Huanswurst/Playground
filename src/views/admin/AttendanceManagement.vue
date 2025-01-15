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
          <span>用户管理</span>
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
          <h1 class="header-title">考勤管理系统</h1>
        </div>
      </el-header>
      <el-main>
        <!-- 考勤记录筛选 -->
        <div class="filter-container">
          <el-form :inline="true">
            <el-form-item label="日期范围">
              <el-date-picker
                v-model="dateRange"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
              ></el-date-picker>
            </el-form-item>
            <el-form-item label="用户类型">
              <el-select v-model="filter.userType" placeholder="请选择">
                <el-option label="全部" value=""></el-option>
                <el-option label="教师" value="teacher"></el-option>
                <el-option label="学生" value="student"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSearch">查询</el-button>
            </el-form-item>
          </el-form>
        </div>

        <!-- 考勤记录表格 -->
        <el-table :data="attendanceList" style="width: 100%">
          <el-table-column prop="username" label="用户名"></el-table-column>
          <el-table-column prop="role" label="角色"></el-table-column>
          <el-table-column prop="date" label="日期"></el-table-column>
          <el-table-column prop="status" label="状态"></el-table-column>
          <el-table-column label="操作">
            <template #default="scope">
              <el-button type="primary" size="small" @click="handleEdit(scope.row)">编辑</el-button>
              <el-button type="danger" size="small" @click="handleDelete(scope.row)">删除</el-button>
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
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { Menu as IconMenu, Setting, Expand, Fold } from '@element-plus/icons-vue'
import { ref } from 'vue'

const isSidebarCollapsed = ref(false)
const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

const dateRange = ref([])
const filter = ref({
  userType: ''
})
const attendanceList = ref([
  {
    username: 'student1',
    role: '学生',
    date: '2023-10-01',
    status: '正常'
  },
  {
    username: 'teacher1',
    role: '教师',
    date: '2023-10-01',
    status: '迟到'
  }
])
const total = ref(100)
const pageSize = ref(10)

const handleSearch = () => {
  console.log('查询考勤记录', filter.value)
}

const handleEdit = (record) => {
  console.log('编辑考勤记录', record)
}

const handleDelete = (record) => {
  console.log('删除考勤记录', record)
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
