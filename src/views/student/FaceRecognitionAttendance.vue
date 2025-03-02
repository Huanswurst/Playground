<template>
  <el-container class="face-recognition-container">
    <el-header class="dashboard-header">
      <div class="header-content">
        <el-button 
          type="primary" 
          @click="$router.push('/student/attendance')" 
          class="back-button"
          :icon="Calendar"
        >
          返回考勤
        </el-button>
          <h1 class="header-title">人脸识别考勤</h1>
          <el-button
            type="danger"
            class="logout-button"
            @click="handleLogout"
            style="margin-left: 15px"
          >
            退出登录
          </el-button>
      </div>
    </el-header>
    
    <el-main>
      <el-card class="camera-card" shadow="hover">
        <div class="camera-section">
          <div class="video-wrapper">
            <video ref="video" autoplay playsinline muted class="camera-video"></video>
            <canvas ref="overlay" class="overlay-canvas"></canvas>
            <canvas ref="canvas" class="hidden-canvas"></canvas>
          </div>

          <div class="camera-controls">
            <el-button 
              type="primary" 
              @click="switchCamera" 
              class="control-button"
              :disabled="cameraDevices.length < 2"
              :icon="Switch"
            >
              切换摄像头 ({{ currentCameraIndex + 1 }}/{{ cameraDevices.length }})
            </el-button>
            <el-button 
              type="success" 
              @click="startRecognition" 
              class="control-button"
              :loading="isRecognizing"
              :icon="Camera"
            >
              {{ isRecognizing ? '识别中...' : '开始识别' }}
            </el-button>
          </div>
        </div>

        <transition name="el-zoom-in-top">
          <el-alert
            v-if="recognitionResult"
            :title="recognitionResult"
            :type="resultType"
            show-icon
            class="recognition-result"
          />
        </transition>
      </el-card>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { Calendar, Switch, Camera } from '@element-plus/icons-vue'
import { ElNotification } from 'element-plus'
import * as faceapi from 'face-api.js'

// 配置常量
const CONFIG = {
  MODEL_PATH: '/models',
  DETECTION_INTERVAL: 150, // 毫秒
  MIN_CONFIDENCE: 0.8     // 最小置信度
}

// 响应式引用
const video = ref(null)
const canvas = ref(null)
const overlay = ref(null)
const mediaStream = ref(null)
const cameraDevices = ref([])
const currentCameraIndex = ref(0)
const recognitionResult = ref('')
const resultType = ref('info')
const isRecognizing = ref(false)
const detectionActive = ref(true)

// 人脸检测相关变量
let detectionInterval = null
let animationFrameId = null

/* 方法定义 */
// 加载人脸识别模型
const loadFaceApiModels = async () => {
  try {
    await Promise.all([
      faceapi.nets.tinyFaceDetector.loadFromUri(CONFIG.MODEL_PATH),
      faceapi.nets.faceLandmark68Net.loadFromUri(CONFIG.MODEL_PATH)
    ])
  } catch (error) {
    handleError('模型加载失败', error)
    throw error
  }
}

// 初始化摄像头
const initCamera = async () => {
  try {
    await getCameraDevices()
    await startCamera()
    startDetectionLoop()
  } catch (error) {
    handleError('摄像头初始化失败', error)
  }
}

// 获取摄像头设备列表
const getCameraDevices = async () => {
  try {
    const devices = await navigator.mediaDevices.enumerateDevices()
    cameraDevices.value = devices.filter(d => d.kind === 'videoinput')
    
    if (cameraDevices.value.length === 0) {
      throw new Error('未找到可用的摄像头设备')
    }
  } catch (error) {
    handleError('设备枚举失败', error)
    throw error
  }
}

// 启动指定摄像头
const startCamera = async () => {
  try {
    if (mediaStream.value) {
      mediaStream.value.getTracks().forEach(track => track.stop())
    }

    const deviceId = cameraDevices.value[currentCameraIndex.value]?.deviceId
    const constraints = {
      video: {
        deviceId: deviceId ? { exact: deviceId } : undefined,
        width: { ideal: 1280 },
        height: { ideal: 720 },
        frameRate: { ideal: 30 }
      }
    }

    mediaStream.value = await navigator.mediaDevices.getUserMedia(constraints)
    video.value.srcObject = mediaStream.value

    await new Promise((resolve) => {
      video.value.onloadedmetadata = () => resolve()
    })
    
    adjustCanvasSize()
    video.value.play()
  } catch (error) {
    handleCameraError(error)
    throw error
  }
}

// 调整画布尺寸
const adjustCanvasSize = () => {
  const videoEl = video.value
  const overlayEl = overlay.value
  const canvasEl = canvas.value

  if (!videoEl || !overlayEl || !canvasEl) return

  const videoWidth = videoEl.videoWidth
  const videoHeight = videoEl.videoHeight

  overlayEl.width = videoWidth
  overlayEl.height = videoHeight
  canvasEl.width = videoWidth
  canvasEl.height = videoHeight

  overlayEl.style.width = `${videoEl.clientWidth}px`
  overlayEl.style.height = `${videoEl.clientHeight}px`
}

// 启动检测循环
const startDetectionLoop = () => {
  stopDetectionLoop()
  detectionActive.value = true
  const detect = async () => {
    if (!detectionActive.value) return
    await detectFaces()
    animationFrameId = requestAnimationFrame(detect)
  }
  detect()
}

// 停止检测循环
const stopDetectionLoop = () => {
  detectionActive.value = false
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId)
  }
}

// 人脸检测处理
const detectFaces = async () => {
  try {
    const detections = await faceapi.detectAllFaces(
      video.value,
      new faceapi.TinyFaceDetectorOptions({
        inputSize: 320,
        scoreThreshold: CONFIG.MIN_CONFIDENCE
      })
    )
    drawDetectionBox(detections)
  } catch (error) {
    console.error('人脸检测错误:', error)
  }
}

// 绘制检测框
const drawDetectionBox = (detections) => {
  const ctx = overlay.value.getContext('2d')
  ctx.clearRect(0, 0, overlay.value.width, overlay.value.height)

  detections.forEach(detection => {
    const box = detection.box
    const score = detection.score.toFixed(2)
    
    ctx.beginPath()
    ctx.lineWidth = 4
    ctx.strokeStyle = '#409EFF'
    ctx.rect(box.x, box.y, box.width, box.height)
    ctx.stroke()

    ctx.fillStyle = '#409EFF'
    ctx.font = 'bold 18px Arial'
    ctx.fillText(`${score * 100}%`, box.x + 5, box.y - 10)
  })
}

// 执行人脸识别
const startRecognition = async () => {
  if (isRecognizing.value) return
  isRecognizing.value = true
  resultType.value = 'info'
  recognitionResult.value = '正在验证身份...'

  try {
    // 本地模拟识别结果
    await new Promise(resolve => setTimeout(resolve, 1500))
    const success = Math.random() > 0.2
    recognitionResult.value = success 
      ? '身份验证成功 ✅' 
      : '验证失败：未匹配到学生信息'
    resultType.value = success ? 'success' : 'error'
  } catch (error) {
    recognitionResult.value = '识别过程发生错误'
    resultType.value = 'error'
  } finally {
    isRecognizing.value = false
  }
}

// 摄像头错误处理
const handleCameraError = (error) => {
  let message = '摄像头访问失败：'
  switch (error.name) {
    case 'NotAllowedError':
      message += '请允许摄像头访问权限'
      break
    case 'NotFoundError':
      message += '未找到摄像头设备'
      break
    default:
      message += error.message
  }
  handleError(message, error)
}

// 通用错误处理
const handleError = (message, error) => {
  let errorMessage = error.message || error
  // 处理HTML格式的错误响应
  if (typeof errorMessage === 'string' && errorMessage.startsWith('<!DOCTYPE')) {
    errorMessage = '服务器返回了HTML错误页面，请检查API请求'
  }
  console.error(error)
  ElNotification({
    title: '发生错误',
    message: `${message}: ${errorMessage}`,
    type: 'error',
    duration: 5000
  })
}

// 生命周期钩子
onMounted(async () => {
  try {
    await loadFaceApiModels()
    await initCamera()
    window.addEventListener('resize', adjustCanvasSize)
  } catch (error) {
    recognitionResult.value = '初始化失败，请刷新页面重试'
  }
})

onBeforeUnmount(() => {
  stopDetectionLoop()
  if (mediaStream.value) {
    mediaStream.value.getTracks().forEach(track => track.stop())
  }
  window.removeEventListener('resize', adjustCanvasSize)
})
</script>

<style scoped lang="scss">
.face-recognition-container {
  height: 100vh;
  background: #f0f2f5;

  .dashboard-header {
    background: linear-gradient(135deg, #409EFF 0%, #337ecc 100%);
    .header-content {
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 100%;
      padding: 0 24px;
      
      .back-button {
        font-weight: 500;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
      }
      
      .header-title {
        margin: 0;
        color: white;
        font-size: 24px;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
      }
    }
  }

  .camera-card {
    max-width: 800px;
    margin: 24px auto;
    border-radius: 12px;
    overflow: hidden;
    
    .camera-section {
      position: relative;
      padding: 16px;
      background: #f8f9fa;
      border-radius: 8px;

      .video-wrapper {
        position: relative;
        width: 100%;
        aspect-ratio: 4/3;
        background: #000;
        border-radius: 8px;
        overflow: hidden;
        
        .camera-video {
          width: 100%;
          height: 100%;
          object-fit: cover;
        }
        
        .overlay-canvas {
          position: absolute;
          top: 0;
          left: 0;
          pointer-events: none;
        }
      }

      .camera-controls {
        margin-top: 16px;
        display: flex;
        gap: 12px;
        justify-content: center;
        
        .control-button {
          padding: 12px 24px;
          font-weight: 500;
          letter-spacing: 0.5px;
        }
      }
    }

    .recognition-result {
      margin-top: 16px;
      transition: all 0.3s ease;
    }
  }
}

.hidden-canvas {
  display: none;
}

@media (max-width: 768px) {
  .dashboard-header {
    padding: 0 12px !important;
    
    .header-title {
      font-size: 18px !important;
    }
    
    .back-button {
      padding: 8px 12px !important;
    }
  }

  .camera-card {
    margin: 12px;
    
    .camera-controls {
      flex-direction: column;
      
      .control-button {
        width: 100%;
      }
    }
  }
}
</style>
