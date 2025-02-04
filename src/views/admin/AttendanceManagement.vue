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
        <el-menu-item index="1" route="/admin/attendance">
          <el-icon><icon-menu /></el-icon>
          <span>考勤记录</span>
        </el-menu-item>
        <el-menu-item index="2" route="/admin/statistics">
          <el-icon><document /></el-icon>
          <span>考勤报表</span>
        </el-menu-item>
        <el-menu-item index="3" route="/admin/permission">
          <el-icon><setting /></el-icon>
          <span>考勤设置</span>
        </el-menu-item>
        <el-menu-item index="4" route="/admin/log">
          <el-icon><warning /></el-icon>
          <span>异常处理</span>
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
        <el-table :data="attendanceList" style="width: 100%" v-loading="loading">
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
import { Menu as IconMenu, Setting, Expand, Fold, Document, Warning } from '@element-plus/icons-vue'
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import config from '@/config'

const isSidebarCollapsed = ref(false)
const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

const dateRange = ref([])
const filter = ref({
  userType: ''
})
const attendanceList = ref([])
const total = ref(0)
const pageSize = ref(10)
const currentPage = ref(1)
const loading = ref(false)
const error = ref(null)

const fetchAttendance = async () => {
  loading.value = true
  error.value = null
  try {
    const token = localStorage.getItem('token')
    const params = new URLSearchParams({
      start_date: dateRange.value[0]?.toISOString().split('T')[0] || '',
      end_date: dateRange.value[1]?.toISOString().split('T')[0] || '',
      user_type: filter.value.userType,
      page: currentPage.value,
      page_size: pageSize.value
    })
    
    const response = await fetch(`${config.apiBaseUrl}${config.apiEndpoints.admin.attendance}?${params.toString()}`, {
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json'
      }
    })
    
    if (!response.ok) {
      throw new Error('获取考勤数据失败')
    }
    
    const data = await response.json()
    attendanceList.value = data.results
    total.value = data.count
  } catch (err) {
    error.value = err.message
    ElMessage.error('获取考勤数据失败：' + err.message)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchAttendance()
}

const handleEdit = async (record) => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`${config.apiBaseUrl}${config.apiEndpoints.admin.attendance}${record.id}/`, {
      method: 'PUT',
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(record)
    })
    
    if (!response.ok) {
      throw new Error('更新考勤记录失败')
    }
    
    ElMessage.success('考勤记录更新成功')
    fetchAttendance()
  } catch (err) {
    ElMessage.error('更新考勤记录失败：' + err.message)
  }
}

const handleDelete = async (record) => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`${config.apiBaseUrl}${config.apiEndpoints.admin.attendance}${record.id}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Token ${token}`
      }
    })
    
    if (!response.ok) {
      throw new Error('删除考勤记录失败')
    }
    
    ElMessage.success('考勤记录删除成功')
    fetchAttendance()
  } catch (err) {
    ElMessage.error('删除考勤记录失败：' + err.message)
  }
}

const handlePageChange = (page) => {
  currentPage.value = page
  fetchAttendance()
}

// 初始化时获取数据
onMounted(() => {
  fetchAttendance()
})
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
