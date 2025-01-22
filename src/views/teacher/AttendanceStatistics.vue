<template>
  <el-container>
    <el-header>
      <h1>考勤统计</h1>
    </el-header>
    <el-main>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card>
            <h3>出勤率趋势</h3>
            <div ref="attendanceChart" style="height: 300px;"></div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card>
            <h3>考勤统计概览</h3>
            <el-table :data="statisticsData" stripe>
              <el-table-column prop="class" label="班级" />
              <el-table-column prop="attendanceRate" label="出勤率" />
              <el-table-column prop="lateCount" label="迟到次数" />
              <el-table-column prop="absentCount" label="缺勤次数" />
            </el-table>
          </el-card>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'

const attendanceChart = ref(null)
const statisticsData = ref([
  {
    class: '高一（1）班',
    attendanceRate: '95%',
    lateCount: 2,
    absentCount: 1
  },
  {
    class: '高一（2）班',
    attendanceRate: '90%',
    lateCount: 5,
    absentCount: 3
  }
])

onMounted(() => {
  const chart = echarts.init(attendanceChart.value)
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: ['10/01', '10/02', '10/03', '10/04', '10/05']
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        formatter: '{value}%'
      }
    },
    series: [
      {
        name: '出勤率',
        type: 'line',
        data: [95, 90, 92, 96, 94],
        smooth: true
      }
    ]
  }
  chart.setOption(option)
})
</script>

<style scoped>
.el-header {
  background-color: #409eff;
  color: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.el-card {
  border-radius: 8px;
  margin-bottom: 20px;
}

h3 {
  margin-top: 0;
  margin-bottom: 20px;
}
</style>
