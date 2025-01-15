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
        <el-sub-menu index="1">
          <template #title>
            <el-icon><calendar /></el-icon>
            <span>考勤管理</span>
          </template>
          <el-menu-item index="1-1" route="/admin/attendance">考勤记录</el-menu-item>
          <el-menu-item index="1-2" route="/admin/attendance/statistics">考勤统计</el-menu-item>
          <el-menu-item index="1-3" route="/admin/attendance/settings">考勤设置</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="2">
          <template #title>
            <el-icon><lock /></el-icon>
            <span>权限管理</span>
          </template>
          <el-menu-item index="2-1" route="/admin/permission/roles">角色管理</el-menu-item>
          <el-menu-item index="2-2" route="/admin/permission/users">用户权限</el-menu-item>
          <el-menu-item index="2-3" route="/admin/permission/audit">权限审计</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="3">
          <template #title>
            <el-icon><document /></el-icon>
            <span>日志管理</span>
          </template>
          <el-menu-item index="3-1" route="/admin/log/login">登录日志</el-menu-item>
          <el-menu-item index="3-2" route="/admin/log/operation">操作日志</el-menu-item>
          <el-menu-item index="3-3" route="/admin/log/error">错误日志</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="4">
          <template #title>
            <el-icon><data-line /></el-icon>
            <span>数据统计</span>
          </template>
          <el-menu-item index="4-1" route="/admin/statistics/attendance">考勤统计</el-menu-item>
          <el-menu-item index="4-2" route="/admin/statistics/course">课程统计</el-menu-item>
          <el-menu-item index="4-3" route="/admin/statistics/user">用户统计</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="5">
          <template #title>
            <el-icon><notebook /></el-icon>
            <span>课程管理</span>
          </template>
          <el-menu-item index="5-1" route="/admin/course/schedule">课程安排</el-menu-item>
          <el-menu-item index="5-2" route="/admin/course/teacher">教师分配</el-menu-item>
          <el-menu-item index="5-3" route="/admin/course/student">学生选课</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="6">
          <template #title>
            <el-icon><school /></el-icon>
            <span>班级管理</span>
          </template>
          <el-menu-item index="6-1" route="/admin/class/student">学生管理</el-menu-item>
          <el-menu-item index="6-2" route="/admin/class/teacher">教师管理</el-menu-item>
          <el-menu-item index="6-3" route="/admin/class/schedule">课表管理</el-menu-item>
        </el-sub-menu>
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
import { Menu as IconMenu, Setting, Expand, Fold, User, Avatar, Document } from '@element-plus/icons-vue'
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
