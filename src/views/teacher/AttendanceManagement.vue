<template>
  <el-container>
    <el-header>
      <h1>考勤管理</h1>
    </el-header>
    <el-main>
      <el-card>
        <el-table :data="attendanceRecords" stripe>
          <el-table-column prop="date" label="日期" />
          <el-table-column prop="course" label="课程" />
          <el-table-column prop="class" label="班级" />
          <el-table-column prop="status" label="状态">
            <template #default="{ row }">
              <el-tag :type="getStatusTagType(row.status)">
                {{ row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template #default="{ row }">
              <el-button type="primary" size="small" @click="handleEdit(row)">
                编辑
              </el-button>
              <el-button type="danger" size="small" @click="handleDelete(row)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref } from 'vue'

const attendanceRecords = ref([
  {
    date: '2023-10-01',
    course: '数学',
    class: '高一（1）班',
    status: '正常'
  },
  {
    date: '2023-10-02',
    course: '英语',
    class: '高一（2）班',
    status: '迟到'
  }
])

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

const handleEdit = (record) => {
  console.log('编辑考勤记录', record)
}

const handleDelete = (record) => {
  console.log('删除考勤记录', record)
}
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
}
</style>
