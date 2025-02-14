<template>
  <div class="chat-wrapper">
    <!-- 聊天容器 -->
    <div ref="chatContainer" class="nlux-container"></div>
  </div>
</template>

<script>
export default {
  name: 'ChatInterface',
  mounted() {
    this.initNLUX();
  },
  methods: {
    async initNLUX() {
      // 确保只加载一次
      if (window.nluxLoaded) return;
      window.nluxLoaded = true;

      // 动态加载样式
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = 'https://g.alicdn.com/aliyun-documentation/web-chatbot-ui/0.0.24/index.css';
      link.crossOrigin = 'anonymous';
      document.head.appendChild(link);

      // 配置需要在脚本加载前设置
      window.CHATBOT_CONFIG = {
        endpoint: "/chat",
        displayByDefault: true,
        aiChatOptions: {
          conversationOptions: {
            conversationStarters: [
              { prompt: '哪款手机续航最长？' },
              { prompt: '你们有哪些手机型号？' },
              { prompt: '有折叠屏手机吗?' },
            ]
          },
          displayOptions: { 
            height: "100%",
            width: "100%",
            // 启用交互模式
            interactionMode: 'full'
          },
          personaOptions: {
            assistant: {
              name: 'AI 助手',
              avatar: 'https://img.alicdn.com/imgextra/i2/O1CN01Pda9nq1YDV0mnZ31H_!!6000000003025-54-tps-120-120.apng',
              tagline: '欢迎提问！'
            }
          }
        }
      };

      try {
        // 动态加载SDK
        await this.loadScript('https://g.alicdn.com/aliyun-documentation/web-chatbot-ui/0.0.24/index.js');
        
        // 等待DOM更新
        await this.$nextTick();
        
        // 显式初始化（假设SDK需要手动初始化）
        if (typeof window.initWebChat === 'function') {
          window.initWebChat({
            container: this.$refs.chatContainer,
            onMessage: this.handleMessage
          });
        }
      } catch (error) {
        console.error('NLUX初始化失败:', error);
      }
    },

    loadScript(src) {
      return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.type = 'module';
        script.src = src;
        script.crossOrigin = 'anonymous';
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
      });
    },

    // 消息处理
    handleMessage(message) {
      this.$emit('message', message);
    }
  },

  beforeDestroy() {
    // 清理工作
    if (window.CHATBOT_CONFIG) {
      delete window.CHATBOT_CONFIG;
    }
    const elements = document.querySelectorAll('[src*="webchatbot-ui"]');
    elements.forEach(el => el.remove());
  }
}
</script>

<style scoped>
.chat-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 9999;
}

/* 深度样式穿透 */
::v-deep .nlux-chat-container {
  height: 100vh !important;
  width: 100vw !important;
  max-width: none !important;
  border: none !important;
  box-shadow: none !important;
}

::v-deep .chat-input-area {
  border-top: 1px solid #eee !important;
}

::v-deep .send-button {
  background-color: #1464E4 !important;
}

/* 隐藏浮动按钮 */
::v-deep .webchat-bubble-tip {
  display: none !important;
}
</style>
