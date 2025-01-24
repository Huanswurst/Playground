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
const marker = ref(null)

// 计算两个坐标之间的距离（单位：米）
const calculateDistance = (lat1, lon1, lat2, lon2) => {
  const R = 6371e3 // 地球半径
  const φ1 = (lat1 * Math.PI) / 180
  const φ2 = (lat2 * Math.PI) / 180
  const Δφ = ((lat2 - lat1) * Math.PI) / 180
  const Δλ = ((lon2 - lon1) * Math.PI) / 180

  const a =
    Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
    Math.cos(φ1) * Math.cos(φ2) * Math.sin(Δλ / 2) * Math.sin(Δλ / 2)
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))

  return R * c
}

// 获取浏览器定位
const getBrowserLocation = () => {
  return new Promise((resolve) => {
    if (!navigator.geolocation) {
      locationStatus.value = '您的设备不支持定位功能'
      locationStatusType.value = 'error'
      return resolve(null)
    }

    navigator.geolocation.getCurrentPosition(
      (position) => resolve({
        latitude: position.coords.latitude,
        longitude: position.coords.longitude,
        source: 'browser'
      }),
      (error) => {
        switch(error.code) {
          case error.PERMISSION_DENIED:
            locationStatus.value = '请开启定位权限'
            break;
          case error.POSITION_UNAVAILABLE:
            locationStatus.value = '无法获取位置信息'
            break;
          case error.TIMEOUT:
            locationStatus.value = '定位请求超时'
            break;
          default:
            locationStatus.value = '定位失败，请重试'
        }
        locationStatusType.value = 'error'
        resolve(null)
      },
      {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0
      }
    )
  })
}

// 获取高德定位
const getAMapLocation = (AMap) => {
  return new Promise((resolve) => {
    const geolocation = new AMap.Geolocation({
      enableHighAccuracy: true,
      timeout: 5000,
      showMarker: true,
      showCircle: true
    })

    geolocation.getCurrentPosition((status, result) => {
      if (status === 'complete') {
        resolve({
          latitude: result.position.lat,
          longitude: result.position.lng,
          source: 'amap'
        })
      } else {
        resolve(null)
      }
    })
  })
}

// 计算最终定位
const calculateFinalLocation = (browserLoc, amapLoc) => {
  if (browserLoc && amapLoc) {
    // 两个定位都存在，取中点
    return {
      latitude: (browserLoc.latitude + amapLoc.latitude) / 2,
      longitude: (browserLoc.longitude + amapLoc.longitude) / 2,
      source: 'combined'
    }
  } else if (browserLoc) {
    // 只有浏览器定位
    return browserLoc
  } else if (amapLoc) {
    // 只有高德定位
    return amapLoc
  } else {
    // 无定位数据
    locationStatus.value = '无法获取定位数据'
    locationStatusType.value = 'error'
    return null
  }
}

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

    // 同时获取浏览器和高德定位
    const [browserLoc, amapLoc] = await Promise.all([
      getBrowserLocation(),
      getAMapLocation(AMap)
    ])

    // 计算最终定位
    const finalLocation = calculateFinalLocation(browserLoc, amapLoc)
    
    if (finalLocation) {
      const center = [finalLocation.longitude, finalLocation.latitude]
      map.value.setCenter(center)
      userLocation.value = finalLocation
      locationStatus.value = '定位成功'
      locationStatusType.value = 'success'

      // 添加标记点
      marker.value = new AMap.Marker({
        position: center,
        icon: 'https://webapi.amap.com/theme/v1.3/markers/n/mark_b.png',
        offset: new AMap.Pixel(-13, -30)
      })
      marker.value.setMap(map.value)
    }

    isMapLoading.value = false
  } catch (error) {
    console.error('地图加载失败:', error)
    locationStatus.value = '地图加载失败'
    locationStatusType.value = 'error'
  }
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
