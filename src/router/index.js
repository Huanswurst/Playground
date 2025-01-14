import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/login.vue';
import Register from '../views/Register.vue';

// 学生界面
import StudentDashboard from '../views/student/dashboard.vue';
import StudentAttendance from '../views/student/StudentAttendance.vue';
/*import StudentCheckIn from '../views/student/CheckIn.vue';
import StudentCheckOut from '../views/student/CheckOut.vue';
*/
// 教师界面
import TeacherDashboard from '../views/teacher/dashboard.vue';
import CourseAttendance from '../views/teacher/CourseAttendance.vue';
import ManageCourses from '../views/teacher/ManageCourses.vue';

const routes = [
    { path: '/', redirect: '/login' },
    { path: '/login', component: Login },
    { path: '/register', component: Register },
    // 学生路由
    { path: '/student/dashboard', component: StudentDashboard },
    { path: '/student/attendance', component: StudentAttendance },
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
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
