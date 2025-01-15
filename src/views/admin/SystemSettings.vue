<template>
  <div class="system-settings">
    <h1>系统设置</h1>
    
    <el-form :model="settings" label-width="120px">
      <el-form-item label="考勤规则">
        <el-input-number v-model="settings.attendanceStartTime" :min="0" :max="23"></el-input-number>
        <span class="time-label">:00 至 </span>
        <el-input-number v-model="settings.attendanceEndTime" :min="0" :max="23"></el-input-number>
        <span class="time-label">:00</span>
      </el-form-item>

      <el-form-item label="迟到时间">
        <el-input-number v-model="settings.lateTime" :min="1" :max="60"></el-input-number>
        <span class="time-label">分钟</span>
      </el-form-item>

      <el-form-item label="通知设置">
        <el-checkbox-group v-model="settings.notificationTypes">
          <el-checkbox label="email">邮件通知</el-checkbox>
          <el-checkbox label="sms">短信通知</el-checkbox>
          <el-checkbox label="app">应用内通知</el-checkbox>
        </el-checkbox-group>
      </el-form-item>

      <el-form-item label="数据保留">
        <el-input-number v-model="settings.dataRetentionDays" :min="30" :max="365"></el-input-number>
        <span class="time-label">天</span>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="handleSave">保存设置</el-button>
        <el-button @click="handleReset">恢复默认</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      settings: {
        attendanceStartTime: 8,
        attendanceEndTime: 18,
        lateTime: 15,
        notificationTypes: ['email', 'app'],
        dataRetentionDays: 180
      }
    }
  },
  methods: {
    handleSave() {
      // 保存设置
      console.log('保存系统设置', this.settings)
      this.$message.success('系统设置已保存')
    },
    handleReset() {
      // 恢复默认设置
      this.settings = {
        attendanceStartTime: 8,
        attendanceEndTime: 18,
        lateTime: 15,
        notificationTypes: ['email', 'app'],
        dataRetentionDays: 180
      }
      this.$message.success('已恢复默认设置')
    }
  }
}
</script>

<style scoped>
.system-settings {
  padding: 20px;
}

.time-label {
  margin: 0 8px;
  color: #606266;
}
</style>
