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
          <el-button type="primary" @click="handleSearch">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="success" @click="addStudent">添加学生</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 学生表格 -->
    <el-table :data="students" style="width: 100%">
      <el-table-column prop="id" label="ID" width="80"></el-table-column>
      <el-table-column prop="name" label="姓名"></el-table-column>
      <el-table-column prop="studentId" label="学号"></el-table-column>
      <el-table-column prop="gender" label="性别"></el-table-column>
      <el-table-column prop="className" label="所属班级"></el-table-column>
      <el-table-column prop="phone" label="联系方式"></el-table-column>
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
          <el-input v-model="currentStudent.name"></el-input>
        </el-form-item>
        <el-form-item label="学号">
          <el-input v-model="currentStudent.studentId"></el-input>
        </el-form-item>
        <el-form-item label="性别">
          <el-select v-model="currentStudent.gender" placeholder="请选择">
            <el-option label="男" value="男"></el-option>
            <el-option label="女" value="女"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="所属班级">
          <el-select v-model="currentStudent.className" placeholder="请选择">
            <el-option label="计算机1班" value="计算机1班"></el-option>
            <el-option label="软件工程2班" value="软件工程2班"></el-option>
            <el-option label="网络安全3班" value="网络安全3班"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="联系方式">
          <el-input v-model="currentStudent.phone"></el-input>
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
export default {
  data() {
    return {
      searchQuery: '',
      students: [
        {
          id: 1,
          name: '张三',
          studentId: '2021001',
          gender: '男',
          className: '计算机1班',
          phone: '13800138000'
        },
        {
          id: 2,
          name: '李四',
          studentId: '2021002',
          gender: '女',
          className: '软件工程2班',
          phone: '13800138001'
        },
        {
          id: 3,
          name: '王五',
          studentId: '2021003',
          gender: '男',
          className: '网络安全3班',
          phone: '13800138002'
        }
      ],
      total: 100,
      pageSize: 10,
      dialogVisible: false,
      dialogTitle: '添加学生',
      currentStudent: {
        id: null,
        name: '',
        studentId: '',
        gender: '',
        className: '',
        phone: ''
      }
    }
  },
  methods: {
    handleSearch() {
      console.log('搜索学生', this.searchQuery)
    },
    addStudent() {
      this.currentStudent = {
        id: null,
        name: '',
        studentId: '',
        gender: '',
        className: '',
        phone: ''
      }
      this.dialogTitle = '添加学生'
      this.dialogVisible = true
    },
    editStudent(student) {
      this.currentStudent = { ...student }
      this.dialogTitle = '编辑学生'
      this.dialogVisible = true
    },
    deleteStudent(student) {
      this.$confirm('确定删除该学生吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.students = this.students.filter(s => s.id !== student.id)
      })
    },
    confirmStudent() {
      if (this.currentStudent.id) {
        // 编辑学生
        const index = this.students.findIndex(s => s.id === this.currentStudent.id)
        this.students.splice(index, 1, this.currentStudent)
      } else {
        // 添加学生
        this.currentStudent.id = this.students.length + 1
        this.students.push(this.currentStudent)
      }
      this.dialogVisible = false
    },
    handlePageChange(page) {
      console.log('切换页码', page)
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
