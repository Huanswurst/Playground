<template>
  <StudentLayout title="地理定位人脸识别考勤">
    <el-card class="attendance-card">
      <template #header>
        <div class="card-header">
          <h2>地理定位人脸识别考勤</h2>
        </div>
      </template>

      <el-form label-width="120px">
        <el-form-item label="当前位置">
          <el-input v-model="location" disabled />
        </el-form-item>
        <el-form-item label="人脸识别">
          <el-button type="primary" @click="startFaceRecognition">
            开始识别
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </StudentLayout>
</template>

<script setup>
import { ref } from 'vue'
import StudentLayout from '@/layouts/StudentLayout.vue'

const location = ref('获取中...')

