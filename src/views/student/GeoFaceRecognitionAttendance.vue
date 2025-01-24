<template>
  <el-container>
    <el-header class="dashboard-header">
      <div class="header-content">
        <el-button type="primary" @click="$router.push('/student/attendance')" class="back-button">
          <el-icon><Calendar /></el-icon>
          <span>返回考勤</span>
        </el-button>
        <h1 class="header-title">人脸识别考勤（带位置验证）</h1>
      </div>
    </el-header>

    <el-main>
      <el-card class="camera-card" shadow="hover">
        <div class="camera-section">
          <!-- 视频元素 -->
          <div class="camera-container">
            <video ref="video" autoplay playsinline class="camera-video"></video>
            <!-- 地图容器 -->
            <div ref="mapContainer" class="map-overlay"></div>
          </div>
          <!-- 画布元素，用于捕获图像 -->
          <canvas ref="canvas" style="display: none;"></canvas>
          <div class="camera-controls">
            <!-- 切换摄像头按钮 -->
            <el-button type="primary" @click="switchCamera" class="control-button">
              <el-icon><Switch /></el-icon>
              <span>切换摄像头</span>
            </el-button>
            <!-- 开始识别按钮 -->
            <el-button type="success" @click="startRecognition" class="control-button">
              <el-icon><Camera /></el-icon>
              <span>开始识别</span>
            </el-button>
          </div>
        </div>

        <!-- 位置验证状态提示 -->
        <el-alert
          v-if="locationStatus"
          :title="locationStatus"
          :type="locationStatusType"
          show-icon
          class="recognition-result"
        />

        <!-- 人脸识别结果提示 -->
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
import AMapLoader from '@amap/amap-jsapi-loader' // 导入高德地图加载器

// 高德地图密钥和安全密钥
const AMAP_KEY = 'ff4dd4814f31d1e9122f1032f39ce9d9' // 你的高德地图 API Key
const AMAP_SECRET = '7dbd1d0587367322e8856f37dc33299d' // 你的高德地图安全密钥

// 摄像头相关
const video = ref(null) // 视频元素引用
const canvas = ref(null) // 画布元素引用
const mapContainer = ref(null) // 地图容器引用
const mediaStream = ref(null) // 媒体流对象
const isFrontCamera = ref(false) // 是否使用前置摄像头

// 状态相关
const recognitionResult = ref('') // 人脸识别结果
const locationStatus = ref('正在获取位置...') // 位置验证状态
const locationStatusType = ref('info') // 位置验证状态类型
const userLocation = ref(null) // 用户当前位置
const allowedLocation = ref(null) // 允许的位置范围
const isLoading = ref(false) // 加载状态
const courseInfo = ref(null) // 课程信息

// 使用高德地图获取 IP 定位
const getLocationByAMap = (AMap) => {
  return new Promise((resolve, reject) => {
    if (!AMap || !AMap.Geolocation) {
      reject(new Error('高德地图 API 未加载或版本不兼容'))
      return
    }

    // 使用高德地图的 IP 定位功能
    const geolocation = new AMap.Geolocation({
      enableHighAccuracy: true, // 是否使用高精度定位
      timeout: 5000, // 超时时间
      showButton: false, // 是否显示定位按钮
    })

    geolocation.getCurrentPosition((status, result) => {
      if (status === 'complete') {
        const { latitude, longitude } = result.position
        userLocation.value = { latitude, longitude }
        resolve({ latitude, longitude })
      } else {
        console.error('获取位置失败:', result) // 打印完整的错误信息
        reject(new Error(`获取位置失败: ${result.message}`))
      }
    })
  })
}

// 地图实例
const map = ref(null)

// 初始化地图
const initMap = (AMap) => {
  return new Promise((resolve) => {
    map.value = new AMap.Map(mapContainer.value, {
      zoom: 15,
      center: [116.397428, 39.90923],
      viewMode: '2D',
      resizeEnable: true,
      zoomEnable: true,
      dragEnable: true,
      doubleClickZoom: false,
      keyboardEnable: false,
      rotateEnable: false,
      pitchEnable: false,
      showLabel: false,
      mapStyle: 'amap://styles/normal',
      features: ['bg', 'road', 'point'],
    })
    resolve(map.value)
  })
}

// 组件挂载时启动摄像头、获取位置和课程信息
onMounted(() => {
  // 设置高德地图安全密钥
  window._AMapSecurityConfig = {
    securityJsCode: AMAP_SECRET,
  }

  // 加载高德地图 JS API
  AMapLoader.load({
    key: AMAP_KEY,
    version: '2.0',
    plugins: ['AMap.Geolocation'], // 需要使用的插件
  })
    .then(async (AMap) => {
      await startCamera()
      await initMap(AMap)
      try {
        const location = await getLocationByAMap(AMap)
        map.value.setCenter([location.longitude, location.latitude])
        verifyLocation()
      } catch (error) {
        locationStatus.value = error.message // 显示具体的错误信息
        locationStatusType.value = 'error'
        console.error('获取位置失败:', error)
      }
      await fetchCourseAndLocationInfo()
    })
    .catch((error) => {
      console.error('高德地图加载失败:', error)
      locationStatus.value = '高德地图加载失败'
      locationStatusType.value = 'error'
    })
})

// 组件卸载时关闭摄像头
onBeforeUnmount(() => {
  if (mediaStream.value) {
    mediaStream.value.getTracks().forEach((track) => track.stop())
  }
})
</script>

<style scoped>
/* 样式保持不变 */
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
}

.back-button {
  max-width: 100px;
  max-height: 80px;
  padding: 15px;
  margin-right: 20px;
  background-color: white;
  border-color: white;
  color: #409eff;
}

.back-button .el-icon {
  font-size: 25px;
}

.back-button span {
  font-size: 15px;
}

.header-title {
  font-size: 24px;
  font-weight: bold;
  margin: 0;
  line-height: 60px;
}

.camera-card {
  max-width: 800px;
  margin: 10px auto;
  padding: 10px;
  text-align: center;
}

@media screen and (max-width: 768px) {
  .dashboard-header {
    padding: 0 10px;
  }
  .el-button + .el-button {
    margin-left: 0 !important;
  }
  .header-title {
    font-size: 18px;
  }

  .back-button {
    max-width: 100px;
    max-height: 80px;
    padding: 15px;
    margin-right: 20px;
    background-color: white;
    border-color: white;
    color: #409eff;
  }

  .back-button .el-icon {
    font-size: 16px;
  }

  .back-button span {
    font-size: 13px;
  }

  .camera-card {
    width: 90%;
    margin: 0 auto;
    padding: 10px;
  }

  .camera-video {
    max-width: 100%;
  }

  .camera-controls {
    flex-direction: column;
    align-items: center;
    width: 100%;
    margin: 5px 0;
  }

  .control-button {
    width: 100%;
    margin-bottom: 10px;
  }

  .el-form-item__content {
    flex-direction: column;
    align-items: flex-start;
  }
}

.camera-container {
  position: relative;
  width: 100%;
  max-width: 640px;
  margin: 0 auto;
}

.camera-video {
  width: 100%;
  border-radius: 8px;
  margin-bottom: 20px;
}

.map-overlay {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 30%;
  height: 200px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.camera-controls {
  display: flex;
  justify-content: center;
  margin: 10px 0;
}

.control-button {
  width: 160px;
  margin-bottom: 10px !important;
}

.recognition-result {
  margin-top: 20px;
}
</style>
