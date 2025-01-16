<template>
    <div class="attendance-page">
      <!-- 任务提示 -->
      <div class="task-prompt">
        <h2>{{ task }}</h2>
        <p>剩余时间：{{ countdown }}秒</p>
      </div>
  
      <!-- 实时摄像头画面 -->
      <div class="camera-section">
        <video ref="video" autoplay playsinline></video>
        <canvas ref="canvas" style="display: none;"></canvas>
        <div class="camera-controls">
          <button @click="switchCamera">切换摄像头</button>
          <button @click="capturePhoto">拍摄照片</button>
        </div>
      </div>
  
      <!-- 照片预览 -->
      <div v-if="imagePreview" class="image-preview">
        <img :src="imagePreview" alt="拍摄的照片" />
        <div class="preview-controls">
          <button @click="submitPhoto">提交照片</button>
          <button @click="retakePhoto">重拍</button>
        </div>
      </div>
  
      <!-- 反馈信息 -->
      <div v-if="feedback" class="feedback">
        <p>{{ feedback }}</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        task: "请拍摄黑板", // 教师发布的任务
        countdown: 300, // 倒计时（5分钟）
        imagePreview: null, // 照片预览的URL
        feedback: "", // 提交后的反馈信息
        timer: null, // 倒计时计时器
        mediaStream: null, // 摄像头流
        isFrontCamera: false, // 是否使用前置摄像头
      };
    },
    mounted() {
      // 启动摄像头
      this.startCamera();
      // 启动倒计时
      this.startCountdown();
    },
    methods: {
      // 启动摄像头
      async startCamera() {
        try {
          const constraints = {
            video: { facingMode: this.isFrontCamera ? "user" : "environment" },
          };
          this.mediaStream = await navigator.mediaDevices.getUserMedia(constraints);
          this.$refs.video.srcObject = this.mediaStream;
        } catch (error) {
          console.error("无法访问摄像头:", error);
          this.feedback = "无法访问摄像头，请检查权限。";
        }
      },
  
      // 切换摄像头
      async switchCamera() {
        // 关闭当前摄像头
        if (this.mediaStream) {
          this.mediaStream.getTracks().forEach((track) => track.stop());
        }
        // 切换摄像头状态
        this.isFrontCamera = !this.isFrontCamera;
        // 重新启动摄像头
        await this.startCamera();
      },
  
      // 拍摄照片
      capturePhoto() {
        const video = this.$refs.video;
        const canvas = this.$refs.canvas;
        const context = canvas.getContext("2d");
  
        // 设置 canvas 尺寸与视频一致
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
  
        // 将视频画面绘制到 canvas 上
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
  
        // 生成照片预览
        this.imagePreview = canvas.toDataURL("image/png");
      },
  
      // 提交照片
      submitPhoto() {
        // 模拟图像识别逻辑
        const isSuccess = this.simulateImageRecognition();
        if (isSuccess) {
          this.feedback = "考勤成功！";
        } else {
          this.feedback = "未检测到黑板，请重新拍摄。";
        }
      },
  
      // 重拍照片
      retakePhoto() {
        this.imagePreview = null;
        this.feedback = "";
      },
  
      // 模拟图像识别
      simulateImageRecognition() {
        // 这里可以替换为实际的图像识别逻辑
        return Math.random() > 0.5; // 50% 的概率模拟成功
      },
  
      // 启动倒计时
      startCountdown() {
        this.timer = setInterval(() => {
          if (this.countdown > 0) {
            this.countdown--;
          } else {
            clearInterval(this.timer);
            this.feedback = "考勤时间已结束！";
            this.stopCamera(); // 倒计时结束后关闭摄像头
          }
        }, 1000);
      },
  
      // 关闭摄像头
      stopCamera() {
        if (this.mediaStream) {
          this.mediaStream.getTracks().forEach((track) => track.stop());
        }
      },
    },
    beforeUnmount() {
      // 清除计时器和摄像头
      clearInterval(this.timer);
      this.stopCamera();
    },
  };
  </script>
  
  <style>
  .attendance-page {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    text-align: center;
    font-family: Arial, sans-serif;
  }
  
  .task-prompt h2 {
    margin-bottom: 10px;
  }
  
  .camera-section video {
    width: 100%;
    max-width: 400px;
    border-radius: 10px;
    margin-bottom: 10px;
  }
  
  .camera-controls {
    display: flex;
    justify-content: space-around;
    margin-top: 10px;
  }
  
  .camera-controls button {
    padding: 10px 20px;
    font-size: 16px;
    background-color: #42b983;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .image-preview img {
    max-width: 100%;
    margin-top: 20px;
    border-radius: 10px;
  }
  
  .preview-controls {
    display: flex;
    justify-content: space-around;
    margin-top: 10px;
  }
  
  .preview-controls button {
    padding: 8px 16px;
    font-size: 14px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .preview-controls button:first-of-type {
    background-color: #42b983;
    color: white;
  }
  
  .preview-controls button:last-of-type {
    background-color: #ff4757;
    color: white;
  }
  
  .feedback {
    margin-top: 20px;
    font-size: 18px;
    color: #42b983;
  }
  </style>