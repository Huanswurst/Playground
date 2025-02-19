<template>
  <el-container class="face-recognition-container">
    <el-header class="dashboard-header">
      <div class="header-content">
        <el-button 
          type="primary" 
          @click="$router.push('/student/attendance')" 
          class="back-button"
        >
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
          <div class="camera-controls">
            <el-button 
              type="primary" 
              @click="switchCamera" 
              class="control-button"
              :disabled="cameraDevices.length < 2"
            >
              <el-icon><Switch /></el-icon>
              <span>切换摄像头</span>
            </el-button>
            <el-button 
              type="success" 
              @click="startRecognition" 
              class="control-button"
              :loading="isRecognizing"
            >
              <el-icon><Camera /></el-icon>
              <span>{{ isRecognizing ? '识别中...' : '开始识别' }}</span>
            </el-button>
          </div>
        </div>
        <el-alert
          v-if="recognitionResult"
          :title="recognitionResult"
          :type="resultType"
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

// 视频元素引用
const video = ref(null)
const overlay = ref(null)

// 状态管理
const mediaStream = ref(null)
const currentCameraIndex = ref(0)
const cameraDevices = ref([])
const recognitionResult = ref("")
const resultType = ref("info")
const isRecognizing = ref(false)
let detectionInterval = null

// 加载人脸检测模型
const loadFaceApiModels = async () => {
  try {
    await Promise.all([
      faceapi.nets.tinyFaceDetector.loadFromUri('/models'),
      faceapi.nets.faceLandmark68Net.loadFromUri('/models')
    ])
  } catch (error) {
    handleError(`模型加载失败: ${error.message}`)
  }
}

// 初始化摄像头
const initCamera = async () => {
  try {
    const devices = await navigator.mediaDevices.enumerateDevices()
    cameraDevices.value = devices.filter(d => d.kind === 'videoinput')
    
    if (cameraDevices.value.length === 0) {
      handleError("未找到可用摄像头设备")
      return
    }
    
    await startCamera()
    startDetection()
  } catch (error) {
    handleError(`摄像头初始化失败: ${error.message}`)
  }
}

// 启动摄像头
const startCamera = async () => {
  const deviceId = cameraDevices.value[currentCameraIndex.value]?.deviceId
  const constraints = {
    video: {
      deviceId: deviceId ? { exact: deviceId } : undefined,
      width: { ideal: 1280 },
      height: { ideal: 720 }
    }
  }

  try {
    mediaStream.value = await navigator.mediaDevices.getUserMedia(constraints)
    video.value.srcObject = mediaStream.value
    
    await new Promise(resolve => {
      video.value.onloadedmetadata = () => resolve()
    })
    
    adjustCanvasSize()
    video.value.play()
  } catch (error) {
    handleError(`摄像头访问失败: ${error.message}`)
  }
}

// 调整画布尺寸
const adjustCanvasSize = () => {
  if (!video.value || !overlay.value) return
  
  overlay.value.width = video.value.videoWidth
  overlay.value.height = video.value.videoHeight
  overlay.value.style.width = `${video.value.clientWidth}px`
  overlay.value.style.height = `${video.value.clientHeight}px`
}

// 人脸检测循环
const startDetection = () => {
  detectionInterval = setInterval(async () => {
    if (!video.value) return
    
    try {
      const detections = await faceapi.detectAllFaces(
        video.value,
        new faceapi.TinyFaceDetectorOptions({ inputSize: 320 })
      )
      drawDetectionBox(detections)
    } catch (error) {
      console.error("人脸检测错误:", error)
    }
  }, 200)
}

// 绘制检测框
const drawDetectionBox = (detections) => {
  const ctx = overlay.value.getContext('2d')
  ctx.clearRect(0, 0, overlay.value.width, overlay.value.height)

  detections.forEach(det => {
    const box = det.box
    ctx.beginPath()
    ctx.lineWidth = 4
    ctx.strokeStyle = "#409EFF"
    ctx.rect(box.x, box.y, box.width, box.height)
    ctx.stroke()

    ctx.fillStyle = "#409EFF"
    ctx.font = "bold 18px Arial"
    ctx.fillText(`置信度: ${(det.score * 100).toFixed(1)}%`, box.x + 5, box.y - 10)
  })
}

// 模拟识别功能
const startRecognition = async () => {
  if (isRecognizing.value) return
  
  isRecognizing.value = true
  recognitionResult.value = "正在验证身份..."
  resultType.value = "info"

  // 模拟识别过程（2秒延迟）
  setTimeout(() => {
    // 随机生成识别结果（80%成功率）
    const success = Math.random() < 0.8
    recognitionResult.value = success 
      ? "身份验证成功 ✅" 
      : "验证失败：未匹配到学生信息"
    resultType.value = success ? "success" : "error"
    isRecognizing.value = false
  }, 2000)
}

// 错误处理
const handleError = (message) => {
  recognitionResult.value = message
  resultType.value = "error"
  console.error(message)
}

// 生命周期
onMounted(async () => {
  await loadFaceApiModels()
  await initCamera()
  window.addEventListener("resize", adjustCanvasSize)
})

onBeforeUnmount(() => {
  clearInterval(detectionInterval)
  if (mediaStream.value) {
    mediaStream.value.getTracks().forEach(track => track.stop())
  }
  window.removeEventListener("resize", adjustCanvasSize)
})
</script>

<style scoped>
.face-recognition-container {
  height: 100vh;
}

.dashboard-header {
  background: #f5f5f5;
  padding: 16px;
  border-bottom: 1px solid #e0e0e0;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.camera-card {
  margin: 24px auto;
  max-width: 800px;
}

.camera-section {
  position: relative;
  text-align: center;
}

.camera-video {
  width: 100%;
  max-width: 640px;
  height: auto;
  aspect-ratio: 4/3;
}

.overlay-canvas {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none;
}

.camera-controls {
  margin-top: 16px;
  display: flex;
  gap: 16px;
  justify-content: center;
}

.recognition-result {
  margin-top: 16px;
}

@media (max-width: 768px) {
  .camera-video {
    aspect-ratio: 9/16;
  }
  
  .camera-controls {
    flex-direction: column;
  }
}
</style>
