<template>
  <!-- 模板部分保持不变 -->
  <!-- ... -->
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { Calendar, Switch, Camera } from '@element-plus/icons-vue'
import AMapLoader from '@amap/amap-jsapi-loader'

const AMAP_KEY = 'ff4dd4814f31d1e9122f1032f39ce9d9'
const AMAP_SECRET = '7dbd1d0587367322e8856f37dc33299d'

// 其他ref变量保持不变
// ...

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

    // 添加工具栏
    map.value.addControl(new AMap.ToolBar({
      position: 'RB',
      offset: [10, 40]
    }))

    // 添加定位控件
    const geolocation = new AMap.Geolocation({
      enableHighAccuracy: true,
      timeout: 5000,
      showButton: true,
      position: 'LB',
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
      }
    })
    map.value.addControl(geolocation)

    isMapLoading.value = false
    resolve(map.value)
  })
}

const getLocationByAMap = (AMap) => {
  return new Promise((resolve, reject) => {
    if (!AMap || !AMap.Geolocation) {
      reject(new Error('高德地图 API 未加载或版本不兼容'))
      return
    }

    const geolocation = new AMap.Geolocation({
      enableHighAccuracy: true,
      timeout: 5000,
      showButton: false,
    })

    // 添加标记点
    const marker = new AMap.Marker({
      position: [116.397428, 39.90923],
      icon: 'https://webapi.amap.com/theme/v1.3/markers/n/mark_b.png',
      offset: new AMap.Pixel(-13, -30)
    })

    // 实时定位
    geolocation.watchPosition((status, result) => {
      if (status === 'complete') {
        const { latitude, longitude } = result.position
        userLocation.value = { latitude, longitude }
        
        // 更新地图中心
        map.value.setCenter([longitude, latitude])
        
        // 更新标记点位置
        marker.setPosition([longitude, latitude])
        map.value.add(marker)
        
        resolve({ latitude, longitude })
      } else {
        console.error('获取位置失败:', result)
        reject(new Error(`获取位置失败: ${result.message}`))
      }
    })
  })
}

// 其他函数保持不变
// ...

onMounted(async () => {
  window._AMapSecurityConfig = {
    securityJsCode: AMAP_SECRET,
  }

  try {
    // 加载高德地图
    const AMap = await AMapLoader.load({
      key: AMAP_KEY,
      version: '2.0',
      plugins: ['AMap.Geolocation', 'AMap.ToolBar'],
    })

    // 初始化地图
    await initMap(AMap)

    // 获取地理位置
    const location = await getLocationByAMap(AMap)
    map.value.setCenter([location.longitude, location.latitude])

    // 验证位置
    verifyLocation()

    // 获取课程信息
    await fetchCourseAndLocationInfo()
  } catch (error) {
    console.error('地图或位置初始化失败:', error)
    locationStatus.value = '地图或位置初始化失败'
    locationStatusType.value = 'error'
  }

  // 启动摄像头（独立处理，不影响地图和位置逻辑）
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
/* ... */
</style>
