<template>
  <div class="app">
    <h1>AI智能助手</h1>
    <div class="chat-container">
      <div class="messages">
        <div v-for="(msg, index) in conversation" :key="index" :class="['message', msg.role]">
          <div class="avatar">
            <el-icon v-if="msg.role === 'user'"><User /></el-icon>
            <el-icon v-if="msg.role === 'assistant'"><ChatLineRound /></el-icon>
          </div>
          <div class="content">{{ msg.content }}</div>
        </div>
        <div v-if="isLoading" class="loading">AI正在思考中...</div>
      </div>

      <div class="input-area">
        <el-input
          v-model="inputMessage"
          placeholder="输入您的问题..."
          @keyup.enter="handleSend"
          :disabled="isLoading"
        />
        <el-button type="primary" @click="handleSend" :loading="isLoading">发送</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { User, ChatLineRound } from '@element-plus/icons-vue'

// 固定API配置
const API_CONFIG = {
  apiKey: '1c2d1b65-e1bb-4a4a-8a07-6ed162435bde',
  baseURL: 'https://ark.cn-beijing.volces.com/api/v3'
}

// 对话状态
const conversation = ref(JSON.parse(localStorage.getItem('conversation')) || [])
const isLoading = ref(false)
const inputMessage = ref('')

// 初始化加载历史记录
onMounted(() => {
  const saved = localStorage.getItem('conversation')
  if (saved) conversation.value = JSON.parse(saved)
})

// 流式请求处理
const handleSend = async () => {
  if (!inputMessage.value.trim()) return
  isLoading.value = true
  conversation.value.push({ role: 'user', content: inputMessage.value })
  
  try {
    const controller = new AbortController()
    const response = await fetch(`${API_CONFIG.baseURL}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_CONFIG.apiKey}`
      },
      body: JSON.stringify({
        model: "gpt-3.5-turbo",
        messages: conversation.value,
        temperature: 0.7,
        stream: true
      }),
      signal: controller.signal
    })

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let aiResponseContent = ''
    conversation.value.push({ role: 'assistant', content: aiResponseContent })

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      const chunk = decoder.decode(value)
      const lines = chunk.split('\n').filter(line => line.trim() !== '')
      
      for (const line of lines) {
        const message = line.replace(/^data: /, '')
        if (message === '[DONE]') break
        
        try {
          const parsed = JSON.parse(message)
          const content = parsed.choices[0]?.delta?.content
          if (content) {
            aiResponseContent += content
            conversation.value[conversation.value.length - 1].content = aiResponseContent
          }
        } catch (err) {
          console.error('解析错误:', err)
        }
      }
    }
  } catch (error) {
    console.error('API请求失败:', error)
    conversation.value.push({ role: 'assistant', content: '服务暂时不可用，请稍后再试' })
  } finally {
    isLoading.value = false
    inputMessage.value = ''
    localStorage.setItem('conversation', JSON.stringify(conversation.value))
  }
}
</script>

<style>
.app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.chat-container {
  border: 1px solid #e4e7ed;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  background: white;
}

.messages {
  height: 60vh;
  overflow-y: auto;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.message {
  display: flex;
  margin: 1rem 0;
  gap: 1rem;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.message.user {
  flex-direction: row-reverse;
}

.avatar {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #409eff;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.assistant .avatar {
  background: #67c23a;
}

.content {
  max-width: 75%;
  padding: 12px 16px;
  border-radius: 12px;
  line-height: 1.6;
  font-size: 15px;
}

.assistant .content {
  background: white;
  border: 1px solid #e4e7ed;
  box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}

.user .content {
  background: #409eff;
  color: white;
  box-shadow: 0 2px 8px rgba(64,158,255,0.2);
}

.input-area {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.loading {
  color: #909399;
  text-align: center;
  padding: 1rem;
  font-size: 14px;
}

.el-input {
  flex-grow: 1;
}

.el-button {
  width: 100px;
}
</style>
