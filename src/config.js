
import axios from 'axios'
import store from './store'

// 环境配置
const envConfig = {
  development: {
    apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
    auth: {
      tokenKey: 'attendance-token',
      refreshTokenKey: 'attendance-refresh-token'
    }
  },
  production: {
    apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'https://www.huanswurst.top:5173',
    auth: {
      tokenKey: 'attendance-token',
      refreshTokenKey: 'attendance-refresh-token'
    }
  }
}

const currentEnv = import.meta.env.MODE || 'development'

// 创建axios实例
const apiClient = axios.create({
  baseURL: envConfig[currentEnv].apiBaseUrl,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
apiClient.interceptors.request.use(
  config => {
    const token = store.state.token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
apiClient.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          store.dispatch('logout')
          break
        case 403:
          // 处理权限不足
          break
        case 500:
          // 处理服务器错误
          break
        default:
          break
      }
    }
    return Promise.reject(error)
  }
)

export default {
  apiClient,
  
  // API endpoints
  apiEndpoints: {
    auth: {
      login: '/api/v1/auth/login/',
      register: '/api/v1/auth/register/',
      refresh: '/api/v1/auth/refresh/',
      logout: '/api/v1/auth/logout/',
      currentUser: '/api/v1/auth/current-user/'
    },
    admin: {
      attendance: '/api/v1/admin/attendance/',
      classes: '/api/v1/admin/classes/',
      courses: '/api/v1/admin/courses/',
      students: '/api/v1/admin/students/',
      teachers: '/api/v1/admin/teachers/'
    },
    teacher: {
      courses: '/api/v1/teacher/courses/',
      attendance: '/api/v1/teacher/attendance/',
      statistics: '/api/v1/teacher/statistics/'
    },
    student: {
      attendance: '/api/v1/student/attendance/',
      location: '/api/v1/student/location/',
      courses: '/api/v1/student/courses/',
      faceRecognition: '/api/v1/student/face-recognition/'

    }
  }
}
