<template>
  <el-container>
    <el-header>
      <h1>考勤设置</h1>
    </el-header>
    <el-main>
      <el-card>
        <el-form :model="settingsForm" label-width="120px">
          <el-form-item label="考勤时间">
            <el-time-picker
              v-model="settingsForm.attendanceTime"
              is-range
              range-separator="至"
              start-placeholder="开始时间"
              end-placeholder="结束时间"
              value-format="HH:mm"
            />
          </el-form-item>

          <el-form-item label="迟到时间">
            <el-input-number
              v-model="settingsForm.lateMinutes"
              :min="1"
              :max="60"
              controls-position="right"
            />
            <span class="form-unit">分钟</span>
          </el-form-item>

          <el-form-item label="考勤方式">
            <el-radio-group v-model="settingsForm.attendanceMethod">
              <el-radio value="face">人脸识别</el-radio>
              <el-radio value="geo">地理位置</el-radio>
              <el-radio value="both">双重验证</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item label="通知设置">
            <el-checkbox-group v-model="settingsForm.notifications">
              <el-checkbox label="late">迟到通知</el-checkbox>
              <el-checkbox label="absent">缺勤通知</el-checkbox>
              <el-checkbox label="reminder">课前提醒</el-checkbox>
            </el-checkbox-group>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="handleSave">保存设置</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const settingsForm = ref({
  attendanceTime: ['08:00', '08:30'],
  lateMinutes: 10,
  attendanceMethod: 'face',
  notifications: ['late', 'absent', 'reminder']
})

const handleSave = () => {
  ElMessage.success('设置保存成功')
  console.log('保存设置', settingsForm.value)
}

const handleReset = () => {
  settingsForm.value = {
    attendanceTime: ['08:00', '08:30'],
    lateMinutes: 10,
    attendanceMethod: 'face',
    notifications: ['late', 'absent', 'reminder']
  }
  ElMessage.info('设置已重置')
}
</script>

<style scoped>
.el-header {
  background-color: #409eff;
  color: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.el-card {
  border-radius: 8px;
}

.form-unit {
  margin-left: 10px;
  color: #666;
}
</style>
