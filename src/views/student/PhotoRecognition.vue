<template>
    <el-container>
      <el-header class="dashboard-header">
        <div class="header-content">
          <el-button type="primary" @click="$router.push('/student/attendance')" class="back-button">
            <el-icon><Calendar /></el-icon>
            <span>返回考勤</span>
          </el-button>
          <h1 class="header-title">照片人脸识别测试</h1>
        </div>
      </el-header>
  
      <el-main>
        <el-card class="photo-card" shadow="hover">
          <div class="photo-section">
            <!-- 文件上传 -->
            <input type="file" accept="image/*" @change="onPhotoSelected" />
            <!-- 显示上传的照片 -->
            <img v-if="selectedPhoto" ref="testPhoto" :src="selectedPhoto" alt="测试照片" class="test-photo" />
            <!-- overlay canvas -->
            <canvas ref="overlay" class="overlay-canvas"></canvas>
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
  import { ref, onMounted } from 'vue'
  import { Calendar } from '@element-plus/icons-vue'
  import * as faceapi from 'face-api.js'
  
  const selectedPhoto = ref('')
  const overlay = ref(null)
  const testPhoto = ref(null)
  const recognitionResult = ref('')
  
  // 加载 face-api.js 模型
  const loadFaceApiModels = async () => {
    const modelUrl = '/models' // 模型文件放在 public/models 下
    await faceapi.nets.tinyFaceDetector.loadFromUri(modelUrl)
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
  
  onMounted(async () => {
    await loadFaceApiModels()
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