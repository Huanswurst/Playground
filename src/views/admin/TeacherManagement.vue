<template>
  <div class="teacher-management">
    <h1>教师管理</h1>
    
    <!-- 搜索和操作区域 -->
    <div class="filter-container">
      <el-form :inline="true">
        <el-form-item>
          <el-input v-model="searchQuery" placeholder="搜索教师姓名或工号"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchStaff">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="success" @click="addStaff">添加教师</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 教师表格 -->
    <el-table :data="staff" v-loading="loading" style="width: 100%">
      <el-table-column prop="user.display_name" label="姓名"></el-table-column>
      <el-table-column prop="employee_number" label="工号"></el-table-column>
      <el-table-column prop="position" label="职位"></el-table-column>
      <el-table-column prop="user.email" label="邮箱"></el-table-column>
      <el-table-column label="操作" width="150">
        <template #default="scope">
          <el-button type="text" size="small" @click="editStaff(scope.row)">编辑</el-button>
          <el-button type="text" size="small" @click="deleteStaff(scope.row)">删除</el-button>
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

    <!-- 教师编辑对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible">
      <el-form :model="currentStaff">
        <el-form-item label="姓名">
          <el-input v-model="currentStaff.user.display_name"></el-input>
        </el-form-item>
        <el-form-item label="工号">
          <el-input v-model="currentStaff.employee_number"></el-input>
        </el-form-item>
        <el-form-item label="职位">
          <el-select v-model="currentStaff.position" placeholder="请选择">
            <el-option label="教师" value="teacher"></el-option>
            <el-option label="管理员" value="administrator"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="currentStaff.user.email"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmStaff">确定</el-button>
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
      staff: [],
      total: 0,
      pageSize: 10,
      currentPage: 1,
      loading: false,
      dialogVisible: false,
      dialogTitle: '添加教师',
      currentStaff: {
        user: {
          display_name: '',
          email: '',
          role: 'teacher'
        },
        employee_number: '',
        position: 'teacher'
      }
    }
  },
  created() {
    this.fetchStaff()
  },
  methods: {
    async fetchStaff() {
      this.loading = true
      try {
        const response = await axios.get('/api/admin/staff/', {
          params: {
            search: this.searchQuery,
            page: this.currentPage
          }
        })
        this.staff = response.data.results
        this.total = response.data.count
      } catch (error) {
        this.$message.error('获取教师列表失败')
      } finally {
        this.loading = false
      }
    },
    addStaff() {
      this.currentStaff = {
        user: {
          display_name: '',
          email: '',
          role: 'teacher'
        },
        employee_number: '',
        position: 'teacher'
      }
      this.dialogTitle = '添加教师'
      this.dialogVisible = true
    },
    editStaff(staff) {
      this.currentStaff = JSON.parse(JSON.stringify(staff))
      this.dialogTitle = '编辑教师'
      this.dialogVisible = true
    },
    async deleteStaff(staff) {
      try {
        await this.$confirm('确定删除该教师吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        await axios.delete(`/api/admin/staff/${staff.user.id}/`)
        this.$message.success('删除成功')
        this.fetchStaff()
      } catch (error) {
        if (error !== 'cancel') {
          this.$message.error('删除失败')
        }
      }
    },
    async confirmStaff() {
      try {
        if (this.currentStaff.user.id) {
          // 编辑教师
          await axios.put(`/api/admin/staff/${this.currentStaff.user.id}/`, this.currentStaff)
          this.$message.success('更新成功')
        } else {
          // 添加教师
          await axios.post('/api/admin/staff/', this.currentStaff)
          this.$message.success('添加成功')
        }
        this.dialogVisible = false
        this.fetchStaff()
      } catch (error) {
        this.$message.error('操作失败')
      }
    },
    handlePageChange(page) {
      this.currentPage = page
      this.fetchStaff()
    }
  }
}
</script>

<style scoped>
.teacher-management {
  padding: 20px;
}

.filter-container {
  margin-bottom: 20px;
}
</style>
