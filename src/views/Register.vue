<template>
  <el-container class="register-container">
    <el-card class="register-card">
      <h2>注册</h2>
      <el-form :model="registerForm" :rules="rules" ref="registerFormRef" label-width="100px">
        <el-form-item label="角色" prop="role">
          <el-radio-group v-model="registerForm.role">
          <el-radio value="teacher">教师</el-radio>
          <el-radio value="student">学生</el-radio>
          <el-radio value="admin">管理员</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="用户名" prop="username">
          <el-input v-model="registerForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="请输入密码"
            show-password
          />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            show-password
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleRegister">注册</el-button>
          <el-button @click="goToLogin">返回登录</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </el-container>
</template>

<script>
import config from '@/config';

export default {
  data() {
    // 自定义密码一致性验证规则
    const validateConfirmPassword = (rule, value, callback) => {
      if (value !== this.registerForm.password) {
        callback(new Error('两次输入的密码不一致'));
      } else {
        callback();
      }
    };

    return {
      registerForm: {
        role: 'teacher', // 默认角色为教师
        username: '',
        password: '',
        confirmPassword: '',
      },
      rules: {
        role: [{ required: true, message: '请选择角色', trigger: 'change' }],
        username: [
          { required: true, message: '用户名不能为空', trigger: 'blur' },
          { min: 3, max: 16, message: '用户名长度应为 3 到 16 个字符', trigger: 'blur' },
        ],
        password: [
          { required: true, message: '密码不能为空', trigger: 'blur' },
          { min: 6, max: 16, message: '密码长度应为 6 到 16 个字符', trigger: 'blur' },
        ],
        confirmPassword: [
          { required: true, message: '请再次输入密码', trigger: 'blur' },
          { validator: validateConfirmPassword, trigger: 'blur' },
        ],
      },
    };
  },
  methods: {
    // 处理注册逻辑
    async handleRegister() {
      this.$refs.registerFormRef.validate(async (valid) => {
        if (valid) {
          try {
            const response = await fetch(`${config.API_BASE_URL}auth/register/`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                username: this.registerForm.username,
                password: this.registerForm.password,
                role: this.registerForm.role
              })
            });

            if (!response.ok) {
              const errorData = await response.json();
              throw new Error(errorData.detail || '注册失败');
            }

            const data = await response.json();
            this.$message.success('注册成功！');
            
            if (this.registerForm.role === 'student') {
              this.$router.push('/face-recognition');
            } else {
              this.$router.push('/login');
            }
          } catch (error) {
            this.$message.error(error.message);
          }
        } else {
          this.$message.error('请检查表单填写是否正确');
        }
      });
    },
    // 跳转到登录页面
    goToLogin() {
      this.$router.push('/login');
    },
  },
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
.register-card {
  width: 400px;
  padding: 20px;
}
</style>
