import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

// 使用路由懒加载
const Login = () => import(/* webpackChunkName: "auth" */ '../views/login.vue')
const Register = () => import(/* webpackChunkName: "auth" */ '../views/Register.vue')

const StudentDashboard = () => import(/* webpackChunkName: "student" */ '../views/student/dashboard.vue')
const FaceRecognitionAttendance = () => import(/* webpackChunkName: "student" */ '../views/student/FaceRecognitionAttendance.vue')
const GeoFaceRecognitionAttendance = () => import(/* webpackChunkName: "student" */ '../views/student/GeoFaceRecognitionAttendance.vue')

const TeacherDashboard = () => import(/* webpackChunkName: "teacher" */ '../views/teacher/dashboard.vue')
const CourseAttendance = () => import(/* webpackChunkName: "teacher" */ '../views/teacher/CourseAttendance.vue')
const AttendanceManagement = () => import(/* webpackChunkName: "teacher" */ '../views/teacher/AttendanceManagement.vue')
const AttendanceStatistics = () => import(/* webpackChunkName: "teacher" */ '../views/teacher/AttendanceStatistics.vue')
const AttendanceSettings = () => import(/* webpackChunkName: "teacher" */ '../views/teacher/AttendanceSettings.vue')

  const AdminDashboard = () => import(/* webpackChunkName: "admin" */ '../views/admin/AttendanceManagement.vue')
const SystemSettings = () => import(/* webpackChunkName: "admin" */ '../views/admin/SystemSettings.vue')

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { requiresAuth: false }
  },

  // Student routes
  {
    path: '/student',
    name: 'StudentDashboard',
    component: StudentDashboard,
    meta: { requiresAuth: true, role: 'student' }
  },
  {
    path: '/student/face-recognition',
    name: 'FaceRecognition',
    component: FaceRecognitionAttendance,
    meta: { requiresAuth: true, role: 'student' }
  },
  {
    path: '/student/geo-attendance',
    name: 'GeoAttendance',
    component: GeoFaceRecognitionAttendance,
    meta: { requiresAuth: true, role: 'student' }
  },

  // Teacher routes
  {
    path: '/teacher',
    name: 'TeacherDashboard',
    component: TeacherDashboard,
    meta: { requiresAuth: true, role: 'teacher' }
  },
  {
    path: '/teacher/courses/:courseId/attendance',
    name: 'CourseAttendance',
    component: CourseAttendance,
    props: true,
    meta: { requiresAuth: true, role: 'teacher' }
  },
  {
    path: '/teacher/attendance',
    name: 'TeacherAttendance',
    component: AttendanceManagement,
    meta: { requiresAuth: true, role: 'teacher' }
  },
  {
    path: '/teacher/attendance/statistics',
    name: 'AttendanceStatistics',
    component: AttendanceStatistics,
    meta: { requiresAuth: true, role: 'teacher' }
  },
  {
    path: '/teacher/attendance/settings',
    name: 'AttendanceSettings',
    component: AttendanceSettings,
    meta: { requiresAuth: true, role: 'teacher' }
  },

  // Admin routes
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/settings',
    name: 'SystemSettings',
    component: SystemSettings,
    meta: { requiresAuth: true, role: 'admin' }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 增强导航守卫
router.beforeEach(async (to, from, next) => {
    store.commit('auth/SET_LOADING', true)
  
    try {
      const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
      const requiredRole = to.meta.role
      const currentUser = store.state.auth.user

      // 如果需要认证但用户未登录
      if (requiresAuth && !currentUser) {
        // 尝试获取当前用户
        await store.dispatch('auth/fetchCurrentUser')
      }

      // 获取更新后的用户状态
      const updatedUser = store.state.auth.user

      // 权限验证
      if (requiresAuth && !updatedUser) {
        next('/login')
      } else if (requiresAuth && updatedUser && requiredRole !== updatedUser.role) {
        next('/')
      } else {
        // 设置页面标题
        document.title = to.meta.title || 'Attendance System'
        next()
      }
    } catch (error) {
      store.commit('auth/SET_ERROR', error.message)
      next('/')
    } finally {
      store.commit('auth/SET_LOADING', false)
  }
})

// 添加路由元信息
routes.forEach(route => {
  route.meta = route.meta || {}
  route.meta.title = route.meta.title || route.name
})

export default router
