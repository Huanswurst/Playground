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
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
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
const isLoading = ref(false)
const courseInfo = ref(null)
const attendanceStatus = ref(null)
let animationFrameId = null

// 加载 face-api.js 模型
const loadFaceApiModels = async () => {
  const modelUrl = import.meta.env.DEV ? '/models' : './models'
  await faceapi.nets.tinyFaceDetector.loadFromUri(modelUrl)
  await faceapi.nets.faceLandmark68Net.loadFromUri(modelUrl)
}

// 获取摄像头设备列表
const getCameraDevices = async () => {
  const devices = await navigator.mediaDevices.enumerateDevices()
  cameraDevices.value = devices.filter(device => device.kind === 'videoinput')
}

// 启动摄像头
const startCamera = async () => {
  try {
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
    
    // 处理视频方向适配
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
  const dpr = window.devicePixelRatio || 1
  const videoWidth = video.value.videoWidth
  const videoHeight = video.value.videoHeight

  // 设置实际画布尺寸
  overlay.value.width = videoWidth
  overlay.value.height = videoHeight
  canvas.value.width = videoWidth
  canvas.value.height = videoHeight

  // 设置CSS显示尺寸
  overlay.value.style.width = `${video.value.clientWidth}px`
  overlay.value.style.height = `${video.value.clientHeight}px`
}

// 切换摄像头
const switchCamera = async () => {
  currentCameraIndex.value = (currentCameraIndex.value + 1) % cameraDevices.value.length
  if (mediaStream.value) {
    mediaStream.value.getTracks().forEach(track => track.stop())
  }
  await startCamera()
}

// 人脸检测帧循环
const detectFrame = async () => {
  if (!video.value || video.value.readyState !== 4) return
  
  const detections = await faceapi.detectAllFaces(
    video.value,
    new faceapi.TinyFaceDetectorOptions({ inputSize: 320 })
  )
  
  drawDetectionBox(detections)
  animationFrameId = requestAnimationFrame(detectFrame)
}

// 绘制检测框（处理坐标转换）
const drawDetectionBox = (detections) => {
  const ctx = overlay.value.getContext("2d")
  ctx.clearRect(0, 0, overlay.value.width, overlay.value.height)
  
  if (detections.length > 0) {
    const resizedDetections = faceapi.resizeResults(
      detections,
      { width: overlay.value.width, height: overlay.value.height }
    )
    
    resizedDetections.forEach(det => {
      const box = det.box
      ctx.beginPath()
      ctx.lineWidth = 4
      ctx.strokeStyle = "red"
      ctx.rect(box.x, box.y, box.width, box.height)
      ctx.stroke()
      
      ctx.font = 'bold 24px Arial'
      ctx.fillStyle = 'red'
      ctx.fillText(`匹配度: ${(det.score * 100).toFixed(1)}%`, box.x + 5, box.y - 10)
    })
  }
}

// 其他方法保持基本结构，主要修改以下部分：
// - 添加窗口尺寸变化监听
// - 优化错误处理
// - 完善API请求处理

onMounted(async () => {
  await loadFaceApiModels()
  await getCameraDevices()
  await startCamera()
  window.addEventListener('resize', adjustCanvasSize)
})

onBeforeUnmount(() => {
  if (animationFrameId) cancelAnimationFrame(animationFrameId)
  if (mediaStream.value) {
    mediaStream.value.getTracks().forEach(track => track.stop())
  }
  window.removeEventListener('resize', adjustCanvasSize)
})
</script>

<style scoped>
/* 原有样式优化 */
.overlay-canvas {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: auto;
  aspect-ratio: 4/3;
}

.camera-video {
  width: 100%;
  max-width: 640px;
  height: auto;
  aspect-ratio: 4/3;
  transform: scaleX(-1); /* 镜像翻转 */
}

@media screen and (max-width: 768px) {
  .overlay-canvas {
    aspect-ratio: 9/16; /* 适配竖屏比例 */
  }
}
</style>