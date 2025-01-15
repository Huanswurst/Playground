<template>
  <div class="attendance-management">
    <h1>考勤管理</h1>
    
    <!-- 考勤记录筛选 -->
    <div class="filter-container">
      <el-form :inline="true">
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="用户类型">
          <el-select v-model="filter.userType" placeholder="请选择">
            <el-option label="全部" value=""></el-option>
            <el-option label="教师" value="teacher"></el-option>
            <el-option label="学生" value="student"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 考勤记录表格 -->
    <el-table :data="attendanceList" style="width: 100%">
      <el-table-column prop="username" label="用户名"></el-table-column>
      <el-table-column prop="role" label="角色"></el-table-column>
      <el-table-column prop="date" label="日期"></el-table-column>
      <el-table-column prop="status" label="状态"></el-table-column>
      <el-table-column label="操作">
        <template #default="scope">
          <el-button type="primary" size="small" @click="handleEdit(scope.row)">编辑</el-button>
          <el-button type="danger" size="small" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
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
        userType: ''
      },
      attendanceList: [
        {
          username: 'student1',
          role: '学生',
          date: '2023-10-01',
          status: '正常'
        },
        {
          username: 'teacher1',
          role: '教师',
          date: '2023-10-01',
          status: '迟到'
        }
      ],
      total: 100,
      pageSize: 10
    }
  },
  methods: {
    handleSearch() {
      // 查询考勤记录
      console.log('查询考勤记录', this.filter)
    },
    handleEdit(record) {
      // 编辑考勤记录
      console.log('编辑考勤记录', record)
    },
    handleDelete(record) {
      // 删除考勤记录
      console.log('删除考勤记录', record)
    },
    handlePageChange(page) {
      // 分页切换
      console.log('切换页码', page)
    }
  }
}
</script>

<style scoped>
.attendance-management {
  padding: 20px;
}

.filter-container {
  margin-bottom: 20px;
}
</style>
