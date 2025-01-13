<template>
  <el-container class="dashboard-container">
    <el-header class="dashboard-header">
      <h1>教师首页</h1>
    </el-header>
    <el-main>
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
    </el-main>
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      courseCount: 5,
      studentCount: 120,
    };
  },
};
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
  background-color: #f5f7fa;
}

.dashboard-header {
  background-color: #409eff;
  color: white;
  text-align: center;
  line-height: 60px;
  font-size: 24px;
  font-weight: bold;
  border-radius: 8px;
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
  border-radius: 8px;
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #409eff;
  margin: 10px 0;
}

.stat-description {
  color: #909399;
  font-size: 14px;
}
</style>
