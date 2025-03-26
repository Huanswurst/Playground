import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/login.vue';
import Register from '../views/Register.vue';
import Recognition from '../views/recogntion.vue';

// 学生界面
import StudentDashboard from '../views/student/dashboard.vue';
import StudentAttendance from '../views/student/StudentAttendance.vue';
import FaceRecognitionAttendance from '../views/student/FaceRecognitionAttendance.vue';
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
  {
    path: '/student',
    component: () => import('@/layouts/StudentLayout.vue'),
    children: [
      {
        path: '',
        redirect: 'dashboard'
      },
      {
        path: 'dashboard',
        name: 'StudentDashboard',
        component: StudentDashboard
      },
      {
        path: 'attendance',
        name: 'StudentAttendance',
        component: StudentAttendance
      },
      {
        path: 'face-recognition',
        name: 'FaceRecognition',
        component: FaceRecognitionAttendance
      },
      {
        path: 'attendance/success',
        name: 'AttendanceSuccess',
        component: () => import('../views/student/AttendanceSuccess.vue')
      },
      {
        path: 'profile',
        name: 'StudentProfile',
        component: () => import('../views/student/Profile.vue')
      },
      {
        path: 'password',
        name: 'ChangePassword',
        component: () => import('../views/student/ChangePassword.vue')
      },
      {
        path: 'course-schedule',
        name: 'CourseSchedule',
        component: () => import('../views/student/CourseSchedule.vue')
      },
      {
        path: 'selfie-capture',
        name: 'StudentSelfieCapture',
        component: StudentSelfieCapture,
        props: {
          default: true,
          title: '学生自拍'
        }
      },
    ]
  },
  
  // 教师路由
  { path: '/teacher/dashboard', component: TeacherDashboard },
  { path: '/teacher/attendance', component: CourseAttendance },
  { path: '/teacher/attendance/statistics', component: () => import('../views/teacher/AttendanceStatistics.vue') },
  { path: '/teacher/courses', component: ManageCourses },
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
