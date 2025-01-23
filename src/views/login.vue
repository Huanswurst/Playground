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
        </el-form-item>
      </el-form>
    </el-card>
  </el-container>
  <el-footer class="footer">
    <div class="footer-content">
      <el-link 
        href="https://beian.miit.gov.cn" 
        target="_blank"
        type="primary"
      >
        苏ICP备2025157736号-1
      </el-link>
    </div>
  </el-footer>
</template>

<script>
import config from '../config';
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
    async handleLogin() {
      this.$refs.loginFormRef.validate(async (valid) => {
        if (valid) {
          try {
            const response = await fetch(`${config.API_BASE_URL}auth/login/`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                username: this.loginForm.username,
                password: this.loginForm.password
              })
            });

            if (!response.ok) {
              const errorData = await response.json();
              throw new Error(errorData.detail || '登录失败');
            }

            const data = await response.json();
            localStorage.setItem('authToken', data.token);
            localStorage.setItem('authRole', this.loginForm.role);
            
            this.token = data.token;
            
            if (this.loginForm.role === 'admin') {
              this.$router.push('/admin/dashboard');
            } else if (this.loginForm.role === 'student') {
              this.$router.push('/student/dashboard');
            } else if (this.loginForm.role === 'teacher') {
              this.$router.push('/teacher/dashboard');
            }
          } catch (error) {
            this.$message.error(error.message);
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
  min-height: 100vh;
  position: relative;
  padding-bottom: 60px;
}

.login-card {
  width: 400px;
  padding: 20px;
  transition: transform 0.3s ease;
}
.login-card:hover {
  transform: translateY(-5px);
}

.footer {
  position: absolute;
  bottom: 0;
  width: 100%;
  text-align: center;
  padding: 10px 0;
  background-color: #f5f7fa;
}

@media screen and (max-width: 768px) {
  .login-card {
    width: 90%;
    margin: 0 auto;
  }
  
  .el-form-item__content {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .el-button {
    width: 100%;
    margin-bottom: 10px;
  }
}
</style>
