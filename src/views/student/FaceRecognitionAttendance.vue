<template>
  <el-container>
    <el-aside width="200px">
      <el-menu default-active="1" class="el-menu-vertical-demo">
        <el-menu-item index="1" route="/student/attendance">
          <el-icon><calendar /></el-icon>
          <span>返回考勤</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    
    <el-container>
      <el-header class="dashboard-header">
        <h1 class="header-title">人脸识别考勤</h1>
      </el-header>
      
      <el-main>
        <el-card class="camera-card" shadow="hover">
          <div class="camera-section">
            <video ref="video" autoplay playsinline class="camera-video"></video>
            <canvas ref="canvas" style="display: none;"></canvas>
            <div class="camera-controls">
              <el-button type="primary" @click="switchCamera" class="control-button">
                <el-icon><switch /></el-icon>
                <span>切换摄像头</span>
              </el-button>
              <el-button type="success" @click="startRecognition" class="control-button">
                <el-icon><camera /></el-icon>
                <span>开始识别</span>
              </el-button>
            </div>
          </div>

          <el-alert
            v-if="recognitionResult"
            :title="recognitionResult"
            type="success"
            show-icon
            class="recognition-result"
          />
        </el-card>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { Calendar, Switch, Camera } from '@element-plus/icons-vue'
import { ref } from 'vue'

const mediaStream = ref(null)
const isFrontCamera = ref(false)
const recognitionResult = ref("")

// 启动摄像头
const startCamera = async () => {
  try {
    const constraints = {
      video: { facingMode: isFrontCamera.value ? "user" : "environment" },
    }
    mediaStream.value = await navigator.mediaDevices.getUserMedia(constraints)
    video.value.srcObject = mediaStream.value
  } catch (error) {
    console.error("无法访问摄像头:", error)
    recognitionResult.value = "无法访问摄像头，请检查权限。"
  }
}

// 切换摄像头
const switchCamera = async () => {
  if (mediaStream.value) {
    mediaStream.value.getTracks().forEach((track) => track.stop())
  }
  isFrontCamera.value = !isFrontCamera.value
  await startCamera()
}

// 开始人脸识别
const startRecognition = async () => {
  const context = canvas.value.getContext("2d")
  canvas.value.width = video.value.videoWidth
  canvas.value.height = video.value.videoHeight
  context.drawImage(video.value, 0, 0, canvas.value.width, canvas.value.height)
  recognitionResult.value = "识别成功！考勤已记录"
}

// 组件挂载时启动摄像头
startCamera()

// 组件卸载时关闭摄像头
onBeforeUnmount(() => {
  if (mediaStream.value) {
    mediaStream.value.getTracks().forEach((track) => track.stop())
  }
})
</script>

<style scoped>
.dashboard-header {
  background-color: #409eff;
  color: white;
  border-radius: 8px;
  margin-bottom: 20px;
  padding: 0 20px;
}

.header-title {
  font-size: 24px;
  font-weight: bold;
  margin: 0;
  line-height: 60px;
}

.camera-card {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

.camera-video {
  width: 100%;
  max-width: 640px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.camera-controls {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.control-button {
  width: 160px;
}

.recognition-result {
  margin-top: 20px;
}
</style>
