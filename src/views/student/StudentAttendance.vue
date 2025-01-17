<template>
  <el-container class="attendance-container">
    <!-- 侧边栏 -->
    <el-aside
      :class="{ 'attendance-sidebar': true, collapsed: isSidebarCollapsed }"
      :style="{ width: isSidebarCollapsed ? '0' : '200px' }"
    >
      <el-menu v-if="!isSidebarCollapsed">
        <el-menu-item index="1">
          <el-icon><menu /></el-icon>
          <span class="menu-text">首页</span>
        </el-menu-item>
        <el-menu-item index="2">
          <el-icon><document /></el-icon>
          <span class="menu-text">考勤记录</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 主体部分 -->
    <el-container>
      <el-header class="attendance-header">
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
        <h1 class="header-title">我的考勤记录</h1>
      </el-header>

      <!-- 主体内容 -->
      <el-main v-loading="loading">
        <!-- 筛选条件 -->
        <el-form :inline="true" class="filter-form">
          <el-form-item label="日期范围">
            <el-date-picker
              v-model="filterDateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              value-format="yyyy-MM-dd"
            />
          </el-form-item>

          <el-form-item label="课程">
            <el-select v-model="filterCourse" placeholder="选择课程">
              <el-option label="全部" value="" />
              <el-option
                v-for="course in courses"
                :key="course.courseName"
                :label="course.courseName"
                :value="course.courseName"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="状态">
            <el-select v-model="filterStatus" placeholder="选择状态">
              <el-option label="全部" value="" />
              <el-option label="正常" value="正常" />
              <el-option label="迟到" value="迟到" />
              <el-option label="缺勤" value="缺勤" />
            </el-select>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button type="success" @click="handleExport">导出数据</el-button>
            <el-button type="info" @click="handleSwitchCamera">
              <el-icon><switch /></el-icon>
              <span>切换摄像头</span>
            </el-button>
            <el-button type="warning" @click="handleStartRecognition">
              <el-icon><camera /></el-icon>
              <span>开始识别</span>
            </el-button>
          </el-form-item>
        </el-form>

        <!-- 考勤表格 -->
        <el-table
          v-if="pagedAttendance.length > 0"
          :data="pagedAttendance"
          style="width: 100%"
          border
        >
          <el-table-column
            prop="date"
            label="日期"
            sortable
            :formatter="formatDate"
          />
          <el-table-column prop="course" label="课程" sortable />
          <el-table-column prop="status" label="状态" sortable>
            <template #default="scope">
              <el-tag :type="getStatusTagType(scope.row.status)">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="checkInTime" label="签到时间" sortable />
          <el-table-column prop="checkOutTime" label="签退时间" sortable />
        </el-table>

        <!-- 空数据提示 -->
        <div v-else class="no-data" v-if="!loading">
          <p>没有符合条件的考勤记录。</p>
        </div>

        <!-- 分页 -->
        <el-pagination
          class="pagination"
          :current-page="currentPage"
          :page-size="pageSize"
          :total="filteredAttendance.length"
          @current-change="handlePageChange"
          layout="total, prev, pager, next"
          background
          v-if="filteredAttendance.length > pageSize"
        />
      </el-main>
    </el-container>
  </el-container>
</template>
<script>
export default {
  data() {
    return {
      filterDateRange: [], // 筛选日期范围
      filterCourse: '', // 筛选课程
      filterStatus: '', // 筛选状态
      currentPage: 1, // 当前页码
      pageSize: 10, // 每页显示条数
      courses: [], // 动态加载的课程列表
      attendanceData: [], // 全部考勤数据
      loading: false, // 加载状态
      isSidebarCollapsed: true, // 侧边栏状态
      activeMenu: '2', // 当前激活的菜单项
    };
  },
  computed: {
    // 根据筛选条件过滤考勤记录
    filteredAttendance() {
      return this.attendanceData.filter((item) => {
        const [startDate, endDate] = this.filterDateRange;
        const matchDate =
          !startDate ||
          !endDate ||
          (item.date >= startDate && item.date <= endDate);
        const matchCourse = !this.filterCourse || item.course === this.filterCourse;
        const matchStatus = !this.filterStatus || item.status === this.filterStatus;
        return matchDate && matchCourse && matchStatus;
      });
    },
    // 分页后的考勤数据
    pagedAttendance() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = this.currentPage * this.pageSize;
      return this.filteredAttendance.slice(start, end);
    },
  },
  methods: {
    // 格式化日期显示
    formatDate(row, column, cellValue) {
      const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
      return new Date(cellValue).toLocaleDateString(undefined, options);
    },
    // 处理搜索
    handleSearch() {
      this.currentPage = 1; // 重置到第一页
      this.fetchAttendanceData();
    },
    // 处理分页变化
    handlePageChange(page) {
      this.currentPage = page;
    },
    // 根据状态返回标签类型
    getStatusTagType(status) {
      switch (status) {
        case '正常':
          return 'success';
        case '迟到':
          return 'warning';
        case '缺勤':
          return 'danger';
        default:
          return 'info';
      }
    },
    // 导出数据为 Excel
    handleExport() {
      const data = this.filteredAttendance.map((item) => ({
        日期: item.date,
        课程: item.course,
        状态: item.status,
        签到时间: item.checkInTime,
        签退时间: item.checkOutTime,
      }));
      // 添加表头
      const worksheet = XLSX.utils.json_to_sheet(data, { header: ['日期', '课程', '状态', '签到时间', '签退时间'] });
      const workbook = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(workbook, worksheet, '考勤记录');
      // 设置列宽
      const wscols = [
        { wpx: 100 },
        { wpx: 100 },
        { wpx: 80 },
        { wpx: 100 },
        { wpx: 100 },
      ];
      worksheet['!cols'] = wscols;
      const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
      const blob = new Blob([excelBuffer], { type: 'application/octet-stream' });
      saveAs(blob, '考勤记录.xlsx');
    },
    // 获取动态课程列表
    async fetchCourses() {
      try {
        this.loading = true;
        // 模拟 API 请求，请根据实际情况替换
        // const response = await axios.get('/api/courses');
        // this.courses = response.data;
        // 这里使用静态数据模拟
        await new Promise((resolve) => setTimeout(resolve, 500)); // 模拟延迟
        this.courses = [
          { courseName: '数学' },
          { courseName: '英语' },
          { courseName: '物理' },
          { courseName: '化学' },
        ];
      } catch (error) {
        ElMessage.error('获取课程列表失败');
      } finally {
        this.loading = false;
      }
    },
    // 获取考勤数据
    async fetchAttendanceData() {
      try {
        this.loading = true;
        // 模拟 API 请求，请根据实际情况替换
        // const response = await axios.get('/api/attendance');
        // this.attendanceData = response.data;
        // 这里使用静态数据模拟
        await new Promise((resolve) => setTimeout(resolve, 500)); // 模拟延迟
        this.attendanceData = [
          {
            date: '2023-10-01',
            course: '数学',
            status: '正常',
            checkInTime: '08:00',
            checkOutTime: '12:00',
          },
          {
            date: '2023-10-02',
            course: '英语',
            status: '迟到',
            checkInTime: '08:15',
            checkOutTime: '12:00',
          },
          {
            date: '2023-10-03',
            course: '物理',
            status: '缺勤',
            checkInTime: '-',
            checkOutTime: '-',
          },
          {
            date: '2023-10-04',
            course: '化学',
            status: '正常',
            checkInTime: '08:05',
            checkOutTime: '12:00',
          },
          // 添加更多模拟数据以测试分页
          {
            date: '2023-10-05',
            course: '数学',
            status: '正常',
            checkInTime: '08:00',
            checkOutTime: '12:00',
          },
          {
            date: '2023-10-06',
            course: '英语',
            status: '迟到',
            checkInTime: '08:10',
            checkOutTime: '12:00',
          },
          {
            date: '2023-10-07',
            course: '物理',
            status: '缺勤',
            checkInTime: '-',
            checkOutTime: '-',
          },
          {
            date: '2023-10-08',
            course: '化学',
            status: '正常',
            checkInTime: '08:00',
            checkOutTime: '12:00',
          },
        ];
      } catch (error) {
        ElMessage.error('获取考勤数据失败');
      } finally {
        this.loading = false;
      }
    },
    // 切换侧边栏显示状态
    toggleSidebar() {
      this.isSidebarCollapsed = !this.isSidebarCollapsed;
    },
    // 处理菜单选择
    handleMenuSelect(index) {
      this.activeMenu = index;
      // 根据选择的菜单项进行相应的导航或操作
      ElMessage(`你选择了菜单项 ${index}`);
    },

    // 切换摄像头
    handleSwitchCamera() {
      ElMessage('正在切换摄像头...');
      // TODO: 实现摄像头切换逻辑
    },

    // 开始人脸识别
    handleStartRecognition() {
      ElMessage('正在启动人脸识别...');
      // TODO: 实现人脸识别逻辑
    },
  },
  created() {
    this.fetchCourses();
    this.fetchAttendanceData();
  },
};
</script>
<script setup>
import { saveAs } from 'file-saver';
import * as XLSX from 'xlsx';
import axios from 'axios'; // 确保已安装 axios
import { ElMessage } from 'element-plus'; // 用于消息提示
import { ref, computed } from 'vue';
import { Expand, Fold, Menu, Document } from '@element-plus/icons-vue';
import { Calendar, Notebook, DataLine, User, Switch, Camera } from '@element-plus/icons-vue';
</script>
<style scoped>
.attendance-container {
  height: 100vh;
  overflow: hidden; /* 防止内容溢出 */
}

.attendance-sidebar {
  background-color: #f0f2f5;
  transition: transform 0.3s ease, width 0.3s ease;
  will-change: transform; /* 启用硬件加速 */
}

.attendance-sidebar.collapsed {
  transform: translateX(-100%);
}

.attendance-header {
  background-color: #409eff;
  color: white;
  display: flex;
  align-items: center;
  padding: 0 20px;
}

.toggle-button {
  color: #409eff;
  padding: 0;
  margin-right: 16px;
}

.header-title {
  flex: 1;
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  margin: 0;
}

.filter-form {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.no-data {
  text-align: center;
  padding: 50px 0;
  color: #470404;
}

.el-table th,
.el-table td {
  word-wrap: break-word;
  white-space: normal;
}

@media (max-width: 768px) {
  .filter-form {
    flex-direction: column;
  }
  .filter-form .el-form-item {
    margin-bottom: 10px;
  }
}
</style>
