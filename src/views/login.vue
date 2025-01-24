<template>
  <el-container class="login-container fade-in">
    <el-card class="login-card">
      <h2>登录</h2>
      <el-form :model="loginForm" :rules="rules" ref="loginFormRef">
        <!-- 角色选择 -->
        <el-form-item label="角色" prop="role">
          <el-radio-group v-model="loginForm.role">
            <el-radio label="student">学生</el-radio>
            <el-radio label="teacher">教师</el-radio>
            <el-radio label="admin">管理员</el-radio>
          </el-radio-group>
        </el-form-item>

        <!-- 用户名 -->
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
          />
        </el-form-item>

        <!-- 密码 -->
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            show-password
            placeholder="请输入密码"
          />
        </el-form-item>

        <!-- 记住我复选框 -->
        <el-form-item>
          <el-checkbox v-model="loginForm.rememberMe">记住我</el-checkbox>
        </el-form-item>

        <!-- 登录、注册、退出按钮 -->
        <el-form-item>
          <el-button
            type="primary"
            :loading="isLoggingIn"
            @click="handleLogin"
          >
            {{ isLoggingIn ? '登录中...' : '登录' }}
          </el-button>
          <el-button @click="goToRegister">注册</el-button>
          <el-button v-if="token" type="danger" @click="logout">登出</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-footer class="footer">
      <div class="footer-content">
        <span>基于图像识别的考勤系统 © 2025</span>
        <el-divider direction="vertical" />
        <el-link 
          href="https://beian.miit.gov.cn" 
          target="_blank"
          type="primary"
        >
          苏ICP备2025157736号-1
        </el-link>
      </div>
    </el-footer>
  </el-container>
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
        rememberMe: false, // 新增「记住我」字段
      },
      rules: {
        role: [
          { required: true, message: '请选择角色', trigger: 'change' }
        ],
        username: [
          { required: true, message: '用户名不能为空', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '密码不能为空', trigger: 'blur' }
        ],
      },
      token: null,
      expires: null,
      isLoggingIn: false  // 登录按钮加载状态
    };
  },
  methods: {
    async handleLogin() {
      // 验证表单
      this.$refs.loginFormRef.validate(async (valid) => {
        if (!valid) {
          console.log('表单验证失败');
          return;
        }
        try {
          this.isLoggingIn = true;
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

          // 如果选择了「记住我」，可在此设置更长的过期时间
          if (this.loginForm.rememberMe) {
            // 例如，7 天后过期
            const future = Date.now() + 7 * 24 * 60 * 60 * 1000;
            localStorage.setItem('authExpires', future.toString());
          } else {
            // 不记住我，设置短时间或不设置 expires
            const soon = Date.now() + 2 * 60 * 60 * 1000;
            localStorage.setItem('authExpires', soon.toString());
          }

          this.token = data.token;

          // 根据角色跳转
          if (this.loginForm.role === 'admin') {
            this.$router.push('/admin/dashboard');
          } else if (this.loginForm.role === 'student') {
            this.$router.push('/student/dashboard');
          } else if (this.loginForm.role === 'teacher') {
            this.$router.push('/teacher/dashboard');
          }
        } catch (error) {
          this.$message.error(error.message);
        } finally {
          this.isLoggingIn = false;
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
/* 容器整体布局 */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  position: relative;
  padding-bottom: 60px;
  background: #f0f2f5; /* 增加微背景色 */
  overflow: hidden;    /* 为视觉效果做准备 */
}

/* 卡片样式 */
.login-card {
  width: 400px;
  padding: 20px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
  border-radius: 6px; /* 轻微圆角 */
  background-color: #fff;
}

.login-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}

/* 增加淡入动画 */
.fade-in {
  animation: fadeIn 0.7s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(15px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 底部样式 */
.footer {
  position: absolute;
  bottom: 0;
  width: 100%;
  text-align: center;
  padding: 10px 0;
  background-color: #f5f7fa;
}

.footer-content {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

/* 响应式处理 */
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