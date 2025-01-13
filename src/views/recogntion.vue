<template>
  <el-container class="dashboard-container" :class="{ mobile: isMobile }">
    <el-header class="dashboard-header">
      <h1>考勤系统 - 实时摄像头识别</h1>
    </el-header>
    <el-main>
      <el-row :gutter="isMobile ? 10 : 20">
        <el-col :span="isMobile ? 24 : 12">
          <el-card class="camera-card" shadow="hover">
            <template #header>
              <span>摄像头画面</span>
            </template>
            <video ref="video" autoplay :style="{ width: isMobile ? '100%' : '100%' }"></video>
            <el-divider />
            <div class="camera-actions">
              <el-button type="primary" @click="startCamera">启动摄像头</el-button>
              <el-button type="danger" @click="stopCamera">关闭摄像头</el-button>
              <el-button type="success" @click="captureAndRecognize">拍照并识别</el-button>
            </div>
          </el-card>
        </el-col>
        <el-col :span="isMobile ? 24 : 12">
          <el-card class="result-card" shadow="hover">
            <template #header>
              <span>识别结果</span>
            </template>
            <div v-if="capturedImage">
              <img :src="capturedImage" alt="捕获的图像" :style="{ width: isMobile ? '100%' : '100%' }" />
            </div>
            <div v-else>
              <p>请拍照以进行识别</p>
            </div>
            <el-divider />
            <div v-if="attendanceResult">
              <h3>考勤结果</h3>
              <p>{{ attendanceResult }}</p>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';

export default {
  setup() {
    const video = ref(null); // 视频元素
    const capturedImage = ref(''); // 捕获的图像
    const attendanceResult = ref(''); // 考勤结果
    const isMobile = ref(false); // 是否移动端
    let mediaStream = null; // 摄像头流

    // 启动摄像头
    const startCamera = async () => {
      try {
        mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.value.srcObject = mediaStream;
      } catch (error) {
        console.error('无法访问摄像头:', error);
        ElMessage.error('无法访问摄像头，请检查权限');
      }
    };

    // 关闭摄像头
    const stopCamera = () => {
      if (mediaStream) {
        mediaStream.getTracks().forEach(track => track.stop());
        video.value.srcObject = null;
        mediaStream = null;
      }
    };

    // 拍照并识别
    const captureAndRecognize = () => {
      if (!video.value) return;

      // 创建 canvas 元素
      const canvas = document.createElement('canvas');
      canvas.width = video.value.videoWidth;
      canvas.height = video.value.videoHeight;
      const context = canvas.getContext('2d');

      // 将视频帧绘制到 canvas 上
      context.drawImage(video.value, 0, 0, canvas.width, canvas.height);

      // 将 canvas 图像转换为 base64
      capturedImage.value = canvas.toDataURL('image/png');

      // 调用识别逻辑
      recognizeImage(capturedImage.value);
    };

    // 模拟图像识别逻辑
    const recognizeImage = (imageData) => {
      // 这里可以调用图像识别 API
      setTimeout(() => {
        attendanceResult.value = '识别成功：张三，已签到';
      }, 1000);
    };

    // 检测设备类型
    const checkDevice = () => {
      isMobile.value = window.innerWidth <= 768;
    };

    // 组件挂载时检测设备
    onMounted(() => {
      checkDevice();
      window.addEventListener('resize', checkDevice);
    });

    // 组件卸载时关闭摄像头
    onUnmounted(() => {
      stopCamera();
      window.removeEventListener('resize', checkDevice);
    });

    return {
      video,
      capturedImage,
      attendanceResult,
      isMobile,
      startCamera,
      stopCamera,
      captureAndRecognize,
    };
  },
};
</script>

<style scoped>
/* 容器样式 */
.dashboard-container {
  height: 100vh; /* 确保容器占满整个视口高度 */
  display: flex;
  flex-direction: column;
}

/* 头部样式 */
.dashboard-header {
  background-color: #409eff;
  color: white;
  text-align: center;
  line-height: 60px;
  font-size: 24px;
  font-weight: bold;
  padding: 0 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

/* 主体内容样式 */
.el-main {
  flex: 1; /* 让 main 部分占据剩余空间 */
  padding: 20px;
  background-color: #f5f7fa;
}

/* 摄像头卡片样式 */
.camera-card {
  border-radius: 12px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  margin-bottom: 10px;
}

.camera-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

/* 识别结果卡片样式 */
.result-card {
  border-radius: 12px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  margin-bottom: 10px;
}

.result-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

/* 摄像头操作按钮布局 */
.camera-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

/* 移动端样式 */
@media (max-width: 768px) {
  .dashboard-container.mobile .el-main {
    padding: 10px; /* 移动端减少内边距 */
  }

  .camera-card,
  .result-card {
    border-radius: 16px; /* 移动端卡片圆角更大 */
    margin-bottom: 15px; /* 移动端卡片间距更大 */
  }

  .camera-actions {
    flex-direction: column; /* 按钮垂直排列 */
  }

  .camera-actions .el-button {
    width: 100%; /* 按钮占满宽度 */
  }
}
</style>
