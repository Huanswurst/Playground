<template>
  <el-container class="special-case-container">
    <el-header class="dashboard-header">
      <div class="header-content">
        <h1 class="header-title">特殊情况信息录入</h1>
      </div>
    </el-header>
    
    <el-main>
      <el-card class="form-card" shadow="hover">
        <el-form :model="form" label-width="120px">
          <!-- 人脸拍照部分 -->
          <el-form-item label="学生照片">
            <div class="camera-section">
              <div class="video-wrapper">
                <video ref="video" autoplay playsinline muted class="camera-video"></video>
                <canvas ref="overlay" class="overlay-canvas"></canvas>
                <canvas ref="canvas" class="hidden-canvas"></canvas>
              </div>
              <el-button 
                type="primary" 
                @click="capturePhoto" 
                class="control-button"
                :loading="isCapturing"
              >
                {{ isCapturing ? '拍摄中...' : '拍摄照片' }}
            </el-button>
            </div>
          </el-form-item>

          <!-- 其他信息录入 -->
          <el-form-item label="学生姓名">
            <el-input v-model="form.name" placeholder="请输入学生姓名" />
          </el-form-item>
          
          <el-form-item label="学号">
            <el-input v-model="form.studentNumber" placeholder="请输入学号" />
          </el-form-item>
          
          <el-form-item label="班级">
            <el-input v-model="form.class" placeholder="请输入班级" />
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" @click="submitForm">提交</el-button>
          </el-form-item>
        </el-form>

        <el-alert
          v-if="resultMessage"
          :title="resultMessage"
          :type="resultType"
          show-icon
          class="result-alert"
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
const resultMessage = ref('')
const resultType = ref('info')
const detectionActive = ref(true)

let detectionInterval = null
let animationFrameId = null

const form = ref({
  name: '',
  studentNumber: '',
  class: '',
  photo: null
})

// 加载人脸识别模型
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

// 拍摄照片
const capturePhoto = async () => {
  if (isCapturing.value) return
  isCapturing.value = true

  try {
    const videoEl = video.value
    const canvasEl = canvas.value
    canvasEl.width = videoEl.videoWidth
    canvasEl.height = videoEl.videoHeight
    
    const ctx = canvasEl.getContext('2d')
    ctx.drawImage(videoEl, 0, 0, canvasEl.width, canvasEl.height)
    
    canvasEl.toBlob((blob) => {
      form.value.photo = blob
      resultMessage.value = '照片拍摄成功'
      resultType.value = 'success'
    }, 'image/jpeg', 0.9)
  } catch (error) {
    resultMessage.value = '照片拍摄失败'
    resultType.value = 'error'
  } finally {
    isCapturing.value = false
  }
}

// 提交表单
const submitForm = async () => {
  try {
    const formData = new FormData()
    formData.append('name', form.value.name)
    formData.append('studentNumber', form.value.studentNumber)
    formData.append('class', form.value.class)
    formData.append('photo', form.value.photo)

    const response = await fetch('/api/special_case_enrollment', {
      method: 'POST',
      body: formData
    })
    
    if (!response.ok) {
      throw new Error('提交失败')
    }

    resultMessage.value = '信息提交成功'
    resultType.value = 'success'
  } catch (error) {
    resultMessage.value = '信息提交失败'
    resultType.value = 'error'
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
    resultMessage.value = '初始化失败，请刷新页面重试'
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
.special-case-container {
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

  .form-card {
    max-width: 800px;
    margin: 24px auto;
    padding: 24px;
    border-radius: 12px;
    
    .camera-section {
      margin-bottom: 24px;
      
      .video-wrapper {
        position: relative;
        width: 100%;
        aspect-ratio: 4/3;
        background: #000;
        border-radius: 8px;
        overflow: hidden;
        margin-bottom: 16px;
        
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

      .control-button {
        width: 100%;
      }
    }

    .result-alert {
      margin-top: 24px;
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

  .form-card {
    margin: 12px;
    padding: 16px;
  }
}
</style>