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
          <video ref="video" autoplay playsinline muted class="camera-video"></video>
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
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { Calendar, Switch, Camera } from '@element-plus/icons-vue'
import * as faceapi from 'face-api.js'

// 配置常量
const config = {
  apiBaseUrl: 'https://your-api-domain.com/api/v1',
  apiEndpoints: {
    student: {
      courses: '/student/courses/',
      attendance: '/student/attendance/'
    }
  }
}

const video = ref(null)
const canvas = ref(null)
const overlay = ref(null)

const mediaStream = ref(null)
const currentCameraIndex = ref(0)
const cameraDevices = ref([])
const recognitionResult = ref("")
let detectionTimeoutId = null

// 加载 face-api.js 模型
const loadFaceApiModels = async () => {
  const modelUrl = '/models'
  try {
    await faceapi.nets.tinyFaceDetector.loadFromUri(modelUrl)
    await faceapi.nets.faceLandmark68Net.loadFromUri(modelUrl)
  } catch (error) {
    recognitionResult.value = "加载模型失败：" + (error.message || error)
    console.error("加载模型错误：", error)
  }
}

// 获取摄像头设备列表
const getCameraDevices = async () => {
  try {
    const devices = await navigator.mediaDevices.enumerateDevices()
    cameraDevices.value = devices.filter(device => device.kind === 'videoinput')
    if (cameraDevices.value.length === 0) {
      recognitionResult.value = "未检测到摄像头设备"
    }
  } catch (error) {
    recognitionResult.value = "获取摄像头设备失败：" + error.message
  }
}

// 摄像头错误处理函数
const handleCameraError = (error) => {
  console.error("Camera error:", error)
  recognitionResult.value = "打开摄像头失败：" + (error.message || error)
}

// 启动摄像头
const startCamera = async () => {
  try {
    // 检查是否为安全连接（HTTPS 或 localhost 下允许摄像头访问）
    if (location.protocol !== 'https:' && location.hostname !== 'localhost') {
      recognitionResult.value = "请使用HTTPS或localhost访问以启用摄像头功能"
      return
    }
    
    if (!navigator.mediaDevices?.getUserMedia) {
      recognitionResult.value = "您的浏览器不支持摄像头访问"
      return
    }
    
    const deviceId = cameraDevices.value[currentCameraIndex.value]?.deviceId
    const constraints = {
      video: { 
        deviceId: deviceId ? { exact: deviceId } : undefined,
        width: { ideal: 1280 },
        height: { ideal: 720 }
      }
    }

    mediaStream.value = await navigator.mediaDevices.getUserMedia(constraints)
    video.value.srcObject = mediaStream.value
    
    // 视频加载完成后处理逻辑
    video.value.onloadedmetadata = () => {
      adjustCanvasSize()
      video.value.play()
      detectFrame() // 启动检测循环
    }
  } catch (error) {
    handleCameraError(error)
  }
}

// 调整画布尺寸（处理设备像素比）
const adjustCanvasSize = () => {
  if (!video.value) return
  const videoWidth = video.value.videoWidth
  const videoHeight = video.value.videoHeight
  if (overlay.value && canvas.value) {
    // 设置实际画布尺寸（像素级）
    overlay.value.width = videoWidth
    overlay.value.height = videoHeight
    canvas.value.width = videoWidth
    canvas.value.height = videoHeight

    // 设置 CSS 显示尺寸
    overlay.value.style.width = `${video.value.clientWidth}px`
    overlay.value.style.height = `${video.value.clientHeight}px`
  }
}

// 切换摄像头
const switchCamera = async () => {
  currentCameraIndex.value = (currentCameraIndex.value + 1) % cameraDevices.value.length
  if (mediaStream.value) {
    mediaStream.value.getTracks().forEach(track => track.stop())
  }
  await startCamera()
}

// 人脸检测循环，降低检测频率（200ms 后检测一次）
const detectFrame = async () => {
  if (!video.value || video.value.readyState !== 4) {
    scheduleNextDetection()
    return
  }
  
  try {
    // 使用 withFaceLandmarks() 返回人脸检测及关键点
    const detections = await faceapi.detectAllFaces(
      video.value,
      new faceapi.TinyFaceDetectorOptions({ inputSize: 320 })
    ).withFaceLandmarks()
    
    drawDetectionBox(detections)
  } catch (error) {
    console.error("检测错误：", error)
  }
  
  scheduleNextDetection()
}

// 调度下一次检测
const scheduleNextDetection = () => {
  detectionTimeoutId = setTimeout(() => {
    detectFrame()
  }, 200)
}

// 绘制检测框：调整位置使得红框中央偏上，靠近鼻子
const drawDetectionBox = (detections) => {
  if (!overlay.value) return
  const ctx = overlay.value.getContext("2d")
  ctx.clearRect(0, 0, overlay.value.width, overlay.value.height)
  
  if (detections.length > 0) {
    const resizedDetections = faceapi.resizeResults(
      detections,
      { width: overlay.value.width, height: overlay.value.height }
    )
    
    resizedDetections.forEach(det => {
      const box = det.detection.box
      // 以80%缩放显示红框
      const factor = 0.8
      const newWidth = box.width * factor
      const newHeight = box.height * factor
      // 计算新的 x 坐标（水平居中）
      const newX = box.x + (box.width - newWidth) / 2
      // 计算新的 y 坐标，向上偏移一定比例，默认上移15%的box高度
      const offset = 0.15 * box.height
      const newY = box.y + (box.height - newHeight) / 2 - offset
      
      ctx.beginPath()
      ctx.lineWidth = 4
      ctx.strokeStyle = "red"
      ctx.rect(newX, newY, newWidth, newHeight)
      ctx.stroke()

      ctx.font = 'bold 24px Arial'
      ctx.fillStyle = 'red'
      ctx.fillText(`匹配度: ${(det.detection.score * 100).toFixed(1)}%`, newX + 5, newY - 10)
    })
  }
}

// 开始人脸识别（示例功能）
const startRecognition = async () => {
  recognitionResult.value = "正在识别，请稍候..."
  // 此处可加入调用 API 进行人脸识别的逻辑；以下为模拟效果
  setTimeout(() => {
    recognitionResult.value = "识别成功：学生信息匹配"
  }, 2000)
}

onMounted(async () => {
  await loadFaceApiModels()
  await getCameraDevices()
  await startCamera()
  window.addEventListener('resize', adjustCanvasSize)
})

onBeforeUnmount(() => {
  if (detectionTimeoutId) clearTimeout(detectionTimeoutId)
  if (mediaStream.value) {
    mediaStream.value.getTracks().forEach(track => track.stop())
  }
  window.removeEventListener('resize', adjustCanvasSize)
})
</script>

<style scoped>
/* 页面整体样式，与其他页面保持一致 */
.dashboard-header {
  background-color: #f5f5f5;
  padding: 16px;
  border-bottom: 1px solid #e0e0e0;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-title {
  margin: 0;
  font-size: 24px;
}

/* 摄像头卡片样式 */
.camera-card {
  margin: 24px auto;
  max-width: 800px;
  padding: 16px;
  position: relative;
}

.camera-section {
  position: relative;
  text-align: center;
}

.camera-video {
  width: 100%;
  max-width: 640px;
  height: auto;
  aspect-ratio: 4 / 3;
}

.overlay-canvas {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: auto;
  aspect-ratio: 4 / 3;
  pointer-events: none;
}

.camera-controls {
  margin-top: 16px;
  display: flex;
  justify-content: center;
  gap: 16px;
}

.control-button {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 针对手机屏幕的适配 */
@media screen and (max-width: 768px) {
  .overlay-canvas {
    aspect-ratio: 9 / 16;
  }
}
</style>
