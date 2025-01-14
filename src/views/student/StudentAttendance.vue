<template>
  <el-container class="attendance-container">
    <el-header class="attendance-header">
      <h1>我的考勤记录</h1>
    </el-header>
    <el-main>
      <!-- 筛选条件 -->
      <el-form :inline="true" class="filter-form">
        <el-form-item label="日期">
          <el-date-picker
            v-model="filterDate"
            type="date"
            placeholder="选择日期"
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
        </el-form-item>
      </el-form>

      <!-- 考勤表格 -->
      <el-table :data="pagedAttendance" style="width: 100%" border>
        <el-table-column prop="date" label="日期" sortable />
        <el-table-column prop="course" label="课程" sortable />
        <el-table-column prop="status" label="状态" sortable>
          <template slot-scope="scope">
            <el-tag :type="getStatusTagType(scope.row.status)">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="checkInTime" label="签到时间" sortable />
        <el-table-column prop="checkOutTime" label="签退时间" sortable />
      </el-table>

      <!-- 分页 -->
      <el-pagination
        class="pagination"
        :current-page="currentPage"
        :page-size="pageSize"
        :total="filteredAttendance.length"
        @current-change="handlePageChange"
        layout="total, prev, pager, next"
      />
    </el-main>
  </el-container>
</template>

<script>
import { saveAs } from 'file-saver';
import XLSX from 'xlsx';

export default {
  data() {
    return {
      filterDate: '', // 筛选日期
      filterCourse: '', // 筛选课程
      filterStatus: '', // 筛选状态
      currentPage: 1, // 当前页码
      pageSize: 10, // 每页显示条数
      courses: [
        { courseName: '数学' },
        { courseName: '英语' },
      ],
      attendanceData: [
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
          course: '数学',
          status: '缺勤',
          checkInTime: '-',
          checkOutTime: '-',
        },
      ],
    };
  },
  computed: {
    // 根据筛选条件过滤考勤记录
    filteredAttendance() {
      return this.attendanceData.filter((item) => {
        const matchDate = !this.filterDate || item.date === this.filterDate;
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
    // 处理搜索
    handleSearch() {
      this.currentPage = 1; // 重置到第一页
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
      const worksheet = XLSX.utils.json_to_sheet(data);
      const workbook = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(workbook, worksheet, '考勤记录');
      const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
      const blob = new Blob([excelBuffer], { type: 'application/octet-stream' });
      saveAs(blob, '考勤记录.xlsx');
    },
  },
};
</script>

<style scoped>
.attendance-container {
  padding: 20px;
}

.attendance-header {
  background-color: #409eff;
  color: white;
  text-align: center;
  line-height: 60px;
}

.filter-form {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}
</style>
