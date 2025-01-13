<template>
  <el-container class="dashboard-container" :class="{ mobile: isMobile }">
    <el-header class="dashboard-header">
      <h1>{{ course.courseName }} 考勤详情</h1>
    </el-header>
    <el-main>
      <!-- 统计卡片 -->
      <el-row :gutter="isMobile ? 10 : 20">
        <el-col :span="isMobile ? 24 : 8">
          <el-card class="stat-card" shadow="hover">
            <h3>总考勤率</h3>
            <p class="stat-value">{{ overallAttendanceRate }}%</p>
            <p class="stat-description">本课程的平均考勤率</p>
          </el-card>
        </el-col>
        <el-col :span="isMobile ? 24 : 8">
          <el-card class="stat-card" shadow="hover">
            <h3>缺勤人数</h3>
            <p class="stat-value">{{ totalAbsentCount }} 人</p>
            <p class="stat-description">本课程的缺勤总人数</p>
          </el-card>
        </el-col>
        <el-col :span="isMobile ? 24 : 8">
          <el-card class="stat-card" shadow="hover">
            <h3>迟到人数</h3>
            <p class="stat-value">{{ totalLateCount }} 人</p>
            <p class="stat-description">本课程的迟到总人数</p>
          </el-card>
        </el-col>
      </el-row>

      <!-- 考勤表格 -->
      <el-card class="attendance-table" shadow="hover">
        <h2>考勤记录</h2>

        <!-- 搜索和操作按钮 -->
        <div class="table-actions">
          <el-input
            v-model="searchQuery"
            placeholder="搜索日期或班级"
            clearable
            style="width: 200px; margin-right: 10px;"
            @clear="handleSearch"
            @input="handleSearch"
          />
          <el-button type="primary" @click="handlePublishAttendance">发布考勤</el-button>
        </div>

        <!-- 表格 -->
        <el-table
          :data="filteredAttendance"
          stripe
          style="width: 100%"
          :default-sort="{ prop: 'date', order: 'descending' }"
        >
          <el-table-column prop="date" label="日期" sortable />
          <el-table-column prop="class" label="班级" sortable />
          <el-table-column prop="attendanceRate" label="出勤率" sortable>
            <template #default="{ row }">
              <el-progress
                :percentage="row.attendanceRate"
                :color="getProgressColor(row.attendanceRate)"
                :stroke-width="12"
              />
            </template>
          </el-table-column>
          <el-table-column prop="absentCount" label="缺勤人数" sortable />
          <el-table-column prop="lateCount" label="迟到人数" sortable />
        </el-table>
      </el-card>
    </el-main>
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      isMobile: false, // 默认不是移动端
      searchQuery: '', // 搜索关键词
      course: {
        id: 1,
        courseName: '数学',
        teacherName: '张老师',
        studentCount: 50,
      },
      attendanceData: [
        {
          date: '2023-10-01',
          class: '高一（1）班',
          attendanceRate: 95,
          absentCount: 2,
          lateCount: 1,
        },
        {
          date: '2023-10-02',
          class: '高一（2）班',
          attendanceRate: 90,
          absentCount: 3,
          lateCount: 2,
        },
        {
          date: '2023-10-03',
          class: '高二（1）班',
          attendanceRate: 85,
          absentCount: 5,
          lateCount: 3,
        },
      ],
    };
  },
  computed: {
    // 计算总考勤率
    overallAttendanceRate() {
      const total = this.attendanceData.reduce((sum, item) => sum + item.attendanceRate, 0);
      return (total / this.attendanceData.length).toFixed(2);
    },
    // 计算缺勤总人数
    totalAbsentCount() {
      return this.attendanceData.reduce((sum, item) => sum + item.absentCount, 0);
    },
    // 计算迟到总人数
    totalLateCount() {
      return this.attendanceData.reduce((sum, item) => sum + item.lateCount, 0);
    },
    // 根据搜索关键词过滤表格数据
    filteredAttendance() {
      return this.attendanceData.filter(
        (item) =>
          item.date.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          item.class.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
  mounted() {
    // 检测设备类型
    this.checkDevice();
    // 监听窗口变化
    window.addEventListener('resize', this.checkDevice);
    // 获取课程 ID
    const courseId = this.$route.params.courseId;
    this.fetchCourseData(courseId);
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
    // 获取课程数据
    async fetchCourseData(courseId) {
      try {
        // 调用 API 获取课程数据
        // const response = await axios.get(`/api/courses/${courseId}`);
        // this.course = response.data;
        this.$message.success('课程数据加载成功');
      } catch (error) {
        this.$message.error('课程数据加载失败');
      }
    },
    // 处理搜索
    handleSearch() {
      // 搜索逻辑已在 computed 中实现
    },
    // 处理发布考勤
    handlePublishAttendance() {
      this.$message.success('考勤发布成功');
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
/* 复用 Dashboard 的样式 */
@import './Dashboard.css';
</style>
