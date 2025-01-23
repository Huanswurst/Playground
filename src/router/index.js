import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/login.vue';
import Register from '../views/Register.vue';

// 学生界面
import StudentDashboard from '../views/student/dashboard.vue';
import StudentAttendance from '../views/student/StudentAttendance.vue';
import FaceRecognitionAttendance from '../views/student/FaceRecognitionAttendance.vue';
import GeoFaceRecognitionAttendance from '../views/student/GeoFaceRecognitionAttendance.vue';
/*import StudentCheckIn from '../views/student/CheckIn.vue';
import StudentCheckOut from '../views/student/CheckOut.vue';
*/
// 教师界面
import TeacherDashboard from '../views/teacher/dashboard.vue';
import CourseAttendance from '../views/teacher/CourseAttendance.vue';
import ManageCourses from '../views/teacher/ManageCourses.vue';

// 管理员界面
import AttendanceManagement from '../views/admin/AttendanceManagement.vue';
import ClassManagement from '../views/admin/ClassManagement.vue';
import CourseManagement from '../views/admin/CourseManagement.vue';
import DataStatistics from '../views/admin/DataStatistics.vue';
import LogManagement from '../views/admin/LogManagement.vue';
import PermissionManagement from '../views/admin/PermissionManagement.vue';

const routes = [
    { path: '/', redirect: '/login' },
    { path: '/login', component: Login },
    { path: '/register', component: Register },
    // 学生路由
    { path: '/student/dashboard', component: StudentDashboard },
    { path: '/student/attendance', component: StudentAttendance },
    { path: '/student/face-recognition', component: FaceRecognitionAttendance },
    { path: '/student/geo-attendance', component: GeoFaceRecognitionAttendance },
    /*{ path: '/student/checkin', component: StudentCheckIn },
    { path: '/student/checkout', component: StudentCheckOut },*/
    // 教师路由
    { path: '/teacher/dashboard', component: TeacherDashboard },
    { path: '/teacher/course-attendance', component: CourseAttendance },
  {
    path: '/teacher/courses/:courseId/attendance',
    name: 'CourseAttendance',
    component: CourseAttendance,
    props: true, // 将路由参数作为 props 传递给组件
  },
  // 管理员路由
  { path: '/admin/attendance', component: AttendanceManagement },
  { path: '/admin/class', component: ClassManagement },
  { path: '/admin/course', component: CourseManagement },
  { path: '/admin/statistics', component: DataStatistics },
  { path: '/admin/log', component: LogManagement },
  { path: '/admin/permission', component: PermissionManagement },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
