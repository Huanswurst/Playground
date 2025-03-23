import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/login.vue';
import Register from '../views/Register.vue';
import Recognition from '../views/recogntion.vue';

// 学生界面
import StudentDashboard from '../views/student/dashboard.vue';
import StudentAttendance from '../views/student/StudentAttendance.vue';
import FaceRecognitionAttendance from '../views/student/FaceRecognitionAttendance.vue';
import GeoFaceRecognitionAttendance from '../views/student/GeoFaceRecognitionAttendance.vue';
import PhotoRecognition from '../views/student/PhotoRecognition.vue';
import StudentSelfieCapture from '../views/student/StudentSelfieCapture.vue';
import SpecialCaseEnrollment from '../views/student/SpecialCaseEnrollment.vue';

// 教师界面
import TeacherDashboard from '../views/teacher/dashboard.vue';
import CourseAttendance from '../views/teacher/CourseAttendance.vue';
import ManageCourses from '../views/teacher/ManageCourses.vue';
import GroupPhotoCapture from '../views/teacher/GroupPhotoCapture.vue';

// 管理员界面
import AttendanceManagement from '../views/admin/AttendanceManagement.vue';
import ClassManagement from '../views/admin/ClassManagement.vue';
import CourseManagement from '../views/admin/CourseManagement.vue';
import DataStatistics from '../views/admin/DataStatistics.vue';
import LogManagement from '../views/admin/LogManagement.vue';
import PermissionManagement from '../views/admin/PermissionManagement.vue';
import StudentManagement from '../views/admin/StudentManagement.vue';
import SystemSettings from '../views/admin/SystemSettings.vue';
import TeacherManagement from '../views/admin/TeacherManagement.vue';
import UserManagement from '../views/admin/UserManagement.vue';

// 临时视图
import ObjectRecognition from '../views/tmpView/objectRecogntion.vue';

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/recognition', component: Recognition },
  
  // 学生路由
  { path: '/student/dashboard', component: StudentDashboard },
  { path: '/student/attendance', component: StudentAttendance },
  { path: '/student/face-recognition', component: FaceRecognitionAttendance },
  {
    path: '/student/attendance/success',
    name: 'AttendanceSuccess',
    component: () => import('../views/student/AttendanceSuccess.vue')
  },
  { path: '/student/geo-attendance', component: GeoFaceRecognitionAttendance },
  { path: '/student/photo-recognition', component: PhotoRecognition },
  { path: '/student/selfie-capture', component: StudentSelfieCapture },
  { path: '/student/special-case', component: SpecialCaseEnrollment },
  { path: '/student/profile', component: () => import('../views/student/Profile.vue') },
  { path: '/student/password', component: () => import('../views/student/ChangePassword.vue') },
  
  // 教师路由
  { path: '/teacher/dashboard', component: TeacherDashboard },
  { path: '/teacher/courses', component: ManageCourses },
  { path: '/teacher/course-attendance', component: CourseAttendance },
  { path: '/teacher/group-photo', component: GroupPhotoCapture },
  {
    path: '/teacher/courses/:courseId/attendance',
    name: 'CourseAttendance',
    component: CourseAttendance,
    props: true,
  },
  
  // 管理员路由
  { path: '/admin/attendance', component: AttendanceManagement },
  { path: '/admin/class', component: ClassManagement },
  { path: '/admin/course', component: CourseManagement },
  { path: '/admin/statistics', component: DataStatistics },
  { path: '/admin/log', component: LogManagement },
  { path: '/admin/permission', component: PermissionManagement },
  { path: '/admin/students', component: StudentManagement },
  { path: '/admin/settings', component: SystemSettings },
  { path: '/admin/teachers', component: TeacherManagement },
  { path: '/admin/users', component: UserManagement },
  
  // 临时视图路由
  { path: '/object-recognition', component: ObjectRecognition },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
