export default {
  apiBaseUrl: process.env.NODE_ENV === 'production' 
    ? 'https://your-production-api.com' 
    : 'http://localhost:8000',
  
  // API endpoints
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
    }
  }
}
