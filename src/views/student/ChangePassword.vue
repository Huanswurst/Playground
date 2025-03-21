<template>
  <div class="change-password-container">
    <h1>修改密码</h1>
    <el-form label-width="120px">
      <el-form-item label="原密码">
        <el-input v-model="form.oldPassword" type="password" />
      </el-form-item>
      <el-form-item label="新密码">
        <el-input v-model="form.newPassword" type="password" />
      </el-form-item>
      <el-form-item label="确认新密码">
        <el-input v-model="form.confirmPassword" type="password" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">提交</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const form = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const onSubmit = () => {
  // TODO: 提交表单
}
</script>

<style scoped>
.change-password-container {
  padding: 20px;
}
</style>