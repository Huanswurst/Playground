<template>
  <div class="permission-management">
    <h1>权限管理</h1>
    
    <el-row :gutter="20">
      <el-col :span="8">
        <div class="role-list">
          <h3>角色列表</h3>
          <el-table :data="roles" style="width: 100%">
            <el-table-column prop="name" label="角色名称"></el-table-column>
            <el-table-column label="操作" width="120">
              <template #default="scope">
                <el-button type="text" size="small" @click="editRole(scope.row)">编辑</el-button>
                <el-button type="text" size="small" @click="deleteRole(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <div style="margin-top: 20px">
            <el-button type="primary" @click="addRole">添加角色</el-button>
          </div>
        </div>
      </el-col>
      <el-col :span="16">
        <div class="permission-tree">
          <h3>权限分配</h3>
          <el-tree
            ref="permissionTree"
            :data="permissions"
            show-checkbox
            node-key="id"
            :default-expand-all="true"
            :props="defaultProps"
          ></el-tree>
          <div style="margin-top: 20px">
            <el-button type="primary" @click="savePermissions">保存权限</el-button>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 角色编辑对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible">
      <el-form :model="currentRole">
        <el-form-item label="角色名称">
          <el-input v-model="currentRole.name"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmRole">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      roles: [
        { id: 1, name: '管理员' },
        { id: 2, name: '教师' },
        { id: 3, name: '学生' }
      ],
      permissions: [
        {
          id: 1,
          label: '系统管理',
          children: [
            { id: 11, label: '用户管理' },
            { id: 12, label: '角色管理' },
            { id: 13, label: '权限管理' }
          ]
        },
        {
          id: 2,
          label: '考勤管理',
          children: [
            { id: 21, label: '考勤记录' },
            { id: 22, label: '考勤统计' },
            { id: 23, label: '考勤设置' }
          ]
        },
        {
          id: 3,
          label: '课程管理',
          children: [
            { id: 31, label: '课程列表' },
            { id: 32, label: '课程安排' },
            { id: 33, label: '课程统计' }
          ]
        }
      ],
      defaultProps: {
        children: 'children',
        label: 'label'
      },
      dialogVisible: false,
      dialogTitle: '添加角色',
      currentRole: {
        id: null,
        name: ''
      }
    }
  },
  methods: {
    addRole() {
      this.currentRole = { id: null, name: '' }
      this.dialogTitle = '添加角色'
      this.dialogVisible = true
    },
    editRole(role) {
      this.currentRole = { ...role }
      this.dialogTitle = '编辑角色'
      this.dialogVisible = true
    },
    deleteRole(role) {
      this.$confirm('确定删除该角色吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.roles = this.roles.filter(r => r.id !== role.id)
      })
    },
    confirmRole() {
      if (this.currentRole.id) {
        // 编辑角色
        const index = this.roles.findIndex(r => r.id === this.currentRole.id)
        this.roles.splice(index, 1, this.currentRole)
      } else {
        // 添加角色
        this.currentRole.id = this.roles.length + 1
        this.roles.push(this.currentRole)
      }
      this.dialogVisible = false
    },
    savePermissions() {
      const checkedKeys = this.$refs.permissionTree.getCheckedKeys()
      console.log('保存权限', checkedKeys)
    }
  }
}
</script>

<style scoped>
.permission-management {
  padding: 20px;
}

.role-list,
.permission-tree {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
</style>
