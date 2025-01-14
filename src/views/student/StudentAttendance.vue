<template>
  <el-container class="attendance-container">
    <!-- 侧边栏 -->
    <el-aside
      :width="isSidebarCollapsed ? '60px' : '200px'"
      class="attendance-sidebar"
    >
      <el-menu
        :default-active="activeMenu"
        class="el-menu-vertical-demo"
        @select="handleMenuSelect"
      >
        <el-menu-item index="1">
          <i class="el-icon-menu"></i>
          <span class="menu-text" v-if="!isSidebarCollapsed">首页</span>
        </el-menu-item>
        <el-menu-item index="2">
          <i class="el-icon-document"></i>
          <span class="menu-text" v-if="!isSidebarCollapsed">考勤记录</span>
        </el-menu-item>
        <!-- 根据需要添加更多菜单项 -->
      </el-menu>
    </el-aside>

    <!-- 主体部分 -->
    <el-container>
      <el-header class="attendance-header">
        <!-- Toggle Menu 按钮 -->
        <el-button
          type="link"
          class="toggle-button"
          @click="toggleSidebar"
          aria-label="Toggle menu"
        >
          <i :class="isSidebarCollapsed ? 'el-icon-s-unfold' : 'el-icon-s-fold'"></i>
        </el-button>
        <h1 class="header-title">我的考勤记录</h1>
      </el-header>

      <!-- 使用 v-loading 指令绑定到 el-main -->
      <el-main v-loading="loading">
        <!-- 筛选条件 -->
        <el-form :inline="true" class="filter-form">
          <el-form-item label="日期范围">
            <el-date-picker
              v-model="filterDateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              value-format="yyyy-MM-dd"
            />
          </el-form-item>

          <el-form-item label="课程">
            <el-select v-model="filterCourse" placeholder="选择课程">
              <el-option label="全部" value="" />
              <el-option
                v-for="course in courses"
                :key="course.courseName"
                :label="course.courseName"
                :value="course.courseName"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="状态">
            <el-select v-model="filterStatus" placeholder="选择状态">
              <el-option label="全部" value="" />
              <el-option label="正常" value="正常" />
              <el-option label="迟到" value="迟到" />
              <el-option label="缺勤" value="缺勤" />
            </el-select>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button type="success" @click="handleExport">导出数据</el-button>
          </el-form-item>
        </el-form>

        <!-- 考勤表格 -->
        <el-table
          v-if="pagedAttendance.length > 0"
          :data="pagedAttendance"
          style="width: 100%"
          border
        >
          <el-table-column
            prop="date"
            label="日期"
            sortable
            :formatter="formatDate"
          />
          <el-table-column prop="course" label="课程" sortable />
          <el-table-column prop="status" label="状态" sortable>
            <template #default="scope">
              <el-tag :type="getStatusTagType(scope.row.status)">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="checkInTime" label="签到时间" sortable />
          <el-table-column prop="checkOutTime" label="签退时间" sortable />
        </el-table>

        <!-- 空数据提示 -->
        <div v-else class="no-data" v-if="!loading">
          <p>没有符合条件的考勤记录。</p>
        </div>

        <!-- 分页 -->
        <el-pagination
          class="pagination"
          :current-page="currentPage"
          :page-size="pageSize"
          :total="filteredAttendance.length"
          @current-change="handlePageChange"
          layout="total, prev, pager, next"
          background
          v-if="filteredAttendance.length > pageSize"
        />
      </el-main>
    </el-container>
  </el-container>
</template>
