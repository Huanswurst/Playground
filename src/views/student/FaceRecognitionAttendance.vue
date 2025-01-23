import { ref, onBeforeUnmount } from 'vue'
import { Calendar, Switch, Camera } from '@element-plus/icons-vue'

// 声明 video 和 canvas 的引用
const video = ref(null)
const canvas = ref(null)

const mediaStream = ref(null)
const isFrontCamera = ref(false)
const recognitionResult = ref("")
const isLoading = ref(false)
const courseInfo = ref(null)
const attendanceStatus = ref(null)

// 获取课程信息
const fetchCourseInfo = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`${config.apiBaseUrl}${config.apiEndpoints.student.courses}`, {
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json'
      }
    })
    const data = await response.json()
    courseInfo.value = data[0] // 假设学生只有一个当前课程
  } catch (error) {
    console.error('获取课程信息失败:', error)
    recognitionResult.value = "获取课程信息失败，请稍后重试"
  }
}

// 启动摄像头
const startCamera = async () => {
  try {
    // 检查浏览器是否支持媒体设备
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      recognitionResult.value = "您的浏览器不支持摄像头访问"
      return
    }

    // 检查是否在HTTPS下运行
    if (window.location.protocol !== 'https:') {
      recognitionResult.value = "请确保在HTTPS环境下访问"
      return
    }

    const constraints = {
      video: { 
        facingMode: isFrontCamera.value ? "user" : "environment",
        width: { ideal: 1280 },
        height: { ideal: 720 }
      },
    }
    
    mediaStream.value = await navigator.mediaDevices.getUserMedia(constraints)
    video.value.srcObject = mediaStream.value // 使用 video.value 访问 DOM 元素
    
    // 添加摄像头状态监听
    mediaStream.value.getVideoTracks()[0].onended = () => {
      recognitionResult.value = "摄像头连接已断开"
    }
    
  } catch (error) {
    console.error("无法访问摄像头:", error)
    let errorMessage = "无法访问摄像头"
    
    if (error.name === 'NotAllowedError') {
      errorMessage = "请允许摄像头访问权限"
    } else if (error.name === 'NotFoundError') {
      errorMessage = "未找到可用的摄像头设备"
    } else if (error.name === 'NotReadableError') {
      errorMessage = "摄像头已被其他应用占用"
    } else if (error.name === 'OverconstrainedError') {
      errorMessage = "无法满足摄像头配置要求"
    }
    
    recognitionResult.value = errorMessage
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
  try {
    isLoading.value = true
    const context = canvas.value.getContext("2d")
    canvas.value.width = video.value.videoWidth
    canvas.value.height = video.value.videoHeight
    context.drawImage(video.value, 0, 0, canvas.value.width, canvas.value.height)
    
    // 提交考勤记录
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
        recognition_data: canvas.value.toDataURL()
      })
    })
    
    if (!response.ok) throw new Error('考勤提交失败')
    
    recognitionResult.value = "识别成功！考勤已记录"
    attendanceStatus.value = 'present'
  } catch (error) {
    console.error('考勤提交失败:', error)
    recognitionResult.value = "考勤提交失败，请稍后重试"
  } finally {
    isLoading.value = false
  }
}

// 组件挂载时启动摄像头并获取课程信息
startCamera()
fetchCourseInfo()

// 组件卸载时关闭摄像头
onBeforeUnmount(() => {
  if (mediaStream.value) {
    mediaStream.value.getTracks().forEach((track) => track.stop())
  }
})
