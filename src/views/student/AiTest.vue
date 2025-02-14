<template>
  <!-- 创建挂载点 -->
  <div ref="chatContainer" class="fullscreen-chat"></div>
</template>

<script>
export default {
  mounted() {
    // 动态创建样式表
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.crossOrigin = true;
    link.href = 'https://g.alicdn.com/aliyun-documentation/web-chatbot-ui/0.0.24/index.css';
    document.head.appendChild(link);

    // 动态创建脚本
    const script = document.createElement('script');
    script.type = 'module';
    script.crossOrigin = true;
    script.src = 'https://g.alicdn.com/aliyun-documentation/web-chatbot-ui/0.0.24/index.js';
    
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
          height: "100vh",
          width: "100vw"
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

    script.onload = () => {
      // 确保 DOM 已渲染
      this.$nextTick(() => {
        // 如果 SDK 需要初始化调用
        if (window.initWebChat) {
          window.initWebChat({
            container: this.$refs.chatContainer
          });
        }
      });
    };

    document.head.appendChild(script);
  },
  beforeDestroy() {
    // 清理全局变量
    delete window.CHATBOT_CONFIG;
    // 移除动态添加的元素
    const elements = document.querySelectorAll('[src*="webchatbot-ui"]');
    elements.forEach(el => el.remove());
  }
}
</script>

<style scoped>
.fullscreen-chat {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 9999;
}

/* 深度样式覆盖 */
::v-deep .webchat-bubble-tip {
  display: none !important;
}

::v-deep .webchat-container {
  height: 100vh !important;
  width: 100vw !important;
}
</style>
