<template>
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
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAIStore } from '@/stores/ai'
import { User, Robot } from '@element-plus/icons-vue'
import { getCurrentInstance } from 'vue'

const aiStore = useAIStore()
const inputMessage = ref('')

// 获取全局配置
const { $config } = getCurrentInstance().appContext.config.globalProperties
const apiClient = $config.apiClient

const { conversation, isLoading } = aiStore

const handleSend = async () => {
  if (!inputMessage.value.trim()) return
  await aiStore.sendMessage(inputMessage.value)
  inputMessage.value = ''
}
</script>

<style scoped>
.chat-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.messages {
  height: 60vh;
  overflow-y: auto;
  margin-bottom: 20px;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 10px;
}

.message {
  display: flex;
  margin: 10px 0;
}

.message.user {
  flex-direction: row-reverse;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 10px;
}

.content {
  max-width: 70%;
  padding: 10px;
  border-radius: 8px;
}

.assistant .content {
  background: #f0f0f0;
}

.user .content {
  background: #409eff;
  color: white;
}

.input-area {
  display: flex;
  gap: 10px;
}
</style>
