<template>
  <el-container class="attendance-container">
    <el-header class="dashboard-header">
      <div class="header-content">
        <h1 class="header-title">课堂考勤系统</h1>
      </div>
    </el-header>

    <el-main>
      <el-card class="success-card" shadow="hover">
        <div class="success-content">
          <el-icon class="success-icon" :size="80">
            <Select />
          </el-icon>
          <h2 class="success-title">考勤成功</h2>
          <p class="success-time">{{ currentTime }}</p>
          
          <el-button 
            type="primary" 
            class="back-button"
            @click="$router.push('/student/attendance')"
          >
            返回考勤页面
          </el-button>
        </div>
      </el-card>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref } from 'vue'
import { Select } from '@element-plus/icons-vue'

const currentTime = ref(new Date().toLocaleString())
</script>

<style scoped lang="scss">
.attendance-container {
  height: 100vh;
  background: #f0f2f5;

  .dashboard-header {
    background: linear-gradient(135deg, #409EFF 0%, #337ecc 100%);
    .header-content {
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100%;
      
      .header-title {
        margin: 0;
        color: white;
        font-size: 24px;
        font-family: 'Microsoft YaHei';
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
      }
    }
  }

  .success-card {
    max-width: 600px;
    margin: 40px auto;
    border-radius: 12px;
    
    .success-content {
      padding: 40px;
      text-align: center;

      .success-icon {
        color: #67C23A;
        margin-bottom: 24px;
      }

      .success-title {
        color: #303133;
        font-size: 28px;
        font-family: 'Microsoft YaHei';
        margin: 16px 0;
      }

      .success-time {
        color: #606266;
        font-size: 16px;
        margin-bottom: 32px;
      }

      .back-button {
        padding: 12px 40px;
        font-size: 16px;
        border-radius: 8px;
        letter-spacing: 1px;
      }
    }
  }
}

@media (max-width: 768px) {
  .success-card {
    margin: 20px!important;
    
    .success-content {
      padding: 20px!important;
      
      .success-title {
        font-size: 22px!important;
      }
      
      .success-time {
        font-size: 14px!important;
      }
    }
  }
}
</style>
