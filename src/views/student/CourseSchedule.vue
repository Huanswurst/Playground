<template>
  <div class="course-schedule-container">
    <div class="course-schedule-header">
      <h1 class="header-title">课程表</h1>
      <el-button
        type="primary"
        @click="startAttendance"
        class="start-attendance-btn"
      >
        开始考勤
      </el-button>
    </div>
    
    <el-table
      :data="courses"
      style="width: 100%"
      border
      v-loading="loading"
    >
      <el-table-column prop="name" label="课程名称" width="180" />
      <el-table-column prop="time" label="上课时间" width="180" />
      <el-table-column prop="location" label="上课地点" />
      <el-table-column label="考勤操作" width="280">
        <template #default="scope">
          <el-button
            type="success"
            size="small"
            @click="startCourseAttendance(scope.row)"
          >
            开始考勤
          </el-button>
          <el-button
            type="primary"
            size="small"
            @click="viewAttendanceHistory(scope.row)"
          >
            考勤历史
          </el-button>
          <el-button
            type="warning"
            size="small"
            @click="appealAttendance(scope.row)"
          >
            考勤申诉
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const startCourseAttendance = (course) => {
  router.push({
    path: '/student/selfie-capture',
    query: {
      courseId: course.id,
      courseName: course.name
    }
  })
}

// 模拟课程数据
const courses = ref([
  {
    id: 1,
    name: '高等数学',
    time: '周一 8:00-9:40',
    location: 'A101'
  },
  {
    id: 2, 
    name: '大学英语',
    time: '周二 10:00-11:40',
    location: 'B202'
  }
])

// 查看考勤历史
const viewAttendanceHistory = (course) => {
  console.log('查看考勤历史', course)
  // TODO: 调用API获取考勤历史
}

// 考勤申诉
const appealAttendance = (course) => {
  console.log('考勤申诉', course)
  // TODO: 调用API提交考勤申诉
}
</script>

<style scoped>
.course-schedule-container {
  padding: 20px;
}

.course-schedule-header {
  margin-bottom: 20px;
}

.header-title {
  font-size: 24px;
  font-weight: bold;
  margin-right: 20px;
}

.start-attendance-btn {
  margin-left: auto;
}

.no-data {
  text-align: center;
  padding: 50px 0;
  color: #909399;
}

@media (max-width: 768px) {
  .course-schedule-container {
    padding: 10px;
  }
  
  .header-title {
    font-size: 20px;
  }
}
</style>