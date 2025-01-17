<template>
  <el-container>
    <el-aside
      :class="{ 'attendance-sidebar': true, collapsed: isSidebarCollapsed }"
      :style="{ width: isSidebarCollapsed ? '0' : '200px' }"
    >
      <el-menu
        default-active="1"
        class="el-menu-vertical-demo"
        v-if="!isSidebarCollapsed"
      >
        <el-sub-menu index="1">
          <template #title>
            <el-icon><calendar /></el-icon>
            <span>考勤管理</span>
          </template>
          <el-menu-item index="1-1" route="/admin/attendance">考勤记录</el-menu-item>
          <el-menu-item index="1-2" route="/admin/attendance/statistics">考勤统计</el-menu-item>
          <el-menu-item index="1-3" route="/admin/attendance/settings">考勤设置</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="2">
          <template #title>
            <el-icon><lock /></el-icon>
            <span>权限管理</span>
          </template>
          <el-menu-item index="2-1" route="/admin/permission/roles">角色管理</el-menu-item>
          <el-menu-item index="2-2" route="/admin/permission/users">用户权限</el-menu-item>
          <el-menu-item index="2-3" route="/admin/permission/audit">权限审计</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="3">
          <template #title>
            <el-icon><document /></el-icon>
            <span>日志管理</span>
          </template>
          <el-menu-item index="3-1" route="/admin/log/login">登录日志</el-menu-item>
          <el-menu-item index="3-2" route="/admin/log/operation">操作日志</el-menu-item>
          <el-menu-item index="3-3" route="/admin/log/error">错误日志</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="4">
          <template #title>
            <el-icon><data-line /></el-icon>
            <span>数据统计</span>
          </template>
          <el-menu-item index="4-1" route="/admin/statistics/attendance">考勤统计</el-menu-item>
          <el-menu-item index="4-2" route="/admin/statistics/course">课程统计</el-menu-item>
          <el-menu-item index="4-3" route="/admin/statistics/user">用户统计</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="5">
          <template #title>
            <el-icon><notebook /></el-icon>
            <span>课程管理</span>
          </template>
          <el-menu-item index="5-1" route="/admin/course/schedule">课程安排</el-menu-item>
          <el-menu-item index="5-2" route="/admin/course/teacher">教师分配</el-menu-item>
          <el-menu-item index="5-3" route="/admin/course/student">学生选课</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="6">
          <template #title>
            <el-icon><school /></el-icon>
            <span>班级管理</span>
          </template>
          <el-menu-item index="6-1" route="/admin/class/student">学生管理</el-menu-item>
          <el-menu-item index="6-2" route="/admin/class/teacher">教师管理</el-menu-item>
          <el-menu-item index="6-3" route="/admin/class/schedule">课表管理</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>
    
    <el-container>
      <el-header class="dashboard-header">
        <div class="header-content">
          <el-button
            type="link"
            class="toggle-button"
            @click="toggleSidebar"
            aria-label="Toggle menu"
          >
            <el-icon :size="24" style="vertical-align: middle;">
              <component :is="isSidebarCollapsed ? Expand : Fold" />
            </el-icon>
          </el-button>
          <h1 class="header-title">数据统计系统</h1>
        </div>
      </el-header>
      <el-main>
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="chart-container">
              <h3>出勤率统计</h3>
              <div ref="attendanceChart" class="chart"></div>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="chart-container">
              <h3>迟到原因分布</h3>
              <div ref="lateReasonChart" class="chart"></div>
            </div>
          </el-col>
        </el-row>

        <el-row :gutter="20" style="margin-top: 20px">
          <el-col :span="24">
            <div class="chart-container">
              <h3>月度考勤趋势</h3>
              <div ref="monthlyTrendChart" class="chart"></div>
            </div>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { Menu as IconMenu, Setting, Expand, Fold, DataLine, TrendCharts, User, Avatar } from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import { ref, onMounted, onBeforeUnmount } from 'vue'

const isSidebarCollapsed = ref(false)
const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

const attendanceChart = ref(null)
const lateReasonChart = ref(null)
const monthlyTrendChart = ref(null)

const initCharts = () => {
  // 出勤率统计
  attendanceChart.value = echarts.init(attendanceChart.value)
  attendanceChart.value.setOption({
    tooltip: {
      trigger: 'item'
    },
    legend: {
      bottom: '10%',
      left: 'center'
    },
    series: [
      {
        name: '出勤率',
        type: 'pie',
        radius: '50%',
        data: [
          { value: 85, name: '正常' },
          { value: 10, name: '迟到' },
          { value: 5, name: '缺勤' }
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  })

  // 迟到原因分布
  lateReasonChart.value = echarts.init(lateReasonChart.value)
  lateReasonChart.value.setOption({
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    xAxis: {
      type: 'category',
      data: ['交通堵塞', '起床晚', '其他']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        data: [120, 200, 150],
        type: 'bar'
      }
    ]
  })

  // 月度考勤趋势
  monthlyTrendChart.value = echarts.init(monthlyTrendChart.value)
  monthlyTrendChart.value.setOption({
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '出勤率',
        type: 'line',
        data: [85, 88, 90, 92, 91, 89, 93],
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color: 'rgba(64, 158, 255, 0.8)'
            },
            {
              offset: 1,
              color: 'rgba(64, 158, 255, 0.2)'
            }
          ])
        }
      }
    ]
  })
}

onMounted(() => {
  initCharts()
})

onBeforeUnmount(() => {
  if (attendanceChart.value) {
    attendanceChart.value.dispose()
  }
  if (lateReasonChart.value) {
    lateReasonChart.value.dispose()
  }
  if (monthlyTrendChart.value) {
    monthlyTrendChart.value.dispose()
  }
})
</script>

<style scoped>
.attendance-sidebar {
  transition: width 0.3s ease;
}

.dashboard-header {
  background-color: #409eff;
  color: white;
  border-radius: 8px;
  margin-bottom: 20px;
  padding: 0 20px;
}

.header-content {
  display: flex;
  align-items: center;
  height: 100%;
}

.header-title {
  flex: 1;
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  margin: 0;
}

.toggle-button {
  color: #409eff;
  padding: 0;
  margin-right: 16px;
}

.chart-container {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.chart {
  height: 300px;
}
</style>
