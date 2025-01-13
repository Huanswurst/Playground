<template>
  <el-container class="dashboard-container">
    <el-header class="dashboard-header">
      <h1>教师首页</h1>
    </el-header>
    <el-main>
      <!-- PC 端界面 -->
      <template v-if="!isMobile">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card class="stat-card" shadow="hover">
              <h3>课程总数</h3>
              <p class="stat-value">{{ courseCount }} 门</p>
              <p class="stat-description">本学期开设的课程数量</p>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card class="stat-card" shadow="hover">
              <h3>学生总数</h3>
              <p class="stat-value">{{ studentCount }} 人</p>
              <p class="stat-description">本学期授课学生总数</p>
            </el-card>
          </el-col>
        </el-row>
      </template>

      <!-- 移动端界面 -->
      <template v-else>
        <el-row :gutter="10">
          <el-col :span="24">
            <el-card class="stat-card" shadow="hover">
              <h3>课程总数</h3>
              <p class="stat-value">{{ courseCount }} 门</p>
              <p class="stat-description">本学期开设的课程数量</p>
            </el-card>
          </el-col>
          <el-col :span="24">
            <el-card class="stat-card" shadow="hover">
              <h3>学生总数</h3>
              <p class="stat-value">{{ studentCount }} 人</p>
              <p class="stat-description">本学期授课学生总数</p>
            </el-card>
          </el-col>
        </el-row>
      </template>
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
  line-height: 1px;
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
  border-radius: 8px;
  transition: transform 0.3s ease;
  margin-bottom: 10px; /* 移动端增加卡片间距 */
}

.stat-card:hover {
  transform: translateY(-5px);
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

/* 移动端样式 */
@media (max-width: 768px) {
  .el-main {
    padding: 10px; /* 移动端减少内边距 */
  }

  .stat-value {
    font-size: 20px; /* 移动端数据字体稍小 */
  }

  .stat-description {
    font-size: 10px; /* 移动端描述字体稍小 */
  }
}
</style>
