<template>
  <div class="data-statistics">
    <h1>数据统计</h1>
    
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
  </div>
</template>

<script>
import * as echarts from 'echarts'

export default {
  data() {
    return {
      attendanceChart: null,
      lateReasonChart: null,
      monthlyTrendChart: null
    }
  },
  mounted() {
    this.initCharts()
  },
  methods: {
    initCharts() {
      // 出勤率统计
      this.attendanceChart = echarts.init(this.$refs.attendanceChart)
      this.attendanceChart.setOption({
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
      this.lateReasonChart = echarts.init(this.$refs.lateReasonChart)
      this.lateReasonChart.setOption({
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
      this.monthlyTrendChart = echarts.init(this.$refs.monthlyTrendChart)
      this.monthlyTrendChart.setOption({
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
  },
  beforeDestroy() {
    if (this.attendanceChart) {
      this.attendanceChart.dispose()
    }
    if (this.lateReasonChart) {
      this.lateReasonChart.dispose()
    }
    if (this.monthlyTrendChart) {
      this.monthlyTrendChart.dispose()
    }
  }
}
</script>

<style scoped>
.data-statistics {
  padding: 20px;
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
