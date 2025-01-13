<template>
  <el-container class="dashboard-container" :class="{ mobile: isMobile }">
    <el-header class="dashboard-header">
      <h1>教师首页</h1>
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
      </el-row>

      <!-- 近期授课考勤情况表格 -->
      <el-card class="attendance-table" shadow="hover">
        <h2>近期授课考勤情况</h2>
        <el-table :data="recentAttendance" stripe style="width: 100%">
          <el-table-column prop="date" label="日期" width="120" />
          <el-table-column prop="course" label="课程" width="120" />
          <el-table-column prop="class" label="班级" width="120" />
          <el-table-column prop="attendanceRate" label="出勤率" width="120">
            <template #default="{ row }">
              <el-progress
                :percentage="row.attendanceRate"
                :color="getProgressColor(row.attendanceRate)"
                :stroke-width="12"
              />
            </template>
          </el-table-column>
          <el-table-column prop="absentCount" label="缺勤人数" width="120" />
          <el-table-column prop="lateCount" label="迟到人数" width="120" />
        </el-table>
      </el-card>
    </el-main>
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      courseCount: 5,
      studentCount: 120,
      isMobile: false, // 默认不是移动端
      recentAttendance: [
        {
          date: '2023-10-01',
          course: '数学',
          class: '高一（1）班',
          attendanceRate: 95,
          absentCount: 2,
          lateCount: 1,
        },
        {
          date: '2023-10-02',
          course: '英语',
          class: '高一（2）班',
          attendanceRate: 90,
          absentCount: 3,
          lateCount: 2,
        },
        {
          date: '2023-10-03',
          course: '物理',
          class: '高二（1）班',
          attendanceRate: 85,
          absentCount: 5,
          lateCount: 3,
        },
        {
          date: '2023-10-04',
          course: '化学',
          class: '高二（2）班',
          attendanceRate: 98,
          absentCount: 1,
          lateCount: 0,
        },
      ],
    };
  },
  mounted() {
    // 检测设备类型
    this.checkDevice();
    // 监听窗口变化
    window.addEventListener('resize', this.checkDevice);
  },
  beforeDestroy() {
    // 移除监听
    window.removeEventListener('resize', this.checkDevice);
  },
  methods: {
    checkDevice() {
      // 判断是否为移动端
      this.isMobile = window.innerWidth <= 768;
    },
    handleCardClick(type) {
      if (type === 'course') {
        this.$message.success('点击了课程总数卡片');
      } else if (type === 'student') {
        this.$message.success('点击了学生总数卡片');
      }
    },
    getProgressColor(attendanceRate) {
      if (attendanceRate >= 90) return '#67c23a'; // 绿色
      if (attendanceRate >= 70) return '#e6a23c'; // 橙色
      return '#f56c6c'; // 红色
    },
  },
};
</script>

<style scoped>
.dashboard-container {
  height: 100vh; /* 确保容器占满整个视口高度 */
  display: flex;
  flex-direction: column;
}

.dashboard-header {
  background-color: #409eff;
  color: white;
  text-align: center;
  line-height: 20px;
  font-size: 24px;
  font-weight: bold;
  padding: 0 20px; /* 添加内边距 */
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1); /* 添加阴影 */
}

.el-main {
  flex: 1; /* 让 main 部分占据剩余空间 */
  padding: 20px;
  background-color: #f5f7fa;
}

.stat-card {
  text-align: center;
  border-radius: 12px; /* 增加圆角 */
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  margin-bottom: 10px; /* 移动端增加卡片间距 */
  cursor: pointer; /* 添加手型光标 */
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2); /* 悬停时增加阴影 */
}

.stat-value {
  font-size: 24px; /* 移动端字体稍小 */
  font-weight: bold;
  color: #409eff;
  margin: 10px 0;
}

.stat-description {
  color: #909399;
  font-size: 12px; /* 移动端字体稍小 */
}

.attendance-table {
  margin-top: 20px;
  border-radius: 12px; /* 增加圆角 */
}

.attendance-table h2 {
  margin-bottom: 20px;
  font-size: 20px;
  font-weight: bold;
  color: #303133;
}

/* 移动端样式 */
.dashboard-container.mobile .dashboard-header {
  line-height: 50px; /* 移动端标题高度减小 */
  font-size: 20px; /* 移动端标题字体稍小 */
}

.dashboard-container.mobile .el-main {
  padding: 10px; /* 移动端减少内边距 */
}

.dashboard-container.mobile .stat-card {
  border-radius: 16px; /* 移动端卡片圆角更大 */
  margin-bottom: 15px; /* 移动端卡片间距更大 */
}

.dashboard-container.mobile .stat-value {
  font-size: 22px; /* 移动端数据字体稍小 */
}

.dashboard-container.mobile .stat-description {
  font-size: 14px; /* 移动端描述字体稍大 */
}

.dashboard-container.mobile .attendance-table {
  margin-top: 10px;
}
</style>
