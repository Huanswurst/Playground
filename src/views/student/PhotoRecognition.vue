<template>
  <el-container class="photo-recognition-container">
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
        <h1 class="header-title">照片人脸识别测试</h1>
      </div>
    </el-header>

    <el-main>
      <el-card class="photo-card" shadow="hover">
        <div class="photo-section">
          <div class="camera-wrapper">
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
              {{ isCapturing ? '拍摄中...' : '拍摄照片' }}
            </el-button>
          </div>

          <div class="upload-section">
            <input type="file" accept="image/*" @change="onPhotoSelected" />
            <img v-if="selectedPhoto" ref="testPhoto" :src="selectedPhoto" alt="测试照片" class="test-photo" />
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
import { Calendar } from '@element-plus/icons-vue'
import * as faceapi from 'face-api.js'

const video = ref(null)
const canvas = ref(null)
const overlay = ref(null)
const testPhoto = ref(null)
const mediaStream = ref(null)
const selectedPhoto = ref('')
const recognitionResult = ref('')
const isCapturing = ref(false)
const detectionActive = ref(true)

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
      selectedPhoto.value = URL.createObjectURL(blob)
      recognitionResult.value = '照片拍摄成功'
    }, 'image/jpeg', 0.9)
  } catch (error) {
    recognitionResult.value = '照片拍摄失败'
  } finally {
    isCapturing.value = false
  }
}

// 处理上传照片
const onPhotoSelected = (event) => {
  const file = event.target.files[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = () => {
    selectedPhoto.value = reader.result
    // 等待图片渲染后进行检测
    setTimeout(() => {
      detectFaceOnImage()
    }, 500)
  }
  reader.readAsDataURL(file)
}

// 对上传的图片进行人脸检测
const detectFaceOnImage = async () => {
  if (!testPhoto.value) return
  // 等待图片加载完成
  await new Promise(resolve => {
    if (testPhoto.value.complete) resolve()
    else testPhoto.value.onload = resolve
  })

  // 设置 overlay 画布尺寸与图片一致
  overlay.value.width = testPhoto.value.naturalWidth
  overlay.value.height = testPhoto.value.naturalHeight
  const displaySize = {
    width: testPhoto.value.naturalWidth,
    height: testPhoto.value.naturalHeight
  }

  // 调用 face-api.js 检测人脸
  const detections = await faceapi.detectAllFaces(testPhoto.value, new faceapi.TinyFaceDetectorOptions())
  const ctx = overlay.value.getContext('2d')
  ctx.clearRect(0, 0, overlay.value.width, overlay.value.height)

  if (detections.length > 0) {
    const resizedDetections = faceapi.resizeResults(detections, displaySize)
    resizedDetections.forEach(det => {
      const box = det.box
      // 绘制红色识别框
      ctx.beginPath()
      ctx.lineWidth = 4
      ctx.strokeStyle = "red"
      ctx.rect(box.x, box.y, box.width, box.height)
      ctx.stroke()
      // 绘制匹配度文字，利用 det.score
      const matchScore = (det.score * 100).toFixed(2) + '%'
      ctx.font = '18px Arial'
      ctx.fillStyle = 'red'
      ctx.fillText("匹配度：" + matchScore, box.x, box.y - 10)
    })
    recognitionResult.value = "人脸识别成功！"
  } else {
    recognitionResult.value = "未检测到人脸！"
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
  console.error(error)
  ElNotification({
    title: '发生错误',
    message: `${message}: ${error.message}`,
    type: 'error',
    duration: 5000
  })
}

// 手动释放摄像头资源
const releaseCamera = () => {
  stopDetectionLoop()
  if (mediaStream.value) {
    mediaStream.value.getTracks().forEach(track => {
      track.stop()
      track.enabled = false
    })
    mediaStream.value = null
  }
}

// 生命周期钩子
onMounted(async () => {
  try {
    await loadFaceApiModels()
    await initCamera()
    window.addEventListener('resize', adjustCanvasSize)
    document.addEventListener('visibilitychange', handleVisibilityChange)
  } catch (error) {
    recognitionResult.value = '初始化失败，请刷新页面重试'
  }
})

onBeforeUnmount(() => {
  releaseCamera()
  window.removeEventListener('resize', adjustCanvasSize)
  document.removeEventListener('visibilitychange', handleVisibilityChange)
})

// 处理页面可见性变化
const handleVisibilityChange = () => {
  if (document.hidden) {
    releaseCamera()
  } else {
    initCamera()
  }
}
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
    margin-right: 20px;
    background-color: white;
    border-color: white;
    color: #409eff;
  }
  
  .photo-card {
    max-width: 800px;
    margin: 10px auto;
    padding: 10px;
    text-align: center;
  }
  
  .photo-section {
    position: relative;
    margin-top: 20px;
  }
  
  .test-photo {
    max-width: 100%;
    border-radius: 8px;
    display: block;
    margin: auto;
  }
  
  .overlay-canvas {
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    pointer-events: none;
  }
  
  .recognition-result {
    margin-top: 20px;
  }
  </style>
