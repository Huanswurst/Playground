<template>
  <el-container class="selfie-container">
    <el-main>
      <el-card class="camera-card" shadow="hover">
        <div class="camera-section">
          <div class="video-wrapper">
            <video ref="video" autoplay playsinline muted class="camera-video"></video>
            <canvas ref="overlay" class="overlay-canvas"></canvas>
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
const video = ref(null)
const overlay = ref(null)
const mediaStream = ref(null)
const isOpenCVLoaded = ref(false)
const openCVError = ref(null)

// 动态加载OpenCV
const loadOpenCV = async () => {
  try {
    await new Promise((resolve, reject) => {
      const script = document.createElement('script')
      script.src = '/opencv.js'
      script.onload = () => {
        cv['onRuntimeInitialized'] = () => {
          isOpenCVLoaded.value = true
          resolve()
        }
      }
      script.onerror = (error) => {
        openCVError.value = error
        reject(error)
      }
      document.head.appendChild(script)
    })
  } catch (error) {
    console.error('OpenCV加载失败:', error)
    ElNotification.error({
      title: 'OpenCV错误',
      message: '无法加载OpenCV库'
    })
  }
}

// 初始化OpenCV分类器
let classifier = null
const initClassifier = () => {
  classifier = new cv.CascadeClassifier()
  classifier.load('/haarcascade_frontalface_default.xml')
}
const isCapturing = ref(false)
const captureResult = ref('')
const resultType = ref('info')
const detectionActive = ref(true)

let detectionInterval = null

// 开始视频流
const startVideoStream = async () => {
  try {
    // 添加摄像头请求状态提示
    captureResult.value = '正在请求摄像头权限...'
    resultType.value = 'info'
    
    // 获取并选择摄像头设备
    const devices = await navigator.mediaDevices.enumerateDevices()
    const videoDevices = devices.filter(device => device.kind === 'videoinput')
    
    if (videoDevices.length === 0) {
      throw new Error('未检测到可用摄像头设备')
    }

    // 优先选择带有"front"标签的前置摄像头
    const preferredCamera = videoDevices.find(device =>
      device.label.toLowerCase().includes('front') ||
      device.label.toLowerCase().includes('face')
    ) || videoDevices[0]

    // 初始化媒体流
    return await initCameraStream(preferredCamera.deviceId)
  } catch (error) {
    handleCameraError(error)
  }
}

// 初始化媒体流
const initCameraStream = async (deviceId) => {
  try {
    mediaStream.value = await navigator.mediaDevices.getUserMedia({
      video: {
        deviceId: deviceId ? { exact: deviceId } : undefined,
        width: { ideal: 1280 },
        height: { ideal: 720 },
        frameRate: { ideal: 30 }
      }
    })

    video.value.srcObject = mediaStream.value
    await new Promise(function(resolve) {
      video.value.onloadedmetadata = function() {
        resolve()
      }
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

  if (!videoEl || !overlayEl) return

  const videoWidth = videoEl.videoWidth
  const videoHeight = videoEl.videoHeight

  overlayEl.width = videoWidth
  overlayEl.height = videoHeight

  overlayEl.style.width = `${videoEl.clientWidth}px`
  overlayEl.style.height = `${videoEl.clientHeight}px`
}

// 摄像头错误处理
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
    
    // 验证视频元素
    if (!video.value) {
      throw new Error('视频元素未正确绑定')
    }
    
    video.value.srcObject = mediaStream.value
    
    // 添加调试信息
    console.log('摄像头设备:', videoDevices)
    console.log('媒体流状态:', mediaStream.value)
    
    await new Promise(resolve => {
      video.value.onloadedmetadata = () => {
        console.log('视频元数据加载完成')
        resolve()
      }
      video.value.onerror = (error) => {
        console.error('视频加载错误:', error)
        throw error
      }
    })
    
    startDetection()
  } catch (error) {
    console.error('无法访问摄像头:', error)
    ElNotification.error({
      title: '摄像头错误',
      message: `无法访问摄像头: ${error.message}`
    })
  }
}

// 开始检测
const startDetection = () => {
  detectionInterval = setInterval(() => {
    if (!detectionActive.value) return
    
    const srcMat = new cv.Mat(video.value.height, video.value.width, cv.CV_8UC4)
    const cap = new cv.VideoCapture(video.value)
    cap.read(srcMat)
    
    // 确保成功读取视频帧
    if (srcMat.empty()) {
      srcMat.delete()
      cap.delete()
      return
    }
    
    // 转换为灰度图
    const grayMat = new cv.Mat()
    cv.cvtColor(srcMat, grayMat, cv.COLOR_RGBA2GRAY)
    
    // 检测人脸
    const faces = new cv.RectVector()
    classifier.detectMultiScale(grayMat, faces)
    
    drawDetections(faces)
    
    srcMat.delete()
    grayMat.delete()
    faces.delete()
  }, 100)
}

// 绘制检测框
const drawDetections = (faces) => {
  const ctx = overlay.value.getContext('2d')
  ctx.clearRect(0, 0, overlay.value.width, overlay.value.height)
  
  // 调整canvas尺寸
  const displayWidth = overlay.value.clientWidth
  const displayHeight = overlay.value.clientHeight
  const scaleX = displayWidth / video.value.videoWidth
  const scaleY = displayHeight / video.value.videoHeight

  for (let i = 0; i < faces.size(); i++) {
    const face = faces.get(i)
    
    // 计算缩放后的坐标
    const scaledX = face.x * scaleX
    const scaledY = face.y * scaleY
    const scaledWidth = face.width * scaleX
    const scaledHeight = face.height * scaleY
    
    // 由于视频是水平翻转的，需要调整x坐标
    const adjustedX = displayWidth - scaledX - scaledWidth
    
    // 绘制矩形框
    ctx.strokeStyle = '#409EFF'
    ctx.lineWidth = 4
    ctx.strokeRect(adjustedX, scaledY, scaledWidth, scaledHeight)
  }
}

// 拍摄自拍照
const captureSelfie = async () => {
  isCapturing.value = true
  try {
    const canvas = document.createElement('canvas')
    canvas.width = video.value.videoWidth
    canvas.height = video.value.videoHeight
    const ctx = canvas.getContext('2d')
    ctx.drawImage(video.value, 0, 0, canvas.width, canvas.height)
    
    // 保存或处理图片
    const imageData = canvas.toDataURL('image/png')
    console.log('Captured image:', imageData)
    
    captureResult.value = '自拍照拍摄成功'
    resultType.value = 'success'
  } catch (error) {
    console.error('拍摄失败:', error)
    captureResult.value = '自拍照拍摄失败'
    resultType.value = 'error'
  } finally {
    isCapturing.value = false
  }
}

onMounted(async () => {
  try {
    await loadOpenCV()
    initClassifier()
    await startVideoStream()
  } catch (error) {
    console.error('初始化失败:', error)
    ElNotification.error({
      title: '初始化错误',
      message: '组件初始化失败'
    })
  }
})

onBeforeUnmount(() => {
  if (mediaStream.value) {
    mediaStream.value.getTracks().forEach(track => track.stop())
  }
  clearInterval(detectionInterval)
})
</script>

<style scoped>
.selfie-container {
  height: calc(100vh - 60px);
}

.camera-card {
  max-width: 900px;
  margin: 20px auto;
}

.video-wrapper {
  position: relative;
  width: 100%;
  padding-top: 56.25%; /* 16:9 宽高比 */
  background: #1a1a1a;
  border-radius: 8px;
  overflow: hidden;
}

.camera-video,
.overlay-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  transform: scaleX(-1); /* 水平镜像 */
  object-fit: cover;
}

.camera-controls {
  margin-top: 20px;
  text-align: center;
}

.control-button {
  width: 200px;
  height: 50px;
  font-size: 16px;
}

.capture-result {
  margin-top: 15px;
}
</style>
