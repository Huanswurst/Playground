<template>
  <el-container class="dashboard-container" :class="{ mobile: isMobile }">
    <el-header class="dashboard-header">
      <h1>课程考勤</h1>
    </el-header>
    <el-main>
      <!-- 统计卡片 -->
      <el-row :gutter="isMobile ? 10 : 20">
        <el-col :span="isMobile ? 24 : 8">
          <el-card class="stat-card" shadow="hover" @click.native="handleCardClick('attendance')">
            <h3>总考勤率</h3>
            <p class="stat-value">{{ overallAttendanceRate }}%</p>
            <p class="stat-description">所有课程的平均考勤率</p>
          </el-card>
        </el-col>
        <el-col :span="isMobile ? 24 : 8">
          <el-card class="stat-card" shadow="hover" @click.native="handleCardClick('absent')">
            <h3>缺勤人数</h3>
            <p class="stat-value">{{ totalAbsentCount }} 人</p>
            <p class="stat-description">所有课程的缺勤总人数</p>
          </el-card>
        </el-col>
        <el-col :span="isMobile ? 24 : 8">
          <el-card class="stat-card" shadow="hover" @click.native="handleCardClick('late')">
            <h3>迟到人数</h3>
            <p class="stat-value">{{ totalLateCount }} 人</p>
            <p class="stat-description">所有课程的迟到总人数</p>
          </el-card>
        </el-col>
      </el-row>

      <!-- 考勤表格 -->
      <el-card class="attendance-table" shadow="hover">
        <h2>课程考勤详情</h2>

        <!-- 搜索和操作按钮 -->
        <div class="table-actions">
          <el-input
            v-model="searchQuery"
            placeholder="搜索课程或班级"
            clearable
            style="width: 200px; margin-right: 10px;"
            @clear="handleSearch"
            @input="handleSearch"
          />
          <el-button type="primary" @click="handleImport">导入数据</el-button>
          <el-button type="success" @click="handleExport">导出数据</el-button>
        </div>

        <!-- 表格 -->
        <el-table
          :data="filteredAttendance"
          stripe
          style="width: 100%"
          :default-sort="{ prop: 'date', order: 'descending' }"
        >
          <el-table-column prop="date" label="日期" sortable />
          <el-table-column prop="course" label="课程" sortable />
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
      attendanceData: [
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
          item.course.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          item.class.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
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
      if (type === 'attendance') {
        this.$message.success('点击了总考勤率卡片');
      } else if (type === 'absent') {
        this.$message.success('点击了缺勤人数卡片');
      } else if (type === 'late') {
        this.$message.success('点击了迟到人数卡片');
      }
    },
    getProgressColor(attendanceRate) {
      if (attendanceRate >= 90) return '#67c23a'; // 绿色
      if (attendanceRate >= 70) return '#e6a23c'; // 橙色
      return '#f56c6c'; // 红色
    },
    // 处理搜索
    handleSearch() {
      // 搜索逻辑已在 computed 中实现
    },
    // 处理导入数据
    handleImport() {
      this.$message.info('导入数据功能待实现');
    },
    // 处理导出数据
    handleExport() {
      this.$message.success('导出数据成功');
      const data = this.filteredAttendance;
      const headers = ['日期', '课程', '班级', '出勤率', '缺勤人数', '迟到人数'];
      const rows = data.map((item) => [
        item.date,
        item.course,
        item.class,
        `${item.attendanceRate}%`,
        item.absentCount,
        item.lateCount,
      ]);
      this.exportToExcel(headers, rows, '考勤数据');
    },
    // 导出为 Excel
    exportToExcel(headers, rows, fileName) {
      const xlsx = require('xlsx');
      const worksheet = xlsx.utils.aoa_to_sheet([headers, ...rows]);
      const workbook = xlsx.utils.book_new();
      xlsx.utils.book_append_sheet(workbook, worksheet, 'Sheet1');
      xlsx.writeFile(workbook, `${fileName}.xlsx`);
    },
  },
};
</script>

<style scoped>
/* 复用 Dashboard 的样式 */
@import './Dashboard.css';
</style>
