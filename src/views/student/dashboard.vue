<template>
  <StudentLayout>
    <el-main>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-card class="stat-card" shadow="hover">
            <h3>出勤率</h3>
            <el-progress
              :percentage="attendanceRate"
              :color="attendanceRateColor"
              :stroke-width="16"
            />
            <p class="stat-description">当前出勤率为 {{ attendanceRate }}%</p>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="stat-card" shadow="hover">
            <h3>签到次数</h3>
            <p class="stat-value">{{ checkInCount }} 次</p>
            <p class="stat-description">本学期累计签到次数</p>
          </el-card>
        </el-col>
      </el-row>
      <el-card class="attendance-table" shadow="hover">
        <h2>最近考勤记录</h2>
        <el-table :data="recentAttendance" stripe style="width: 100%">
          <el-table-column prop="date" label="日期" width="180" />
          <el-table-column prop="course" label="课程" width="180" />
          <el-table-column prop="status" label="状态">
            <template #default="{ row }">
              <el-tag :type="getStatusTagType(row.status)">
                {{ row.status }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </el-main>
  </StudentLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import StudentLayout from '@/layouts/StudentLayout.vue'

const router = useRouter()

const attendanceRate = ref(0)
const checkInCount = ref(0)
const recentAttendance = ref([])

// 获取仪表盘数据
const fetchDashboardData = async () => {
  try {
    const response = await axios.get('/api/student/dashboard/')
    attendanceRate.value = response.data.attendance_rate
    checkInCount.value = response.data.check_in_count
    recentAttendance.value = response.data.recent_attendance
  } catch (error) {
    console.error('获取仪表盘数据失败:', error)
  }
}

// 组件挂载时获取数据
onMounted(() => {
  fetchDashboardData()
})

const attendanceRateColor = computed(() => {
  if (attendanceRate.value >= 90) return '#67c23a' // 绿色
  if (attendanceRate.value >= 70) return '#e6a23c' // 橙色
  return '#f56c6c' // 红色
})

const getStatusTagType = (status) => {
  switch (status) {
    case '正常':
      return 'success'
    case '迟到':
      return 'warning'
    case '缺勤':
      return 'danger'
    default:
      return 'info'
  }
}
</script>

<style scoped>
.stat-card {
  text-align: center;
  border-radius: 8px;
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #409eff;
  margin: 10px 0;
}

.stat-description {
  color: #909399;
  font-size: 14px;
}

.attendance-table {
  margin-top: 20px;
  border-radius: 8px;
}

.el-progress {
  margin: 20px 0;
}

.el-tag {
  font-size: 14px;
}
</style>
