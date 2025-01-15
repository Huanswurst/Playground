<template>
  <div class="class-management">
    <h1>班级管理</h1>
    
    <!-- 搜索和操作区域 -->
    <div class="filter-container">
      <el-form :inline="true">
        <el-form-item>
          <el-input v-model="searchQuery" placeholder="搜索班级名称"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="success" @click="addClass">添加班级</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 班级表格 -->
    <el-table :data="classes" style="width: 100%">
      <el-table-column prop="id" label="ID" width="80"></el-table-column>
      <el-table-column prop="name" label="班级名称"></el-table-column>
      <el-table-column prop="grade" label="年级"></el-table-column>
      <el-table-column prop="major" label="专业"></el-table-column>
      <el-table-column prop="headTeacher" label="班主任"></el-table-column>
      <el-table-column prop="studentCount" label="学生人数"></el-table-column>
      <el-table-column label="操作" width="150">
        <template #default="scope">
          <el-button type="text" size="small" @click="editClass(scope.row)">编辑</el-button>
          <el-button type="text" size="small" @click="deleteClass(scope.row)">删除</el-button>
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

    <!-- 班级编辑对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible">
      <el-form :model="currentClass">
        <el-form-item label="班级名称">
          <el-input v-model="currentClass.name"></el-input>
        </el-form-item>
        <el-form-item label="年级">
          <el-select v-model="currentClass.grade" placeholder="请选择">
            <el-option label="2021级" value="2021级"></el-option>
            <el-option label="2022级" value="2022级"></el-option>
            <el-option label="2023级" value="2023级"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="专业">
          <el-select v-model="currentClass.major" placeholder="请选择">
            <el-option label="计算机科学与技术" value="计算机科学与技术"></el-option>
            <el-option label="软件工程" value="软件工程"></el-option>
            <el-option label="网络空间安全" value="网络空间安全"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="班主任">
          <el-select v-model="currentClass.headTeacher" placeholder="请选择">
            <el-option label="张三" value="张三"></el-option>
            <el-option label="李四" value="李四"></el-option>
            <el-option label="王五" value="王五"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmClass">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: '',
      classes: [
        {
          id: 1,
          name: '计算机1班',
          grade: '2021级',
          major: '计算机科学与技术',
          headTeacher: '张三',
          studentCount: 45
        },
        {
          id: 2,
          name: '软件工程2班',
          grade: '2022级',
          major: '软件工程',
          headTeacher: '李四',
          studentCount: 50
        },
        {
          id: 3,
          name: '网络安全3班',
          grade: '2023级',
          major: '网络空间安全',
          headTeacher: '王五',
          studentCount: 40
        }
      ],
      total: 100,
      pageSize: 10,
      dialogVisible: false,
      dialogTitle: '添加班级',
      currentClass: {
        id: null,
        name: '',
        grade: '',
        major: '',
        headTeacher: '',
        studentCount: 0
      }
    }
  },
  methods: {
    handleSearch() {
      console.log('搜索班级', this.searchQuery)
    },
    addClass() {
      this.currentClass = {
        id: null,
        name: '',
        grade: '',
        major: '',
        headTeacher: '',
        studentCount: 0
      }
      this.dialogTitle = '添加班级'
      this.dialogVisible = true
    },
    editClass(cls) {
      this.currentClass = { ...cls }
      this.dialogTitle = '编辑班级'
      this.dialogVisible = true
    },
    deleteClass(cls) {
      this.$confirm('确定删除该班级吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.classes = this.classes.filter(c => c.id !== cls.id)
      })
    },
    confirmClass() {
      if (this.currentClass.id) {
        // 编辑班级
        const index = this.classes.findIndex(c => c.id === this.currentClass.id)
        this.classes.splice(index, 1, this.currentClass)
      } else {
        // 添加班级
        this.currentClass.id = this.classes.length + 1
        this.classes.push(this.currentClass)
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
.class-management {
  padding: 20px;
}

.filter-container {
  margin-bottom: 20px;
}
</style>
