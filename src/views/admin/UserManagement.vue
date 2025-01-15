<template>
  <div class="user-management">
    <h1>用户管理</h1>
    <!-- 用户列表 -->
    <div class="user-list">
      <el-table :data="userList" style="width: 100%">
        <el-table-column prop="username" label="用户名"></el-table-column>
        <el-table-column prop="role" label="角色"></el-table-column>
        <el-table-column prop="status" label="状态"></el-table-column>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 添加用户 -->
    <el-button type="primary" @click="dialogVisible = true">添加用户</el-button>

    <el-dialog v-model="dialogVisible" title="添加用户">
      <el-form :model="newUser" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="newUser.username"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="newUser.password" type="password"></el-input>
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="newUser.role" placeholder="请选择角色">
            <el-option label="管理员" value="admin"></el-option>
            <el-option label="教师" value="teacher"></el-option>
            <el-option label="学生" value="student"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleAddUser">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userList: [
        { username: 'admin1', role: '管理员', status: '正常' },
        { username: 'teacher1', role: '教师', status: '正常' },
        { username: 'student1', role: '学生', status: '正常' }
      ],
      dialogVisible: false,
      newUser: {
        username: '',
        password: '',
        role: ''
      }
    }
  },
  methods: {
    handleEdit(user) {
      // 编辑用户逻辑
      console.log('编辑用户', user)
    },
    handleDelete(user) {
      // 删除用户逻辑
      console.log('删除用户', user)
    },
    handleAddUser() {
      // 添加用户逻辑
      console.log('添加用户', this.newUser)
      this.dialogVisible = false
    }
  }
}
</script>

<style scoped>
.user-management {
  padding: 20px;
}
</style>
