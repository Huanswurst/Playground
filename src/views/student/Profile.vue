作业提交<template>
  <div class="profile-container">
    <h1>个人信息</h1>
    <el-form label-width="120px">
      <el-form-item label="姓名">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="学号">
        <el-input v-model="form.studentId" disabled />
      </el-form-item>
      <el-form-item label="邮箱">
        <el-input v-model="form.email" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">保存</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const form = ref({
  name: '',
  studentId: '20230001',
  email: ''
})

const onSubmit = () => {
  // TODO: 提交表单
}
</script>

<style scoped>
.profile-container {
  padding: 20px;
}
</style>