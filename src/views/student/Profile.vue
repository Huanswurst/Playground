<template>
  <div class="profile-container">
    <h1>学生个人中心</h1>
    <div class="profile-content">
      <div class="profile-info">
        <div class="info-item">
          <label>姓名：</label>
          <span>张三</span>
        </div>
        <div class="info-item">
          <label>学号：</label>
          <span>20230001</span>
        </div>
        <div class="info-item">
          <label>班级：</label>
          <span>计算机科学与技术1班</span>
        </div>
      </div>
      
      <div class="profile-actions">
        <button class="btn">修改密码</button>
        <button class="btn">查看考勤记录</button>
      </div>
    </div>
  </div>
</template>

<script setup>
// 这里可以添加组件逻辑
</script>

<style scoped>
.profile-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
}

.profile-content {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.profile-info {
  margin-bottom: 20px;
}

.info-item {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  font-size: 16px;
}

.info-item label {
  width: 80px;
  font-weight: bold;
  color: #666;
}

.info-item span {
  flex: 1;
  color: #333;
}

.profile-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
}

.btn {
  padding: 8px 20px;
  border: none;
  border-radius: 4px;
  background: #409eff;
  color: #fff;
  cursor: pointer;
  transition: background 0.3s;
}

.btn:hover {
  background: #66b1ff;
}
</style>
