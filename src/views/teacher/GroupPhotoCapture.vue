<template>
  <el-container class="group-photo-container">
    <el-header class="dashboard-header">
      <div class="header-content">
        <h1 class="header-title">集体照拍摄</h1>
        <el-button
          type="danger"
          class="logout-button"
          @click="handleLogout"
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
              @click="capturePhoto"
              class="control-button"
              :loading="isCapturing"
            >
              {{ isCapturing ? '拍摄中...' : '拍摄集体照' }}
            </el-button>
            
            <el-button
              v-if="devices.length > 1"
              type="info"
              @click="toggleCamera"
              class="control-button"
            >
              {{ isRearCamera ? '切换前置摄像头' : '切换后置摄像头' }}
            </el-button>
          </div>
        </div>

        <el-alert
          v-if="captureResult"
          :title="captureResult"
          :type="resultType"
          show-icon
          class="capture-result"
        />
      </el-card>
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { ElNotification } from 'element-plus'
import { useRouter } from 'vue-router'

const router = useRouter()
const handleLogout = () => {
  router.push('/login')
}
import * as faceapi from 'face-api.js'

const video = ref(null)
const canvas = ref(null)
const overlay = ref(null)
const mediaStream = ref(null)
const isCapturing = ref(false)
const captureResult = ref('')
const resultType = ref('info')
const detectionActive = ref(true)
const devices = ref([])
const currentDeviceId = ref('')
const isRearCamera = ref(false)

let detectionInterval = null
let animationFrameId = null

// 加载人脸识别模型
const loadFaceApiModels = async () => {
  try {
    await faceapi.loadTinyFaceDetectorModel('/models')
    await faceapi.loadFaceLandmarkTinyModel('/models')
  } catch (error) {
    handleError('模型加载失败', error)
  }
}

// 获取摄像头设备
const getCameraDevices = async () => {
  try {
    const devices = await navigator.mediaDevices.enumerateDevices()
    const videoDevices = devices.filter(device => device.kind === 'videoinput')
    devices.value = videoDevices
    return videoDevices
  } catch (error) {
    console.error('获取摄像头设备失败:', error)
    return []
  }
}

// 切换摄像头
const switchCamera = async (deviceId) => {
  if (mediaStream.value) {
    mediaStream.value.getTracks().forEach(track => track.stop())
  }

  try {
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
    currentDeviceId.value = deviceId

    await new Promise((resolve) => {
      video.value.onloadedmetadata = () => resolve()
    })
    
    adjustCanvasSize()
    video.value.play()
    startDetectionLoop()
  } catch (error) {
    handleCameraError(error)
  }
}

// 初始化摄像头
const initCamera = async () => {
  try {
    const devices = await getCameraDevices()
    if (devices.length === 0) {
      throw new Error('未找到摄像头设备')
    }

    // 优先选择后置摄像头
    const rearCamera = devices.find(device =>
      device.label.toLowerCase().includes('back') ||
      device.label.toLowerCase().includes('rear')
    )

    if (rearCamera) {
      await switchCamera(rearCamera.deviceId)
      isRearCamera.value = true
    } else {
      await switchCamera(devices[0].deviceId)
      isRearCamera.value = false
    }
  } catch (error) {
    handleCameraError(error)
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
    // 确保模型已加载
    if (!faceapi.nets.tinyFaceDetector.params || !faceapi.nets.faceLandmark68Net.params) {
      return
    }

    // 确保overlay元素存在
    if (!overlay.value) {
      return
    }

    const detections = await faceapi.detectAllFaces(
      video.value,
      new faceapi.TinyFaceDetectorOptions()
    ).withFaceLandmarks() // 添加人脸特征点检测
    
    // 调整检测结果到canvas尺寸
    const resizedDetections = faceapi.resizeResults(detections, {
      width: overlay.value.width,
      height: overlay.value.height
    })
    
    drawDetectionBox(resizedDetections)
  } catch (error) {
    console.error('人脸检测错误:', error)
  }
}

// 绘制检测框
const drawDetectionBox = (detections) => {
  if (!overlay.value) return
  
  const ctx = overlay.value.getContext('2d')
  if (!ctx) return

  ctx.clearRect(0, 0, overlay.value.width, overlay.value.height)

  detections.forEach(detection => {
    const box = detection.detection.box // 使用detection.detection.box获取更精确的框
    const score = detection.detection.score.toFixed(2)
    
    // 绘制人脸框
    ctx.beginPath()
    ctx.lineWidth = 4
    ctx.strokeStyle = '#409EFF'
    ctx.rect(box.x, box.y, box.width, box.height)
    ctx.stroke()

    // 绘制置信度
    ctx.fillStyle = '#409EFF'
    ctx.font = 'bold 18px Arial'
    ctx.fillText(`${score * 100}%`, box.x + 5, box.y - 10)
    
    // 绘制人脸特征点（可选）
    if (detection.landmarks) {
      ctx.fillStyle = '#FF0000'
      detection.landmarks.positions.forEach(point => {
        ctx.beginPath()
        ctx.arc(point.x, point.y, 2, 0, 2 * Math.PI)
        ctx.fill()
      })
    }
  })
}

// 切换摄像头
const toggleCamera = async () => {
  try {
    const devices = await getCameraDevices()
    if (devices.length < 2) return

    // 找到当前未使用的摄像头
    const nextDevice = devices.find(device =>
      device.deviceId !== currentDeviceId.value
    )

    if (nextDevice) {
      await switchCamera(nextDevice.deviceId)
      isRearCamera.value = nextDevice.label.toLowerCase().includes('back') ||
                         nextDevice.label.toLowerCase().includes('rear')
    }
  } catch (error) {
    console.error('切换摄像头失败:', error)
    ElNotification({
      title: '错误',
      message: '切换摄像头失败',
      type: 'error',
      duration: 3000
    })
  }
}

// 拍摄集体照
const capturePhoto = async () => {
  if (isCapturing.value) return
  isCapturing.value = true
  captureResult.value = '正在拍摄集体照...'
  resultType.value = 'info'

  try {
    // 获取视频帧
    const videoEl = video.value
    const canvasEl = canvas.value
    canvasEl.width = videoEl.videoWidth
    canvasEl.height = videoEl.videoHeight
    
    const ctx = canvasEl.getContext('2d')
    ctx.drawImage(videoEl, 0, 0, canvasEl.width, canvasEl.height)
    
    // 将图像转换为Blob
    canvasEl.toBlob(async (blob) => {
      try {
        // 上传集体照
        const formData = new FormData()
        formData.append('file', blob, 'group_photo.jpg')
        
        const response = await fetch('/api/upload_group_photo', {
          method: 'POST',
          body: formData
        })
        
        if (!response.ok) {
          throw new Error('上传失败')
        }
        
        captureResult.value = '集体照上传成功'
        resultType.value = 'success'
      } catch (error) {
        captureResult.value = '集体照上传失败'
        resultType.value = 'error'
        throw error
      } finally {
        isCapturing.value = false
      }
    }, 'image/jpeg', 0.9)
  } catch (error) {
    captureResult.value = '拍摄集体照失败'
    resultType.value = 'error'
    isCapturing.value = false
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
  ElNotification({
    title: '发生错误',
    message: message,
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
    captureResult.value = '初始化失败，请刷新页面重试'
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
.group-photo-container {
  height: 100vh;
  background: #f0f2f5;

  .dashboard-header {
    background: linear-gradient(135deg, #409EFF 0%, #337ecc 100%);
    .header-content {
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100%;
      padding: 0 24px;
      
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

    .capture-result {
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