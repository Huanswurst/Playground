<template>
  <div class="chat-container">
    <!-- 操作按钮区域 -->
    <div class="action-buttons">
      <button @click="clearHistory" class="btn-clear">清除历史</button>
      <button 
        @click="stopGeneration" 
        class="btn-stop"
        v-if="isLoading"
      >
        停止生成
      </button>
    </div>

    <!-- 消息展示区域 -->
    <div class="messages">
      <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.role]">
        <div class="avatar">
          <span v-if="msg.role === 'user'">👤</span>
          <span v-else>🤖</span>
        </div>
        <div class="content">{{ msg.content }}</div>
      </div>
      <div v-if="isLoading" class="loading">AI正在思考中...</div>
    </div>

    <!-- 输入区域 -->
    <div class="input-area">
      <input
        v-model="inputText"
        placeholder="输入您的问题..."
        @keyup.enter="sendMessage"
        :disabled="isLoading"
      />
      <button 
        @click="sendMessage" 
        :disabled="isLoading"
        class="btn-send"
      >
        {{ isLoading ? '发送中...' : '发送' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 状态管理
const messages = ref(JSON.parse(localStorage.getItem('chatHistory')) || [])
const inputText = ref('')
const isLoading = ref(false)
const controller = ref(null)

// 清除历史记录
const clearHistory = () => {
  messages.value = []
  localStorage.removeItem('chatHistory')
  showToast('历史记录已清除')
}

// 停止生成
const stopGeneration = () => {
  if (controller.value) {
    controller.value.abort()
    isLoading.value = false
    showToast('已停止生成')
  }
}

// 显示临时提示
const showToast = (text) => {
  const toast = document.createElement('div')
  toast.className = 'toast-message'
  toast.textContent = text
  document.body.appendChild(toast)
  
  setTimeout(() => {
    toast.remove()
  }, 2000)
}

// 发送消息
const sendMessage = async () => {
  if (!inputText.value.trim() || isLoading.value) return

  try {
    isLoading.value = true
    messages.value.push({ role: 'user', content: inputText.value })
    messages.value.push({ role: 'assistant', content: '' })
    const messageIndex = messages.value.length - 1

    controller.value = new AbortController()
    
    const response = await fetch('/api/chat-stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        messages: messages.value.slice(0, -1)
      }),
      signal: controller.value.signal
    })

    const reader = response.body.getReader()
    const decoder = new TextDecoder()

    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      
      const chunk = decoder.decode(value, { stream: true })
      processChunk(chunk, messageIndex)
    }

  } catch (error) {
    handleError(error, messageIndex)
  } finally {
    finalizeRequest(messageIndex)
  }
}

// 处理数据块
const processChunk = (chunk, messageIndex) => {
  chunk.split('\n\n').forEach(line => {
    if (!line.startsWith('data: ')) return
    try {
      const data = JSON.parse(line.replace('data: ', ''))
      if (data.choices?.[0]?.delta?.content) {
        messages.value[messageIndex].content += data.choices[0].delta.content
      }
    } catch (e) {
      console.warn('数据解析错误:', e)
    }
  })
}

// 错误处理
const handleError = (error, messageIndex) => {
  if (error.name !== 'AbortError') {
    messages.value[messageIndex].content = '❌ 请求失败: ' + error.message
  }
}

// 结束请求处理
const finalizeRequest = (messageIndex) => {
  isLoading.value = false
  inputText.value = ''
  controller.value = null
  saveHistory()
  
  // 自动滚动到底部
  setTimeout(() => {
    const container = document.querySelector('.messages')
    container.scrollTop = container.scrollHeight
  }, 100)
}

// 保存历史记录
const saveHistory = () => {
  localStorage.setItem('chatHistory', JSON.stringify(
    messages.value.filter(m => m.content.trim())
  ))
}
</script>

<style>
/* 新增样式 */
.action-buttons {
  margin-bottom: 1rem;
  display: flex;
  gap: 10px;
}

.btn-clear, .btn-stop {
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn-clear {
  background: #ff4757;
  color: white;
}

.btn-stop {
  background: #ffa502;
  color: white;
}

.btn-clear:hover, .btn-stop:hover {
  opacity: 0.9;
}

.toast-message {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0,0,0,0.8);
  color: white;
  padding: 12px 24px;
  border-radius: 25px;
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from { bottom: -50px; }
  to { bottom: 20px; }
}

/* 原有样式优化 */
.input-area {
  display: flex;
  gap: 10px;
  margin-top: 1rem;
}

input {
  flex: 1;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.btn-send {
  padding: 12px 24px;
  background: #2ed573;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.messages {
  height: 60vh;
  overflow-y: auto;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}
</style>
