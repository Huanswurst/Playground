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
        <!-- 添加地图容器 -->
        <div id="map-container" style="height: 400px; margin-bottom: 20px;"></div>

        <div class="camera-section">
          <video ref="video" autoplay playsinline class="camera-video"></video>
          <canvas ref="canvas" style="display: none;"></canvas>
          <div class="camera-controls">
            <el-button type="primary" @click="switchCamera" class="control-button">
              <el-icon><Switch /></el-icon>
              <span>切换摄像头</span>
            </el-button>
            <el-button type="success" @click="startRecognition" class="control-button">
              <el-icon><camera /></el-icon>
              <span>开始识别</span>
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
          v-if="userLocation"
          :title="`当前位置：纬度 ${userLocation.latitude.toFixed(6)}，经度 ${userLocation.longitude.toFixed(6)}`"
          type="info"
          show-icon
          class="recognition-result"
        >
          <template #default>
            <div class="location-details">
              <p>纬度: {{ userLocation.latitude.toFixed(6) }}</p>
              <p>经度: {{ userLocation.longitude.toFixed(6) }}</p>
              <el-button 
                type="primary" 
                size="small"
                @click="copyCoordinates"
              >
                复制坐标
              </el-button>
            </div>
          </template>
        </el-alert>

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
import { Calendar, Switch, Camera } from '@element-plus/icons-vue'
import config from '@/config.js'
import { ref, onBeforeUnmount, onMounted } from 'vue'
import AMapLoader from '@amap/amap-jsapi-loader'

const video = ref(null)
const mediaStream = ref(null)
const isFrontCamera = ref(false)
const recognitionResult = ref("")
const locationStatus = ref("正在获取位置...")
const locationStatusType = ref("info")
const userLocation = ref(null)
const isLoading = ref(false)
const courseInfo = ref(null)
const allowedLocation = ref(null)
const map = ref(null)

// 初始化地图
    const initMap = async () => {
      try {
        // Set security config first
        window._AMapSecurityConfig = {
          securityJsCode: config.amapSecurityKey
        }

        const AMap = await AMapLoader.load({
          key: config.amapKey,
          version: '2.0',
          plugins: ['AMap.Geolocation', 'AMap.Scale']
        })

        map.value = new AMap.Map('map-container', {
          zoom: 15,
          resizeEnable: true,
          viewMode: '3D'
        })

        // Add scale control
        map.value.addControl(new AMap.Scale())

        // Add geolocation control with better error handling
        const geolocation = new AMap.Geolocation({
          enableHighAccuracy: true,
          timeout: 20000,
          maximumAge: 0,
          showMarker: true,
          showCircle: true,
          panToLocation: true,
          convert: true,
          GeoLocationFirst: true,
          noIpLocate: true,
          noGeoLocation: false,
          useNative: true,
          showButton: false
        })

        map.value.addControl(geolocation)
    
    // 增加定位重试机制
    let retryCount = 0
    const maxRetries = 3
    
    const getLocationWithRetry = () => {
      geolocation.getCurrentPosition((status, result) => {
        if (status === 'complete' && result.accuracy < 50) {
          // 精度小于50米时接受
          userLocation.value = {
            latitude: result.position.lat,
            longitude: result.position.lng
          }
          verifyLocation()
        } else if (retryCount < maxRetries) {
          retryCount++
          setTimeout(getLocationWithRetry, 2000)
        } else {
          locationStatus.value = "无法获取精确位置"
          locationStatusType.value = "error"
        }
      })
    }
    
    getLocationWithRetry()

    // 监听地图点击事件
    map.value.on('click', (e) => {
      userLocation.value = {
        latitude: e.lnglat.lat,
        longitude: e.lnglat.lng
      }
      verifyLocation()
    })
  } catch (error) {
    console.error('地图加载失败:', error)
  }
}

// 获取地理位置
const getLocation = () => {
  if (!navigator.geolocation) {
    locationStatus.value = "浏览器不支持地理位置功能"
    locationStatusType.value = "error"
    return
  }

  let retryCount = 0
  const maxRetries = 3
  
  const tryGetLocation = () => {
  navigator.geolocation.getCurrentPosition(
    (position) => {
      if (position.coords.accuracy < 50) {
        userLocation.value = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude
        }
        verifyLocation()
      } else if (retryCount < maxRetries) {
        retryCount++
        setTimeout(tryGetLocation, 2000)
      } else {
        locationStatus.value = "无法获取精确位置"
        locationStatusType.value = "error"
      }
    },
    (error) => {
      if (error.code === error.PERMISSION_DENIED) {
        locationStatus.value = "位置权限被拒绝，请开启权限"
        locationStatusType.value = "error"
      } else if (error.code === error.POSITION_UNAVAILABLE) {
        locationStatus.value = "无法获取位置信息，请检查设备定位服务"
        locationStatusType.value = "error"
      } else if (error.code === error.TIMEOUT) {
        locationStatus.value = "获取位置超时，请重试"
        locationStatusType.value = "error"
      }

      if (retryCount < maxRetries) {
        retryCount++
        setTimeout(tryGetLocation, 2000)
      } else {
        locationStatus.value = "无法获取位置信息"
        locationStatusType.value = "error"
        console.error("获取位置失败:", error)
      }
    },
    {
      enableHighAccuracy: true,
      timeout: 30000,  // 进一步延长超时时间
      maximumAge: 0,
      desiredAccuracy: 50,  // 降低精度要求
      requireAltitude: false,
      requireHeading: false,
      requireSpeed: false
    }
  )
}
  
  tryGetLocation()
}

// 获取课程信息和允许的地理位置范围
const fetchCourseAndLocationInfo = async () => {
  try {
    const token = localStorage.getItem('token')
    const [courseResponse, locationResponse] = await Promise.all([
      fetch(`${config.apiBaseUrl}${config.apiEndpoints.student.courses}`, {
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        }
      }),
      fetch(`${config.apiBaseUrl}${config.apiEndpoints.student.location}`, {
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        }
      })
    ])
    
    const [courseData, locationData] = await Promise.all([
      courseResponse.json(),
      locationResponse.json()
    ])
    
    courseInfo.value = courseData[0] // 假设学生只有一个当前课程
    allowedLocation.value = locationData
  } catch (error) {
    console.error('获取课程或位置信息失败:', error)
    locationStatus.value = "获取位置信息失败"
    locationStatusType.value = "error"
  }
}

// 验证位置是否在允许范围内
const verifyLocation = () => {
  if (!allowedLocation.value || !userLocation.value) return

  const distance = calculateDistance(
    userLocation.value.latitude,
    userLocation.value.longitude,
    allowedLocation.value.latitude,
    allowedLocation.value.longitude
  )

  if (distance <= allowedLocation.value.radius) {
    locationStatus.value = "位置验证通过"
    locationStatusType.value = "success"
  } else {
    locationStatus.value = `当前位置超出允许范围（距离${distance.toFixed(0)}米）`
    locationStatusType.value = "error"
  }
}

// 计算两点间距离（米）
const calculateDistance = (lat1, lon1, lat2, lon2) => {
  const R = 6371e3 // 地球半径（米）
  const φ1 = lat1 * Math.PI/180
  const φ2 = lat2 * Math.PI/180
  const Δφ = (lat2-lat1) * Math.PI/180
  const Δλ = (lon2-lon1) * Math.PI/180

  const a = Math.sin(Δφ/2) * Math.sin(Δφ/2) +
            Math.cos(φ1) * Math.cos(φ2) *
            Math.sin(Δλ/2) * Math.sin(Δλ/2)
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))

  return R * c
}

// 启动摄像头
const startCamera = async () => {
  try {
    const constraints = {
      video: { facingMode: isFrontCamera.value ? "user" : "environment" },
    }
    mediaStream.value = await navigator.mediaDevices.getUserMedia(constraints)
    video.value.srcObject = mediaStream.value
  } catch (error) {
    console.error("无法访问摄像头:", error)
    recognitionResult.value = "无法访问摄像头，请检查权限。"
  }
}

// 切换摄像头
const switchCamera = async () => {
  if (mediaStream.value) {
    mediaStream.value.getTracks().forEach((track) => track.stop())
  }
  isFrontCamera.value = !isFrontCamera.value
  await startCamera()
}

// 开始人脸识别
const startRecognition = async () => {
  if (locationStatusType.value !== "success") {
    recognitionResult.value = "请先通过位置验证"
    return
  }

  try {
    isLoading.value = true
    const context = canvas.value.getContext("2d")
    canvas.value.width = video.value.videoWidth
    canvas.value.height = video.value.videoHeight
    context.drawImage(video.value, 0, 0, canvas.value.width, canvas.value.height)
    
    // 提交带地理位置的考勤记录
    const token = localStorage.getItem('token')
    const response = await fetch(`${config.apiBaseUrl}${config.apiEndpoints.student.attendance}`, {
      method: 'POST',
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        course_id: courseInfo.value.id,
        status: 'present',
        recognition_data: canvas.value.toDataURL(),
        location: {
          latitude: userLocation.value.latitude,
          longitude: userLocation.value.longitude
        }
      })
    })
    
    if (!response.ok) throw new Error('考勤提交失败')
    
    recognitionResult.value = "识别成功！考勤已记录"
  } catch (error) {
    console.error('考勤提交失败:', error)
    recognitionResult.value = "考勤提交失败，请稍后重试"
  } finally {
    isLoading.value = false
  }
}

// 组件挂载时启动摄像头、获取位置和课程信息
onMounted(() => {
  startCamera()
  getLocation()
  fetchCourseAndLocationInfo()
  initMap()
})

// 复制坐标到剪贴板
const copyCoordinates = () => {
  const text = `${userLocation.value.latitude.toFixed(6)},${userLocation.value.longitude.toFixed(6)}`
  navigator.clipboard.writeText(text)
    .then(() => {
      ElMessage.success('坐标已复制到剪贴板')
    })
    .catch(() => {
      ElMessage.error('复制失败')
    })
}

// 组件卸载时关闭摄像头
onBeforeUnmount(() => {
  if (mediaStream.value) {
    mediaStream.value.getTracks().forEach((track) => track.stop())
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
  height: 100%;
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

.camera-video {
  width: 100%;
  max-width: 640px;
  border-radius: 8px;
  margin-bottom: 20px;
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
