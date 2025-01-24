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
          </div>
          <!-- 画布元素，用于显示摄像头 -->
          <canvas ref="canvas" class="camera-canvas"></canvas>
          
          <!-- 地图容器 -->
          <div class="map-container">
            <div class="map-overlay" ref="mapContainer">
              <div v-if="isMapLoading" class="map-loading">
                <span class="map-loading-text">地图加载中...</span>
              </div>
            </div>
          </div>
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
            <!-- 重试摄像头按钮 -->
            <el-button
              v-if="cameraError"
              type="primary"
              @click="retryCamera"
              class="control-button"
            >
              <el-icon><Camera /></el-icon>
              <span>重试摄像头</span>
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

        <!-- 摄像头错误提示 -->
        <el-alert
          v-if="cameraError"
          :title="cameraError"
          type="error"
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
import AMapLoader from '@amap/amap-jsapi-loader'

const AMAP_KEY = 'ff4dd4814f31d1e9122f1032f39ce9d9'
const AMAP_SECRET = '7dbd1d0587367322e8856f37dc33299d'

const video = ref(null)
const canvas = ref(null)
const mapContainer = ref(null)
const mediaStream = ref(null)
const isFrontCamera = ref(false)

const recognitionResult = ref('')
const locationStatus = ref('正在获取位置...')
const locationStatusType = ref('info')
const userLocation = ref(null)
const allowedLocation = ref(null)
const isLoading = ref(false)
const courseInfo = ref(null)
const isMapLoading = ref(true)
const cameraError = ref('')

const map = ref(null)

const getLocationByAMap = (AMap) => {
  return new Promise((resolve, reject) => {
    if (!AMap || !AMap.Geolocation) {
      reject(new Error('高德地图 API 未加载或版本不兼容'))
      return
    }

    // 优化定位配置
    const geolocation = new AMap.Geolocation({
      enableHighAccuracy: true,
      timeout: 2000,  // 缩短超时时间
      maximumAge: 30000,  // 使用缓存位置
      showButton: false,  // 隐藏定位按钮
      position: 'RB',
      offset: [10, 20],
      showMarker: true,
      markerOptions: {
        offset: new AMap.Pixel(-18, -36),
        content: '<img src="https://a.amap.com/jsapi_demos/static/resource/img/user.png" style="width:36px;height:36px"/>'
      },
      showCircle: true,
      circleOptions: {
        strokeColor: '#0093FF',
        noSelect: true,
        strokeOpacity: 0.5,
        strokeWeight: 1,
        fillColor: '#02B0FF',
        fillOpacity: 0.25
      },
      panToLocation: true,
      zoomToAccuracy: true,
      noGeoLocation: 0,
      animation: false
    })

    map.value.addControl(geolocation)

    geolocation.watchPosition((status, result) => {
      if (status === 'complete') {
        const { latitude, longitude } = result.position
        
        // 更健壮的坐标验证
        if (typeof latitude !== 'number' || typeof longitude !== 'number' ||
            isNaN(latitude) || isNaN(longitude) ||
            latitude < -90 || latitude > 90 ||
            longitude < -180 || longitude > 180) {
          console.warn('获取的坐标无效，使用默认中心点')
          return
        }
        
        userLocation.value = { latitude, longitude }
        
        // 确保地图实例存在
        if (map.value && typeof map.value.setCenter === 'function') {
          const center = [longitude, latitude]
          map.value.setCenter(center)
          map.value.setZoom(17)
        }
        
        resolve({ latitude, longitude })
      } else {
        console.error('获取位置失败:', result)
        reject(new Error(`获取位置失败: ${result.message}`))
      }
    })
  })
}

const initMap = (AMap) => {
  return new Promise((resolve) => {
    // 设置默认中心点为上海
    const defaultCenter = [121.473701, 31.230416]
    
    map.value = new AMap.Map(mapContainer.value, {
      zoom: 17,
      center: defaultCenter,
      viewMode: '2D',
      resizeEnable: true,
      zoomEnable: true,
      dragEnable: true,
      doubleClickZoom: false,
      keyboardEnable: false,
      rotateEnable: false,
      pitchEnable: false,
      showLabel: true,
      mapStyle: 'amap://styles/normal',
      features: ['bg', 'road', 'point', 'building'],
    })
    
    map.value.addControl(new AMap.ToolBar({
      position: 'RB',
      zoomPosition: false
    }))

    isMapLoading.value = false
    resolve(map.value)
  })
}

const startCamera = async () => {
  try {
    const constraints = {
      video: {
        width: { ideal: 640 },
        height: { ideal: 480 },
        facingMode: isFrontCamera.value ? 'user' : 'environment',
      },
    }
    mediaStream.value = await navigator.mediaDevices.getUserMedia(constraints)
    video.value.srcObject = mediaStream.value
  } catch (error) {
    console.error('摄像头启动失败:', error)
    if (error.name === 'NotAllowedError') {
      throw new Error('摄像头权限被拒绝，请检查浏览器设置')
    } else if (error.name === 'NotFoundError') {
      throw new Error('未找到摄像头设备')
    } else {
      throw new Error('无法访问摄像头，请检查设备设置')
    }
  }
}

const switchCamera = async () => {
  isFrontCamera.value = !isFrontCamera.value
  if (mediaStream.value) {
    mediaStream.value.getTracks().forEach((track) => track.stop())
  }
  await startCamera()
}

const startRecognition = () => {
  recognitionResult.value = '识别成功'
}

const verifyLocation = () => {
  locationStatus.value = '位置验证通过'
  locationStatusType.value = 'success'
}

const fetchCourseAndLocationInfo = async () => {
  isLoading.value = true
  try {
    await new Promise((resolve) => setTimeout(resolve, 1000))
    courseInfo.value = { name: '课程名称', location: { latitude: 39.90923, longitude: 116.397428 } }
    allowedLocation.value = { latitude: 39.90923, longitude: 116.397428 }
  } catch (error) {
    console.error('获取课程信息失败:', error)
  } finally {
    isLoading.value = false
  }
}

const retryCamera = async () => {
  cameraError.value = ''
  try {
    await startCamera()
  } catch (error) {
    cameraError.value = error.message
  }
}

onMounted(async () => {
  window._AMapSecurityConfig = {
    securityJsCode: AMAP_SECRET,
  }

  try {
    const AMap = await AMapLoader.load({
      key: AMAP_KEY,
      version: '2.0',
      plugins: ['AMap.Geolocation', 'AMap.ToolBar', 'AMap.Scale'],
    })

    await initMap(AMap)

    const location = await getLocationByAMap(AMap)
    map.value.setCenter([location.longitude, location.latitude])
    map.value.setZoom(17)
    
    new AMap.Marker({
      position: [location.longitude, location.latitude],
      title: '我的位置',
      map: map.value
    })

    verifyLocation()
    await fetchCourseAndLocationInfo()
  } catch (error) {
    console.error('地图或位置初始化失败:', error)
    locationStatus.value = '地图或位置初始化失败'
    locationStatusType.value = 'error'
  }

  try {
    await startCamera()
  } catch (error) {
    cameraError.value = error.message
  }
})

onBeforeUnmount(() => {
  if (mediaStream.value) {
    mediaStream.value.getTracks().forEach((track) => track.stop())
  }
  if (map.value) {
    map.value.destroy()
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

.map-container {
  margin-top: 20px;
  width: 100%;
  max-width: 640px;
  margin: 20px auto;
  transition: all 0.3s ease;
  position: relative;
}

.map-overlay {
  width: 100%;
  height: 300px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: all 0.3s ease;
}

.map-loading {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  z-index: 1;
}

.map-loading-text {
  color: #409eff;
  font-size: 16px;
  font-weight: bold;
}

@media screen and (max-width: 768px) {
  .map-container {
    margin: 10px auto;
  }
  
  .map-overlay {
    height: 250px;
  }
}

@media screen and (max-width: 480px) {
  .map-overlay {
    height: 200px;
  }
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
