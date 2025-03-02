<template>
  <el-container>
    <el-header class="dashboard-header">
      <div class="header-content">
        <h1 class="header-title">学生管理</h1>
        <el-button
          type="danger"
          class="logout-button"
          @click="handleLogout"
          style="margin-left: 15px"
        >
          退出登录
        </el-button>
      </div>
    </el-header>
    <div class="student-management">
    <el-row :gutter="20" class="mb-20">
      <el-col :span="12">
        <el-input
          v-model="searchQuery"
          placeholder="搜索学生姓名或学号"
          clearable
          @clear="handleSearch"
          @input="handleSearch"
        />
      </el-col>
      <el-col :span="12" class="text-right">
        <el-button type="primary" @click="handleAddStudent">添加学生</el-button>
      </el-col>
    </el-row>

    <!-- 学生列表 -->
    <el-table
      :data="filteredStudents"
      stripe
      style="width: 100%"
      v-loading="loading"
    >
      <el-table-column prop="studentNumber" label="学号" sortable />
      <el-table-column prop="name" label="姓名" sortable />
      <el-table-column prop="attendanceRate" label="出勤率" sortable>
        <template #default="{ row }">
          <el-progress
            :percentage="row.attendanceRate"
            :status="getAttendanceStatus(row.attendanceRate)"
          />
        </template>
      </el-table-column>
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <el-button type="danger" size="small" @click="handleRemoveStudent(row)">移除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加学生对话框 -->
    <el-dialog
      v-model="addStudentDialogVisible"
      title="添加学生"
      width="30%"
    >
      <el-form
        ref="addStudentForm"
        :model="addStudentForm"
        label-width="80px"
        :rules="addStudentRules"
      >
        <el-form-item label="学号" prop="studentNumber">
          <el-input
            v-model="addStudentForm.studentNumber"
            placeholder="请输入学生学号"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="addStudentDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleConfirmAddStudent">确认</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
  </el-container>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const handleLogout = () => {
  router.push('/login')
}

const props = defineProps({
  course: {
    type: Object,
    required: true
  }
})

const searchQuery = ref('')
const loading = ref(false)
const students = ref([])
const addStudentDialogVisible = ref(false)
const addStudentForm = ref({
  studentNumber: ''
})

const addStudentRules = ref({
  studentNumber: [
    { required: true, message: '请输入学生学号', trigger: 'blur' }
  ]
})

// 计算属性
const filteredStudents = computed(() => {
  return students.value.filter(student => {
    return student.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      student.studentNumber.toLowerCase().includes(searchQuery.value.toLowerCase())
  })
})

// 获取课程学生列表
const fetchStudents = async () => {
  try {
    loading.value = true
    const response = await axios.get(`/api/get_course_students/${props.course.id}/`)
    students.value = response.data
  } catch (error) {
    ElMessage.error('获取学生列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  // 搜索逻辑已在 computed 中实现
}

const handleAddStudent = () => {
  addStudentDialogVisible.value = true
}

const handleConfirmAddStudent = async () => {
  try {
    await axios.post('/api/add_student_to_course/', {
      course_id: props.course.id,
      student_number: addStudentForm.value.studentNumber
    })
    ElMessage.success('添加学生成功')
    addStudentDialogVisible.value = false
    await fetchStudents()
  } catch (error) {
    ElMessage.error(error.response?.data?.error || '添加学生失败')
  }
}

const handleRemoveStudent = async (student) => {
  try {
    await axios.post('/api/remove_student_from_course/', {
      course_id: props.course.id,
      student_id: student.id
    })
    ElMessage.success('移除学生成功')
    await fetchStudents()
  } catch (error) {
    ElMessage.error(error.response?.data?.error || '移除学生失败')
  }
}

const getAttendanceStatus = (rate) => {
  if (rate >= 90) return 'success'
  if (rate >= 80) return 'warning'
  return 'exception'
}

// 监听课程变化
watch(() => props.course, () => {
  fetchStudents()
}, { immediate: true })
</script>

<style scoped>
.student-management {
  padding: 20px;
}

.mb-20 {
  margin-bottom: 20px;
}

.text-right {
  text-align: right;
}
</style>
