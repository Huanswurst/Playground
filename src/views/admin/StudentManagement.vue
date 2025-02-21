<template>
  <div class="student-management">
    <h1>学生管理</h1>
    
    <!-- 搜索和操作区域 -->
    <div class="filter-container">
      <el-form :inline="true">
        <el-form-item>
          <el-input v-model="searchQuery" placeholder="搜索学生姓名或学号"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchStudents">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="success" @click="addStudent">添加学生</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 学生表格 -->
    <el-table :data="students" v-loading="loading" style="width: 100%">
      <el-table-column prop="user.display_name" label="姓名"></el-table-column>
      <el-table-column prop="student_number" label="学号"></el-table-column>
      <el-table-column prop="user.email" label="邮箱"></el-table-column>
      <el-table-column label="操作" width="150">
        <template #default="scope">
          <el-button type="text" size="small" @click="editStudent(scope.row)">编辑</el-button>
          <el-button type="text" size="small" @click="deleteStudent(scope.row)">删除</el-button>
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

    <!-- 学生编辑对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible">
      <el-form :model="currentStudent">
        <el-form-item label="姓名">
          <el-input v-model="currentStudent.user.display_name"></el-input>
        </el-form-item>
        <el-form-item label="学号">
          <el-input v-model="currentStudent.student_number"></el-input>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="currentStudent.user.email"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmStudent">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      searchQuery: '',
      students: [],
      total: 0,
      pageSize: 10,
      currentPage: 1,
      loading: false,
      dialogVisible: false,
      dialogTitle: '添加学生',
      currentStudent: {
        user: {
          display_name: '',
          email: '',
          role: 'student'
        },
        student_number: ''
      }
    }
  },
  created() {
    this.fetchStudents()
  },
  methods: {
    async fetchStudents() {
      this.loading = true
      try {
        const response = await axios.get('/api/admin/students/', {
          params: {
            search: this.searchQuery,
            page: this.currentPage
          }
        })
        this.students = response.data.results
        this.total = response.data.count
      } catch (error) {
        this.$message.error('获取学生列表失败')
      } finally {
        this.loading = false
      }
    },
    addStudent() {
      this.currentStudent = {
        user: {
          display_name: '',
          email: '',
          role: 'student'
        },
        student_number: ''
      }
      this.dialogTitle = '添加学生'
      this.dialogVisible = true
    },
    editStudent(student) {
      this.currentStudent = JSON.parse(JSON.stringify(student))
      this.dialogTitle = '编辑学生'
      this.dialogVisible = true
    },
    async deleteStudent(student) {
      try {
        await this.$confirm('确定删除该学生吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        await axios.delete(`/api/admin/students/${student.user.id}/`)
        this.$message.success('删除成功')
        this.fetchStudents()
      } catch (error) {
        if (error !== 'cancel') {
          this.$message.error('删除失败')
        }
      }
    },
    async confirmStudent() {
      try {
        if (this.currentStudent.user.id) {
          // 编辑学生
          await axios.put(`/api/admin/students/${this.currentStudent.user.id}/`, this.currentStudent)
          this.$message.success('更新成功')
        } else {
          // 添加学生
          await axios.post('/api/admin/students/', this.currentStudent)
          this.$message.success('添加成功')
        }
        this.dialogVisible = false
        this.fetchStudents()
      } catch (error) {
        this.$message.error('操作失败')
      }
    },
    handlePageChange(page) {
      this.currentPage = page
      this.fetchStudents()
    }
  }
}
</script>

<style scoped>
.student-management {
  padding: 20px;
}

.filter-container {
  margin-bottom: 20px;
}
</style>
