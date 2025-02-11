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
          <!-- 叠加的 canvas -->
          <canvas ref="overlay" class="overlay-canvas"></canvas>
          <canvas ref="canvas" style="display: none;"></canvas>
          <div class="camera-controls">
            <el-button type="primary" @click="switchCamera" class="control-button">
              <el-icon><Switch /></el-icon>
              <span>切换摄像头</span>
            </el-button>
            <el-button type="success" @click="startRecognition" class="control-button">
              <el-icon><Camera /></el-icon>
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
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { Calendar, Switch, Camera } from '@element-plus/icons-vue'
import * as faceapi from 'face-api.js'

const video = ref(null)
const canvas = ref(null)
const overlay = ref(null)

const mediaStream = ref(null)
const isFrontCamera = ref(false)
const recognitionResult = ref("")
const isLoading = ref(false)
const courseInfo = ref(null)
const attendanceStatus = ref(null)
let detectionTimer = null

// 加载 face-api.js 模型
const loadFaceApiModels = async () => {
  const modelUrl = '/models'
  await faceapi.nets.tinyFaceDetector.loadFromUri(modelUrl)
}

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
    courseInfo.value = data[0]
  } catch (error) {
    console.error('获取课程信息失败:', error)
    recognitionResult.value = "获取课程信息失败，请稍后重试"
  }
}

// 启动摄像头
const startCamera = async () => {
  try {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      recognitionResult.value = "您的浏览器不支持摄像头访问"
      return
    }
    if (window.location.protocol !== 'https:' && window.location.hostname !== 'localhost') {
      recognitionResult.value = "请确保在HTTPS环境下访问"
      return
    }
    const constraints = {
      video: { 
        facingMode: isFrontCamera.value ? "user" : "environment",
        width: { ideal: 1280 },
        height: { ideal: 720 }
      },
    }
    mediaStream.value = await navigator.mediaDevices.getUserMedia(constraints)
    video.value.srcObject = mediaStream.value
    mediaStream.value.getVideoTracks()[0].onended = () => {
      recognitionResult.value = "摄像头连接已断开"
    }
    // 等待视频元数据加载完成
    video.value.onloadedmetadata = () => {
      video.value.play()
    }
  } catch (error) {
    console.error("无法访问摄像头:", error)
    let errorMessage = "无法访问摄像头"
    if (error.name === 'NotAllowedError') {
      errorMessage = "请允许摄像头访问权限"
    } else if (error.name === 'NotFoundError') {
      errorMessage = "未找到可用的摄像头设备"
    } else if (error.name === 'NotReadableError') {
      errorMessage = "摄像头已被其他应用占用"
    } else if (error.name === 'OverconstrainedError') {
      errorMessage = "无法满足摄像头配置要求"
    }
    recognitionResult.value = errorMessage
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

// 实时人脸检测（采用自适应大小，适合移动端）
const detectFace = async () => {
  if (!video.value || video.value.readyState !== 4) return

  // 使用 clientWidth/clientHeight 来适配当前屏幕尺寸
  const videoWidth = video.value.clientWidth
  const videoHeight = video.value.clientHeight
  overlay.value.width = videoWidth
  overlay.value.height = videoHeight
  const displaySize = { width: videoWidth, height: videoHeight }
  
  const detections = await faceapi.detectAllFaces(video.value, new faceapi.TinyFaceDetectorOptions())
  const ctx = overlay.value.getContext("2d")
  ctx.clearRect(0, 0, overlay.value.width, overlay.value.height)
  
  if (detections.length > 0) {
    const resizedDetections = faceapi.resizeResults(detections, displaySize)
    resizedDetections.forEach(det => {
      const box = det.box
      ctx.beginPath()
      ctx.lineWidth = 4
      ctx.strokeStyle = "red"
      ctx.rect(box.x, box.y, box.width, box.height)
      ctx.stroke()
      const matchScore = (det.score * 100).toFixed(2) + '%'
      ctx.font = '18px Arial'
      ctx.fillStyle = 'red'
      ctx.fillText("匹配度：" + matchScore, box.x, box.y - 10)
    })
    recognitionResult.value = "人脸识别成功！"
  } else {
    recognitionResult.value = "未检测到人脸"
  }
}

// 开始人脸识别并提交考勤记录
const startRecognition = async () => {
  try {
    isLoading.value = true
    await nextTick()  // 确保最新尺寸已更新
    const ctx = canvas.value.getContext("2d")
    canvas.value.width = video.value.clientWidth
    canvas.value.height = video.value.clientHeight
    ctx.drawImage(video.value, 0, 0, canvas.value.width, canvas.value.height)
    
    await detectFace()
    
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
    
    recognitionResult.value += "，考勤已记录"
    attendanceStatus.value = 'present'
  } catch (error) {
    console.error('考勤提交失败:', error)
    recognitionResult.value = "考勤提交失败，请稍后重试"
  } finally {
    isLoading.value = false
  }
}

onMounted(async () => {
  await loadFaceApiModels()
  await startCamera()
  fetchCourseInfo()
  detectionTimer = setInterval(detectFace, 1000)
})

onBeforeUnmount(() => {
  if (detectionTimer) clearInterval(detectionTimer)
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
  font-size: 24px;
  font-weight: bold;
  margin: 0;
  line-height: 60px;
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

.camera-card {
  max-width: 800px;
  margin: 10px auto;
  padding: 10px;
  text-align: center;
}

.camera-section {
  position: relative;
}

/* 设置视频宽度占满父容器，自动适应移动端 */
.camera-video {
  width: 100%;
  max-width: 640px;
  border-radius: 8px;
  margin-bottom: 20px;
}

/* overlay 画布与视频重合 */
.overlay-canvas {
  position: absolute;
  top: 0;
  left: 0;
  pointer-events: none;
  z-index: 10;
}

/* 控制按钮样式 */
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

/* 响应式样式 */
@media screen and (max-width: 768px) {
  .header-title {
    font-size: 18px;
  }
  .back-button {
    max-width: 80px;
    max-height: 60px;
    padding: 10px;
    margin-right: 15px;
  }
  .back-button .el-icon {
    font-size: 16px;
  }
  .back-button span {
    font-size: 12px;
  }
  .camera-card {
    width: 90%;
    margin: 0 auto;
    padding: 10px;
  }
  .camera-video {
    max-width: 100%;
  }
  .control-button {
    width: 100%;
    margin-bottom: 10px;
  }
}
</style>