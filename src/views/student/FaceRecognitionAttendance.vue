<template>
  <el-container>
    <el-header class="dashboard-header">
      <div class="header-content">
        <el-button type="primary" @click="$router.push('/student/attendance')" class="back-button">
          <el-icon><Calendar /></el-icon>
          <span>返回考勤</span>
        </el-button>
        <h1 class="header-title">人脸识别考勤</h1>
      </div>
    </el-header>
      
    <el-main>
      <el-card class="camera-card" shadow="hover">
        <div class="camera-section">
          <video ref="video" autoplay playsinline class="camera-video"></video>
          <canvas ref="canvas" style="display: none;"></canvas>
          <div class="camera-controls">
            <el-button type="primary" @click="switchCamera" class="control-button">
              <el-icon><Switch /></el-icon>
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
</template>

<script setup>
import { Calendar, Switch, Camera } from '@element-plus/icons-vue'
import { ref, onBeforeUnmount } from 'vue'

const mediaStream = ref(null)
const isFrontCamera = ref(false)
const recognitionResult = ref("")
const isLoading = ref(false)
const courseInfo = ref(null)
const attendanceStatus = ref(null)

// 获取课程信息
const fetchCourseInfo = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`${config.apiBaseUrl}${config.apiEndpoints.student.courses}`, {
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json'
      }
    })
    const data = await response.json()
    courseInfo.value = data[0] // 假设学生只有一个当前课程
  } catch (error) {
    console.error('获取课程信息失败:', error)
    recognitionResult.value = "获取课程信息失败，请稍后重试"
  }
}

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
  try {
    isLoading.value = true
    const context = canvas.value.getContext("2d")
    canvas.value.width = video.value.videoWidth
    canvas.value.height = video.value.videoHeight
    context.drawImage(video.value, 0, 0, canvas.value.width, canvas.value.height)
    
    // 提交考勤记录
    const token = localStorage.getItem('token')
    const response = await fetch(`${config.apiBaseUrl}${config.apiEndpoints.student.attendance}`, {
      method: 'POST',
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        course_id: courseInfo.value.id,
        status: 'present',
        recognition_data: canvas.value.toDataURL()
      })
    })
    
    if (!response.ok) throw new Error('考勤提交失败')
    
    recognitionResult.value = "识别成功！考勤已记录"
    attendanceStatus.value = 'present'
  } catch (error) {
    console.error('考勤提交失败:', error)
    recognitionResult.value = "考勤提交失败，请稍后重试"
  } finally {
    isLoading.value = false
  }
}

// 组件挂载时启动摄像头并获取课程信息
startCamera()
fetchCourseInfo()

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

.header-content {
  display: flex;
  align-items: center;
  height: 100%;
  position: relative;
}

.header-title {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

.back-button {
  max-width: 100px;
  max-height: 80px;
  padding: 15px;
  margin-right: 20px;
  background-color: white;
  border-color: white;
  color: #409eff;
}

.back-button .el-icon {
  font-size: 25px;
}

.back-button span {
  font-size: 15px;
}

.header-title {
  font-size: 24px;
  font-weight: bold;
  margin: 0;
  line-height: 60px;
}

.camera-card {
  max-width: 800px;
  margin: 10px auto;
  padding: 10px;
  text-align: center;
}

@media screen and (max-width: 768px) {
  .dashboard-header {
    padding: 0 10px;
  }
  .el-button + .el-button {
  margin-left: 0 !important;
}
  .header-title {
    font-size: 18px;
  }
  
  .back-button {
    max-width: 100px;
    max-height: 80px;
    padding: 15px;
    margin-right: 20px;
    background-color: white;
    border-color: white;
    color: #409eff;
  }
  
  .back-button .el-icon {
    font-size: 16px;
  }
  
  .back-button span {
    font-size: 13px;
  }
  
  .camera-card {
    width: 90%;
    margin: 0 auto;
    padding: 10px;
  }
  
  .camera-video {
    max-width: 100%;
  }
  
  .camera-controls {
    flex-direction: column;
    align-items: center;
    width: 100%;
    margin: 5px 0;
  }
  
  .control-button {
    width: 100%;
    margin-bottom: 10px;
  }
  
  .el-form-item__content {
    flex-direction: column;
    align-items: flex-start;
  }
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
  margin: 10px 0;
}

.control-button {
  width: 160px;
  margin-bottom: 10px !important;
}

.recognition-result {
  margin-top: 20px;
}
</style>
