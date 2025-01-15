<template>
  <el-container>
    <el-aside
      :class="{ 'attendance-sidebar': true, collapsed: isSidebarCollapsed }"
      :style="{ width: isSidebarCollapsed ? '0' : '200px' }"
    >
      <el-menu
        default-active="1"
        class="el-menu-vertical-demo"
        v-if="!isSidebarCollapsed"
      >
        <el-menu-item index="1">
          <el-icon><icon-menu /></el-icon>
          <span>权限管理</span>
        </el-menu-item>
        <el-menu-item index="2">
          <el-icon><setting /></el-icon>
          <span>角色管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    
    <el-container>
      <el-header class="dashboard-header">
        <div class="header-content">
          <el-button
            type="link"
            class="toggle-button"
            @click="toggleSidebar"
            aria-label="Toggle menu"
          >
            <el-icon :size="24">
              <component :is="isSidebarCollapsed ? 'Expand' : 'Fold'" />
            </el-icon>
          </el-button>
          <h1 class="header-title">权限管理系统</h1>
        </div>
      </el-header>
      <el-main>
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
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { Menu as IconMenu, Setting, Expand, Fold } from '@element-plus/icons-vue'
import { ref } from 'vue'
import { ElMessageBox } from 'element-plus'

const isSidebarCollapsed = ref(false)
const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

const roles = ref([
  { id: 1, name: '管理员' },
  { id: 2, name: '教师' },
  { id: 3, name: '学生' }
])

const permissions = ref([
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
])

const defaultProps = ref({
  children: 'children',
  label: 'label'
})

const dialogVisible = ref(false)
const dialogTitle = ref('添加角色')
const currentRole = ref({
  id: null,
  name: ''
})

const addRole = () => {
  currentRole.value = { id: null, name: '' }
  dialogTitle.value = '添加角色'
  dialogVisible.value = true
}

const editRole = (role) => {
  currentRole.value = { ...role }
  dialogTitle.value = '编辑角色'
  dialogVisible.value = true
}

const deleteRole = (role) => {
  ElMessageBox.confirm('确定删除该角色吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    roles.value = roles.value.filter(r => r.id !== role.id)
  })
}

const confirmRole = () => {
  if (currentRole.value.id) {
    // 编辑角色
    const index = roles.value.findIndex(r => r.id === currentRole.value.id)
    roles.value.splice(index, 1, currentRole.value)
  } else {
    // 添加角色
    currentRole.value.id = roles.value.length + 1
    roles.value.push(currentRole.value)
  }
  dialogVisible.value = false
}

const savePermissions = () => {
  const checkedKeys = permissionTree.value.getCheckedKeys()
  console.log('保存权限', checkedKeys)
}
</script>

<style scoped>
.attendance-sidebar {
  transition: width 0.3s ease;
}

.dashboard-header {
  background-color: #409eff;
  color: white;
  border-radius: 8px;
  margin-bottom: 20px;
  padding: 0 20px;
}

.header-content {
  display: flex;
  align-items: center;
  height: 100%;
}

.header-title {
  flex: 1;
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  margin: 0;
}

.toggle-button {
  color: white;
  padding: 0;
  margin-right: 16px;
}

.role-list,
.permission-tree {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
</style>
