<template>
  <el-container class="dashboard-container">
    <el-header class="dashboard-header">
      <h1>学生首页</h1>
    </el-header>
    <el-main>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-card>
            <h3>出勤率</h3>
            <el-progress :percentage="attendanceRate" :color="attendanceRateColor" />
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card>
            <h3>签到次数</h3>
            <p>{{ checkInCount }} 次</p>
          </el-card>
        </el-col>
      </el-row>
      <el-card class="attendance-table">
        <h2>最近考勤记录</h2>
        <el-table :data="recentAttendance">
          <el-table-column prop="date" label="日期" />
          <el-table-column prop="course" label="课程" />
          <el-table-column prop="status" label="状态" />
        </el-table>
      </el-card>
    </el-main>
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      attendanceRate: 85,
      checkInCount: 12,
      recentAttendance: [
        { date: '2023-10-01', course: '数学', status: '正常' },
        { date: '2023-10-02', course: '英语', status: '迟到' },
      ],
    };
  },
  computed: {
    attendanceRateColor() {
      if (this.attendanceRate >= 90) return '#67c23a';
      if (this.attendanceRate >= 70) return '#e6a23c';
      return '#f56c6c';
    },
  },
};
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}
.dashboard-header {
  background-color: #409eff;
  color: white;
  text-align: center;
  line-height: 60px;
}
.attendance-table {
  margin-top: 20px;
}
</style>