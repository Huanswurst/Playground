<template>
  <el-container class="attendance-container">

    <el-header class="attendance-header">
      <h1>我的考勤记录</h1>
    </el-header>

    <el-main>
      <!-- 筛选条件 -->
      <el-form :inline="true" class="filter-form">

        <el-form-item label="日期">
          <el-date-picker
            v-model="filterDate"
            type="date"
            placeholder="选择日期"
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
      <el-table v-if="pagedAttendance.length > 0" :data="pagedAttendance" style="width: 100%" border>
        <el-table-column prop="date" label="日期" sortable :formatter="formatDate" />
        <el-table-column prop="course" label="课程" sortable />
        <el-table-column prop="status" label="状态" sortable>
          <template slot-scope="scope">
            <el-tag :type="getStatusTagType(scope.row.status)">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="checkInTime" label="签到时间" sortable />
        <el-table-column prop="checkOutTime" label="签退时间" sortable />
      </el-table>

      <!-- 无数据提示 -->
      <div v-else class="no-data">
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
      />
    </el-main>

  </el-container>
</template>

<script>
import { saveAs } from 'file-saver';
import * as XLSX from 'xlsx';

export default {
  data() {
    return {
      filterDate: '', // 筛选日期
      filterCourse: '', // 筛选课程
      filterStatus: '', // 筛选状态
      currentPage: 1, // 当前页码
      pageSize: 10, // 每页显示条数
      courses: [
        { courseName: '数学' },
        { courseName: '英语' },
      ],
      attendanceData: [
        {
          date: '2023-10-01',
          course: '数学',
          status: '正常',
          checkInTime: '08:
加载更多
