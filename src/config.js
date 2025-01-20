export default {
  apiBaseUrl: process.env.NODE_ENV === 'production' 
    ? 'https://www.huanswurst.top' 
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
    },
    student: {
      attendance: '/api/student/attendance/',
      location: '/api/student/location/',
      courses: '/api/student/courses/'
    }
  }
}
