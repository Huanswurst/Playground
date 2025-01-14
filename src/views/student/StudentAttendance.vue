<template>
  <el-container class="attendance-container">
    <el-header class="attendance-header">
      <h1>我的考勤记录</h1>
    </el-header>
    <el-main>
      <!-- 筛选条件 -->
      <el-form :inline="true" class="filter-form">
        <el-form-item label="日期">
          <el-date-picker v-model="filterDate" type="date" placeholder="选择日期" />
        </el-form-item>
        <el-form-item label="课程">
          <el-select v-model="filterCourse" placeholder="选择课程">
            <el-option
              v-for="course in courses"
              :key="course.courseName"
              :label="course.courseName"
              :value="course.courseName"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
        </el-form-item>
      </el-form>

      <!-- 考勤表格 -->
      <el-table :data="filteredAttendance" style="width: 100%">
        <el-table-column prop="date" label="日期" sortable />
        <el-table-column prop="course" label="课程" sortable />
        <el-table-column prop="status" label="状态" sortable />
        <el-table-column prop="checkInTime" label="签到时间" sortable />
        <el-table-column prop="checkOutTime" label="签退时间" sortable />
      </el-table>
    </el-main>
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      filterDate: '', // 筛选日期
      filterCourse: '', // 筛选课程
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
      ],
    };
  },
  computed: {
    // 根据筛选条件过滤考勤记录
    filteredAttendance() {
      return this.attendanceData.filter((item) => {
        const matchDate = !this.filterDate || item.date === this.filterDate;
        const matchCourse = !this.filterCourse || item.course === this.filterCourse;
        return matchDate && matchCourse;
      });
    },
  },
  methods: {
    handleSearch() {
      // 搜索逻辑已在 computed 中实现
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
</style>
