<template>
  <el-container class="dashboard-container">
    <el-header class="dashboard-header">
      <h1>教师首页</h1>
    </el-header>
    <el-main>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-card>
            <h3>课程总数</h3>
            <p>{{ courseCount }} 门</p>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card>
            <h3>学生总数</h3>
            <p>{{ studentCount }} 人</p>
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
}
.dashboard-header {
  background-color: #409eff;
  color: white;
  text-align: center;
  line-height: 60px;
}
</style>