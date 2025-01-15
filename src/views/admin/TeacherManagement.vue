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
          <el-button type="primary" @click="handleSearch">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="success" @click="addTeacher">添加教师</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 教师表格 -->
    <el-table :data="teachers" style="width: 100%">
      <el-table-column prop="id" label="ID" width="80"></el-table-column>
      <el-table-column prop="name" label="姓名"></el-table-column>
      <el-table-column prop="teacherId" label="工号"></el-table-column>
      <el-table-column prop="title" label="职称"></el-table-column>
      <el-table-column prop="department" label="所属院系"></el-table-column>
      <el-table-column prop="phone" label="联系方式"></el-table-column>
      <el-table-column label="操作" width="150">
        <template #default="scope">
          <el-button type="text" size="small" @click="editTeacher(scope.row)">编辑</el-button>
          <el-button type="text" size="small" @click="deleteTeacher(scope.row)">删除</el-button>
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
      <el-form :model="currentTeacher">
        <el-form-item label="姓名">
          <el-input v-model="currentTeacher.name"></el-input>
        </el-form-item>
        <el-form-item label="工号">
          <el-input v-model="currentTeacher.teacherId"></el-input>
        </el-form-item>
        <el-form-item label="职称">
          <el-select v-model="currentTeacher.title" placeholder="请选择">
            <el-option label="教授" value="教授"></el-option>
            <el-option label="副教授" value="副教授"></el-option>
            <el-option label="讲师" value="讲师"></el-option>
            <el-option label="助教" value="助教"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="所属院系">
          <el-select v-model="currentTeacher.department" placeholder="请选择">
            <el-option label="计算机学院" value="计算机学院"></el-option>
            <el-option label="软件学院" value="软件学院"></el-option>
            <el-option label="网络空间安全学院" value="网络空间安全学院"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="联系方式">
          <el-input v-model="currentTeacher.phone"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmTeacher">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: '',
      teachers: [
        {
          id: 1,
          name: '张三',
          teacherId: '1001',
          title: '教授',
          department: '计算机学院',
          phone: '13800138000'
        },
        {
          id: 2,
          name: '李四',
          teacherId: '1002',
          title: '副教授',
          department: '软件学院',
          phone: '13800138001'
        },
        {
          id: 3,
          name: '王五',
          teacherId: '1003',
          title: '讲师',
          department: '网络空间安全学院',
          phone: '13800138002'
        }
      ],
      total: 100,
      pageSize: 10,
      dialogVisible: false,
      dialogTitle: '添加教师',
      currentTeacher: {
        id: null,
        name: '',
        teacherId: '',
        title: '',
        department: '',
        phone: ''
      }
    }
  },
  methods: {
    handleSearch() {
      console.log('搜索教师', this.searchQuery)
    },
    addTeacher() {
      this.currentTeacher = {
        id: null,
        name: '',
        teacherId: '',
        title: '',
        department: '',
        phone: ''
      }
      this.dialogTitle = '添加教师'
      this.dialogVisible = true
    },
    editTeacher(teacher) {
      this.currentTeacher = { ...teacher }
      this.dialogTitle = '编辑教师'
      this.dialogVisible = true
    },
    deleteTeacher(teacher) {
      this.$confirm('确定删除该教师吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.teachers = this.teachers.filter(t => t.id !== teacher.id)
      })
    },
    confirmTeacher() {
      if (this.currentTeacher.id) {
        // 编辑教师
        const index = this.teachers.findIndex(t => t.id === this.currentTeacher.id)
        this.teachers.splice(index, 1, this.currentTeacher)
      } else {
        // 添加教师
        this.currentTeacher.id = this.teachers.length + 1
        this.teachers.push(this.currentTeacher)
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
.teacher-management {
  padding: 20px;
}

.filter-container {
  margin-bottom: 20px;
}
</style>
