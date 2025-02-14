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

const messages = ref([])
const inputText = ref('')
const isLoading = ref(false)
const controller = ref(null)

async function sendMessage() {
  if (!inputText.value.trim() || isLoading.value) return
  
  try {
    isLoading.value = true
    const userMessage = { role: 'user', content: inputText.value }
    messages.value.push(userMessage)
    
    // 添加loading状态消息
    const assistantMessage = { role: 'assistant', content: '', loading: true }
    messages.value.push(assistantMessage)
    const messageIndex = messages.value.length - 1

    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        messages: [userMessage],
        stream: false // 明确要求非流式响应
      })
    })

    // 处理标准响应
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
    
    const data = await response.json()
    const content = data.choices[0].message.content
    
    // 直接更新消息内容
    messages.value[messageIndex] = {
      ...assistantMessage,
      content: content,
      loading: false
    }

  } catch (error) {
    messages.value[messageIndex] = {
      ...assistantMessage,
      content: '❌ 请求失败: ' + error.message,
      loading: false
    }
  } finally {
    isLoading.value = false
    inputText.value = ''
    saveHistory()
  }
}

// 保存历史（保持原有实现）
const saveHistory = () => {
  localStorage.setItem('chatHistory', JSON.stringify(
    messages.value.filter(m => !m.loading)
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
