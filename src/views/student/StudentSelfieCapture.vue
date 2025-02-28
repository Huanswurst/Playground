<template>
  <el-container class="selfie-container">
    <el-header class="dashboard-header">
      <div class="header-content">
        <h1 class="header-title">学生自拍</h1>
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
              @click="captureSelfie" 
              class="control-button"
              :loading="isCapturing"
            >
              {{ isCapturing ? '拍摄中...' : '拍摄自拍照' }}
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
import * as faceapi from 'face-api.js'

const video = ref(null)
const canvas = ref(null)
const overlay = ref(null)
const mediaStream = ref(null)
const isCapturing = ref(false)
const captureResult = ref('')
const resultType = ref('info')
const detectionActive = ref(true)

let detectionInterval = null
let animationFrameId = null

const loadFaceApiModels = async () => {
  try {
    await faceapi.loadTinyFaceDetectorModel('/models')
    await faceapi.loadFaceLandmarkTinyModel('/models')
  } catch (error) {
    handleError('模型加载失败', error)
  }
}

// 初始化摄像头
const initCamera = async () => {
  try {
    const constraints = {
      video: {
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
    startDetectionLoop()
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
    const detections = await faceapi.detectAllFaces(
      video.value,
      new faceapi.TinyFaceDetectorOptions()
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

// 拍摄自拍照
const captureSelfie = async () => {
  if (isCapturing.value) return
  isCapturing.value = true
  captureResult.value = '正在拍摄自拍照...'
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
        // 上传自拍照并进行比对
        const formData = new FormData()
        formData.append('file', blob, 'selfie.jpg')
        
        const response = await fetch('/api/compare_faces', {
          method: 'POST',
          body: formData
        })
        
        if (!response.ok) {
          throw new Error('比对失败')
        }

        const result = await response.json()
        if (result.match) {
          captureResult.value = '比对成功，身份验证通过'
          resultType.value = 'success'
          // 执行录入系统逻辑
          await enrollStudent()
        } else {
          captureResult.value = '比对失败，请重试'
          resultType.value = 'error'
        }
      } catch (error) {
        captureResult.value = '自拍照比对失败'
        resultType.value = 'error'
        throw error
      } finally {
        isCapturing.value = false
      }
    }, 'image/jpeg', 0.9)
  } catch (error) {
    captureResult.value = '拍摄自拍照失败'
    resultType.value = 'error'
    isCapturing.value = false
  }
}

// 录入学生信息
const enrollStudent = async () => {
  try {
    const response = await fetch('/api/enroll_student', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        // 学生信息
      })
    })
    
    if (!response.ok) {
      throw new Error('录入失败')
    }
  } catch (error) {
    captureResult.value = '学生信息录入失败'
    resultType.value = 'error'
    throw error
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
.selfie-container {
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