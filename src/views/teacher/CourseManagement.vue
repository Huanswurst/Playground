<template>
  <div class="course-management">
    <h1>课程管理</h1>
    
    <div class="toolbar">
      <el-button type="primary" @click="handleAddCourse">
        添加课程
      </el-button>
    </div>

    <el-table
      :data="courses"
      style="width: 100%"
      stripe
      v-loading="loading"
    >
      <el-table-column
        prop="courseName"
        label="课程名称"
        width="180"
      />
      <el-table-column
        prop="teacher"
        label="授课教师"
        width="120"
      />
      <el-table-column
        prop="time"
        label="上课时间"
        width="180"
      />
      <el-table-column
        prop="location"
        label="上课地点"
        width="150"
      />
      <el-table-column
        label="操作"
        width="180"
      >
        <template #default="scope">
          <el-button
            size="small"
            @click="handleEdit(scope.$index, scope.row)"
          >
            编辑
          </el-button>
          <el-button
            size="small"
            type="danger"
            @click="handleDelete(scope.$index, scope.row)"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      class="pagination"
      background
      layout="prev, pager, next"
      :total="total"
      :page-size="pageSize"
      @current-change="handlePageChange"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 模拟数据
const courses = ref([
  {
    courseName: 'Vue.js 高级开发',
    teacher: '王老师',
    time: '周一 10:00-12:00',
    location: 'A101'
  },
  {
    courseName: 'Node.js 实战',
    teacher: '李老师',
    time: '周三 14:00-16:00',
    location: 'B202'
  }
])

const loading = ref(false)
const total = ref(50)
const pageSize = ref(10)

const handleAddCourse = () => {
  // 添加课程逻辑
}

const handleEdit = (index, row) => {
  // 编辑课程逻辑
}

const handleDelete = (index, row) => {
  // 删除课程逻辑
}

const handlePageChange = (currentPage) => {
  // 分页逻辑
}
</script>

<style scoped>
.course-management {
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
}

.toolbar {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  justify-content: flex-end;
}
</style>
