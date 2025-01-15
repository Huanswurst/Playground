<template>
  <div class="course-management">
    <h1>课程管理</h1>
    
    <!-- 搜索和操作区域 -->
    <div class="filter-container">
      <el-form :inline="true">
        <el-form-item>
          <el-input v-model="searchQuery" placeholder="搜索课程名称或代码"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="success" @click="addCourse">添加课程</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 课程表格 -->
    <el-table :data="courses" style="width: 100%">
      <el-table-column prop="id" label="ID" width="80"></el-table-column>
      <el-table-column prop="name" label="课程名称"></el-table-column>
      <el-table-column prop="code" label="课程代码"></el-table-column>
      <el-table-column prop="credit" label="学分"></el-table-column>
      <el-table-column prop="teacher" label="授课教师"></el-table-column>
      <el-table-column prop="time" label="上课时间"></el-table-column>
      <el-table-column label="操作" width="150">
        <template #default="scope">
          <el-button type="text" size="small" @click="editCourse(scope.row)">编辑</el-button>
          <el-button type="text" size="small" @click="deleteCourse(scope.row)">删除</el-button>
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

    <!-- 课程编辑对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible">
      <el-form :model="currentCourse">
        <el-form-item label="课程名称">
          <el-input v-model="currentCourse.name"></el-input>
        </el-form-item>
        <el-form-item label="课程代码">
          <el-input v-model="currentCourse.code"></el-input>
        </el-form-item>
        <el-form-item label="学分">
          <el-input-number v-model="currentCourse.credit" :min="1" :max="10"></el-input-number>
        </el-form-item>
        <el-form-item label="授课教师">
          <el-select v-model="currentCourse.teacher" placeholder="请选择">
            <el-option label="张三" value="张三"></el-option>
            <el-option label="李四" value="李四"></el-option>
            <el-option label="王五" value="王五"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="上课时间">
          <el-time-picker
            v-model="currentCourse.time"
            format="HH:mm"
            value-format="HH:mm"
            placeholder="选择时间"
          ></el-time-picker>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmCourse">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: '',
      courses: [
        {
          id: 1,
          name: '数据结构',
          code: 'CS101',
          credit: 3,
          teacher: '张三',
          time: '08:00'
        },
        {
          id: 2,
          name: '操作系统',
          code: 'CS102',
          credit: 4,
          teacher: '李四',
          time: '10:00'
        },
        {
          id: 3,
          name: '计算机网络',
          code: 'CS103',
          credit: 3,
          teacher: '王五',
          time: '14:00'
        }
      ],
      total: 100,
      pageSize: 10,
      dialogVisible: false,
      dialogTitle: '添加课程',
      currentCourse: {
        id: null,
        name: '',
        code: '',
        credit: 1,
        teacher: '',
        time: ''
      }
    }
  },
  methods: {
    handleSearch() {
      console.log('搜索课程', this.searchQuery)
    },
    addCourse() {
      this.currentCourse = {
        id: null,
        name: '',
        code: '',
        credit: 1,
        teacher: '',
        time: ''
      }
      this.dialogTitle = '添加课程'
      this.dialogVisible = true
    },
    editCourse(course) {
      this.currentCourse = { ...course }
      this.dialogTitle = '编辑课程'
      this.dialogVisible = true
    },
    deleteCourse(course) {
      this.$confirm('确定删除该课程吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.courses = this.courses.filter(c => c.id !== course.id)
      })
    },
    confirmCourse() {
      if (this.currentCourse.id) {
        // 编辑课程
        const index = this.courses.findIndex(c => c.id === this.currentCourse.id)
        this.courses.splice(index, 1, this.currentCourse)
      } else {
        // 添加课程
        this.currentCourse.id = this.courses.length + 1
        this.courses.push(this.currentCourse)
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
.course-management {
  padding: 20px;
}

.filter-container {
  margin-bottom: 20px;
}
</style>
