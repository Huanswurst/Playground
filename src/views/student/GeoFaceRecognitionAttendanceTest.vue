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
          <div class="camera-container">
            <video ref="video" autoplay playsinline class="camera-video"></video>
          </div>
          <canvas ref="canvas" class="camera-canvas"></canvas>
          
          <div class="map-container">
            <div class="map-overlay" ref="mapContainer">
              <div v-if="isMapLoading" class="map-loading">
                <span class="map-loading-text">地图加载中...</span>
              </div>
            </div>
          </div>
          <div class="camera-controls">
            <el-button type="primary" @click="switchCamera" class="control-button">
              <el-icon><Switch /></el-icon>
              <span>切换摄像头</span>
            </el-button>
            <el-button type="success" @click="startRecognition" class="control-button">
              <el-icon><Camera /></el-icon>
              <span>开始识别</span>
            </el-button>
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

        <el-alert
          v-if="locationStatus"
          :title="locationStatus"
          :type="locationStatusType"
          show-icon
          class="recognition-result"
        />

        <el-alert
          v-if="recognitionResult"
          :title="recognitionResult"
          type="success"
          show-icon
          class="recognition-result"
        />

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
const marker = ref(null)

const initAMap = async () => {
  try {
    const AMap = await AMapLoader.load({
      key: AMAP_KEY,
      version: '2.0',
      plugins: ['AMap.Geolocation', 'AMap.Marker']
    })

    // 初始化地图
    map.value = new AMap.Map(mapContainer.value, {
      zoom: 16,
      resizeEnable: true
    })

    // 添加定位控件
    const geolocation = new AMap.Geolocation({
      enableHighAccuracy: true,
      timeout: 10000,
      position: 'RB',
      offset: [10, 20],
      zoomToAccuracy: true,
      showMarker: true,
      showCircle: true
    })
    map.value.addControl(geolocation)

    // 获取定位
    geolocation.getCurrentPosition((status, result) => {
      if (status === 'complete') {
        onComplete(result)
      } else {
        onError(result)
      }
    })

    isMapLoading.value = false
  } catch (error) {
    console.error('地图加载失败:', error)
    locationStatus.value = '地图加载失败'
    locationStatusType.value = 'error'
  }
}

// 定位成功回调
function onComplete(data) {
  const str = []
  str.push('定位结果：' + data.position)
  str.push('定位类别：' + data.location_type)
  if(data.accuracy){
    str.push('精度：' + data.accuracy + ' 米')
  }
  str.push('是否经过偏移：' + (data.isConverted ? '是' : '否'))
  
  locationStatus.value = str.join('<br>')
  locationStatusType.value = 'success'
  
  // 保存定位结果
  userLocation.value = {
    latitude: data.position.lat,
    longitude: data.position.lng,
    source: 'amap'
  }
}

// 定位失败回调
function onError(data) {
  locationStatus.value = '定位失败：' + data.message
  locationStatusType.value = 'error'
}

onMounted(() => {
  initAMap()
})

onBeforeUnmount(() => {
  if (map.value) {
    map.value.destroy()
  }
  if (marker.value) {
    marker.value.setMap(null)
  }
})
</script>

<style scoped>
/* 保持原有样式不变 */
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
