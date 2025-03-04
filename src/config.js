import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NODE_ENV === 'production' 
    ? 'https://www.huanswurst.top:5173' 
    : 'https://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

// 请求拦截器
apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

// 响应拦截器
apiClient.interceptors.response.use(response => {
  return response.data;
}, error => {
  if (error.response) {
    switch (error.response.status) {
      case 401:
        localStorage.removeItem('token');
        window.location.href = '/login';
        break;
      case 403:
        window.location.href = '/403';
        break;
      default:
        break;
    }
  }
  return Promise.reject(error);
});

export default {
  apiClient,
  apiEndpoints: {
    admin: {
      attendance: '/api/admin/attendance/',
      classes: '/api/admin/classes/',
      courses: '/api/admin/courses/',
      students: '/api/admin/students/',
      teachers: '/api/admin/teachers/'
    },
    teacher: {
      courses: '/api/teacher/courses/',
      attendance: '/api/teacher/attendance/'
    },
    student: {
      attendance: '/api/student/attendance/',
      location: '/api/student/location/',
      courses: '/api/student/courses/'
    }
  }
}
