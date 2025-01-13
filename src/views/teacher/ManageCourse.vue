<template>
  <el-container class="dashboard-container" :class="{ mobile: isMobile }">
    <el-header class="dashboard-header">
      <h1>课程管理</h1>
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

      <!-- 课程管理表格 -->
      <el-card class="course-table" shadow="hover">
        <h2>课程列表</h2>

        <!-- 搜索和操作按钮 -->
        <div class="table-actions">
          <el-input
            v-model="searchQuery"
            placeholder="搜索课程名称"
            clearable
            style="width: 200px; margin-right: 10px;"
            @clear="handleSearch"
            @input="handleSearch"
          />
          <el-button type="primary" @click="handleAddCourse">添加课程</el-button>
        </div>

        <!-- 表格 -->
        <el-table
          :data="filteredCourses"
          stripe
          style="width: 100%"
          :default-sort="{ prop: 'courseName', order: 'ascending' }"
        >
          <el-table-column prop="courseName" label="课程名称" sortable />
          <el-table-column prop="teacherName" label="授课教师" sortable />
          <el-table-column prop="studentCount" label="学生人数" sortable />
          <el-table-column label="操作" width="200">
            <template #default="{ row }">
              <el-button type="primary" @click="handleViewAttendance(row)">查看考勤</el-button>
              <el-button type="danger" @click="handleDeleteCourse(row)">删除</el-button>
            </template>
          </el-table-column>
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
      courseCount: 5,
      studentCount: 120,
      courses: [
        {
          id: 1,
          courseName: '数学',
          teacherName: '张老师',
          studentCount: 50,
        },
        {
          id: 2,
          courseName: '英语',
          teacherName: '李老师',
          studentCount: 45,
        },
        {
          id: 3,
          courseName: '物理',
          teacherName: '王老师',
          studentCount: 40,
        },
        {
          id: 4,
          courseName: '化学',
          teacherName: '赵老师',
          studentCount: 35,
        },
      ],
    };
  },
  computed: {
    // 根据搜索关键词过滤表格数据
    filteredCourses() {
      return this.courses.filter((item) =>
        item.courseName.toLowerCase().includes(this.searchQuery.toLowerCase())
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
      if (type === 'course') {
        this.$message.success('点击了课程总数卡片');
      } else if (type === 'student') {
        this.$message.success('点击了学生总数卡片');
      }
    },
    // 处理搜索
    handleSearch() {
      // 搜索逻辑已在 computed 中实现
    },
    // 处理添加课程
    handleAddCourse() {
      this.$message.info('添加课程功能待实现');
    },
    // 处理删除课程
    handleDeleteCourse(row) {
      this.courses = this.courses.filter((course) => course !== row);
      this.$message.success('删除课程成功');
    },
    // 处理查看考勤
    handleViewAttendance(row) {
      this.$router.push({ name: 'CourseAttendance', params: { courseId: row.id } });
    },
  },
};
</script>

<style scoped>
/* 复用 Dashboard 的样式 */
@import './Dashboard.css';
</style>
