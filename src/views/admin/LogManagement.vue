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
        <el-menu-item index="1" @click="$router.push('/admin/log')">
          <el-icon><icon-menu /></el-icon>
          <span>日志查询</span>
        </el-menu-item>
        <el-menu-item index="2" @click="$router.push('/admin/log/login')">
          <el-icon><user /></el-icon>
          <span>登录日志</span>
        </el-menu-item>
        <el-menu-item index="3" @click="$router.push('/admin/log/operation')">
          <el-icon><operation /></el-icon>
          <span>操作日志</span>
        </el-menu-item>
        <el-menu-item index="4" @click="$router.push('/admin/log/error')">
          <el-icon><warning /></el-icon>
          <span>错误日志</span>
        </el-menu-item>
        <el-menu-item index="5" @click="$router.push('/admin/log/export')">
          <el-icon><download /></el-icon>
          <span>日志导出</span>
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
          <h1 class="header-title">日志管理系统</h1>
        </div>
      </el-header>
      <el-main>
        <!-- 日志筛选 -->
        <div class="filter-container">
          <el-form :inline="true">
            <el-form-item label="操作类型">
              <el-select v-model="filter.type" placeholder="请选择">
                <el-option label="全部" value=""></el-option>
                <el-option label="登录" value="login"></el-option>
                <el-option label="考勤" value="attendance"></el-option>
                <el-option label="系统" value="system"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="日期范围">
              <el-date-picker
                v-model="dateRange"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
              ></el-date-picker>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSearch">查询</el-button>
            </el-form-item>
          </el-form>
        </div>

        <!-- 日志表格 -->
        <el-table :data="logList" style="width: 100%">
          <el-table-column prop="time" label="时间" width="180"></el-table-column>
          <el-table-column prop="username" label="用户名" width="120"></el-table-column>
          <el-table-column prop="type" label="操作类型" width="120"></el-table-column>
          <el-table-column prop="description" label="操作描述"></el-table-column>
          <el-table-column prop="ip" label="IP地址" width="150"></el-table-column>
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
import { Menu as IconMenu, Setting, Expand, Fold, User, Operation, Warning, Download } from '@element-plus/icons-vue'
import { ref } from 'vue'

const isSidebarCollapsed = ref(false)
const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

const dateRange = ref([])
const filter = ref({
  type: ''
})
const logList = ref([
  {
    time: '2023-10-01 08:30:12',
    username: 'admin1',
    type: '登录',
    description: '用户登录系统',
    ip: '192.168.1.1'
  },
  {
    time: '2023-10-01 09:15:45',
    username: 'teacher1',
    type: '考勤',
    description: '提交考勤记录',
    ip: '192.168.1.2'
  },
  {
    time: '2023-10-01 10:00:23',
    username: 'admin1',
    type: '系统',
    description: '修改系统设置',
    ip: '192.168.1.1'
  }
])
const total = ref(100)
const pageSize = ref(10)

const handleSearch = () => {
  console.log('查询日志', filter.value)
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
