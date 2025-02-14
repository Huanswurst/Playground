<template>
  <div class="app">
    <h1>AI对话助手</h1>
    <div class="chat-container">
      <div class="messages">
        <div v-for="(msg, index) in conversation" :key="index" :class="['message', msg.role]">
          <div class="avatar">
            <el-icon v-if="msg.role === 'user'"><User /></el-icon>
            <el-icon v-if="msg.role === 'assistant'"><Robot /></el-icon>
          </div>
          <div class="content">{{ msg.content }}</div>
        </div>
        <div v-if="isLoading" class="loading">AI正在思考...</div>
      </div>

      <div class="input-area">
        <el-input
          v-model="inputMessage"
          placeholder="输入你的问题..."
          @keyup.enter="handleSend"
          :disabled="isLoading"
        />
        <el-button type="primary" @click="handleSend" :loading="isLoading">发送</el-button>
      </div>

      <div class="config">
        <el-input v-model="apiEndpoint" placeholder="API地址" />
        <el-input v-model="apiKey" type="password" placeholder="API密钥" show-password />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import axios from 'axios'
import { ElIcon } from 'element-plus'
import { User, Robot } from '@element-plus/icons-vue'

// 状态管理
const conversation = ref(JSON.parse(localStorage.getItem('conversation')) || [])
const isLoading = ref(false)
const apiKey = ref(localStorage.getItem('apiKey') || '')
const apiEndpoint = ref(localStorage.getItem('apiEndpoint') || 'https://api.openai.com/v1/chat/completions')
const inputMessage = ref('')

// 持久化存储
watch([apiKey, apiEndpoint], ([newKey, newEndpoint]) => {
  localStorage.setItem('apiKey', newKey)
  localStorage.setItem('apiEndpoint', newEndpoint)
})

watch(conversation, (newVal) => {
  localStorage.setItem('conversation', JSON.stringify(newVal))
}, { deep: true })

// 流式请求处理
const handleSend = async () => {
  if (!inputMessage.value.trim()) return
  isLoading.value = true
  conversation.value.push({ role: 'user', content: inputMessage.value })
  
  try {
    const controller = new AbortController()
    const response = await fetch(apiEndpoint.value, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey.value}`
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
          const content = parsed.choices[0].delta.content
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
    console.error('API错误:', error)
    conversation.value.push({ role: 'assistant', content: '请求失败，请检查配置' })
  } finally {
    isLoading.value = false
    inputMessage.value = ''
  }
}
</script>

<style>
.app {
  font-family: Arial, sans-serif;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.chat-container {
  border: 1px solid #ebeef5;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
}

.messages {
  height: 60vh;
  overflow-y: auto;
  margin-bottom: 20px;
  padding: 10px;
  background: #fafafa;
  border-radius: 8px;
}

.message {
  display: flex;
  margin: 15px 0;
  gap: 12px;
}

.message.user {
  flex-direction: row-reverse;
}

.avatar {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.content {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 8px;
  line-height: 1.6;
}

.assistant .content {
  background: white;
  border: 1px solid #e0e0e0;
}

.user .content {
  background: #409eff;
  color: white;
}

.input-area {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.config {
  margin-top: 20px;
  background: #f5f7fa;
  padding: 15px;
  border-radius: 8px;
}

.config .el-input {
  margin-bottom: 10px;
}

.loading {
  color: #666;
  text-align: center;
  padding: 10px;
}
</style>
