<template>
  <el-container class="login-container">
    <el-card class="login-card">
      <h2>登录</h2>
      <el-form :model="loginForm" :rules="rules" ref="loginFormRef">
        <el-form-item label="角色" prop="role">
          <el-radio-group v-model="loginForm.role">
            <el-radio label="student">学生</el-radio>
            <el-radio label="teacher">教师</el-radio>
            <el-radio label="admin">管理员</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="用户名" prop="username">
          <el-input v-model="loginForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            show-password
            placeholder="请输入密码"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleLogin">登录</el-button>
          <el-button @click="goToRegister">注册</el-button>
          <el-button v-if="token" type="danger" @click="logout">登出</el-button>
          <el-button type="info" @click="testApiConnection">测试API连接</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      loginForm: {
        role: 'student',
        username: '',
        password: '',
      },
      rules: {
        role: [{ required: true, message: '请选择角色', trigger: 'change' }],
        username: [{ required: true, message: '用户名不能为空', trigger: 'blur' }],
        password: [{ required: true, message: '密码不能为空', trigger: 'blur' }],
      },
      token: null,
      expires: null,
    };
  },
  methods: {
    handleLogin() {
      this.$refs.loginFormRef.validate((valid) => {
        if (valid) {
          // 如果是管理员角色，直接跳转不保存session
          if (this.loginForm.role === 'admin') {
            this.$router.push('/admin/dashboard');
            return;
          }

          // 学生和教师保存session
          const token = 'mock-token-' + Date.now();
          const expires = Date.now() + 259200000; // 3天有效期
          
          // 保存到localStorage
          localStorage.setItem('authToken', token);
          localStorage.setItem('authExpires', expires);
          localStorage.setItem('authRole', this.loginForm.role);
          
          // 更新组件状态
          this.token = token;
          this.expires = expires;

          if (this.loginForm.role === 'student') {
            this.$router.push('/student/dashboard');
          } else if (this.loginForm.role === 'teacher') {
            this.$router.push('/teacher/dashboard');
          }
        } else {
          console.log('表单验证失败');
        }
      });
    },
    checkLoginStatus() {
      const token = localStorage.getItem('authToken');
      const expires = localStorage.getItem('authExpires');
      
      if (token && expires && Date.now() < Number(expires)) {
        this.token = token;
        this.expires = Number(expires);
        // 根据角色跳转到对应页面
        const role = localStorage.getItem('authRole') || 'student';
        if (role !== 'admin') {
          this.$router.push(`/${role}/dashboard`);
        }
      }
    },
    logout() {
      localStorage.removeItem('authToken');
      localStorage.removeItem('authExpires');
      localStorage.removeItem('authRole');
      this.token = null;
      this.expires = null;
      this.$router.push('/login');
    },
    goToRegister() {
      this.$router.push('/register');
    },
    async testApiConnection() {
      try {
        const response = await fetch('http://localhost:8000/api/test/', {
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include'
        });
        
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`API连接失败: ${response.status} ${errorText}`);
        }
        
        const data = await response.json();
        this.$message.success(`API连接成功: ${data.message}`);
      } catch (error) {
        console.error('API连接错误详情:', error);
        this.$message.error(error.message);
      }
    }
  },
  created() {
    this.checkLoginStatus();
  },
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
.login-card {
  width: 400px;
  padding: 20px;
  transition: transform 0.3s ease;
}
.login-card:hover {
  transform: translateY(-5px);
}
</style>
