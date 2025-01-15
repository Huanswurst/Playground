<template>
  <div class="log-management">
    <h1>日志管理</h1>
    
    <!-- 日志筛选 -->
    <div class="filter-container">
      <el-form :inline="true">
        <el-form-item label="操作类型">
          <el-select v-model="filter.type" placeholder="请选择">
            <el-option label="全部" value=""></el-option>
            <el-option label="登录" value="login"></el-option>
            <el-option label="考勤" value="attendance"></el-option>
            <el-option label="系统" value="system"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
          ></el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 日志表格 -->
    <el-table :data="logList" style="width: 100%">
      <el-table-column prop="time" label="时间" width="180"></el-table-column>
      <el-table-column prop="username" label="用户名" width="120"></el-table-column>
      <el-table-column prop="type" label="操作类型" width="120"></el-table-column>
      <el-table-column prop="description" label="操作描述"></el-table-column>
      <el-table-column prop="ip" label="IP地址" width="150"></el-table-column>
    </el-table>

    <!-- 分页 -->
    <el-pagination
      background
      layout="prev, pager, next"
      :total="total"
      :page-size="pageSize"
      @current-change="handlePageChange"
    ></el-pagination>
  </div>
</template>

<script>
export default {
  data() {
    return {
      dateRange: [],
      filter: {
        type: ''
      },
      logList: [
        {
          time: '2023-10-01 08:30:12',
          username: 'admin1',
          type: '登录',
          description: '用户登录系统',
          ip: '192.168.1.1'
        },
        {
          time: '2023-10-01 09:15:45',
          username: 'teacher1',
          type: '考勤',
          description: '提交考勤记录',
          ip: '192.168.1.2'
        },
        {
          time: '2023-10-01 10:00:23',
          username: 'admin1',
          type: '系统',
          description: '修改系统设置',
          ip: '192.168.1.1'
        }
      ],
      total: 100,
      pageSize: 10
    }
  },
  methods: {
    handleSearch() {
      // 查询日志
      console.log('查询日志', this.filter)
    },
    handlePageChange(page) {
      // 分页切换
      console.log('切换页码', page)
    }
  }
}
</script>

<style scoped>
.log-management {
  padding: 20px;
}

.filter-container {
  margin-bottom: 20px;
}
</style>
