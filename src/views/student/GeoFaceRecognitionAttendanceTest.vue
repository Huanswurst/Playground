<template>
  <div class="chat-container">
    <div class="messages">
      <div v-for="(msg, index) in history" :key="index" :class="['message', msg.role]">
        <div class="avatar">
          <span v-if="msg.role === 'user'">👤</span>
          <span v-else>🤖</span>
        </div>
        <div class="content">{{ msg.content }}</div>
      </div>
      <div v-if="loading" class="loading">AI正在生成...</div>
    </div>

    <div class="input-area">
      <input
        v-model="input"
        placeholder="输入您的问题"
        @keyup.enter="sendMessage"
        :disabled="loading"
      />
      <button @click="sendMessage" :disabled="loading">
        {{ loading ? '生成中...' : '发送' }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      history: JSON.parse(localStorage.getItem('chatHistory')) || [],
      input: '',
      loading: false,
      controller: null
    }
  },
  methods: {
    async sendMessage() {
      if (!this.input.trim() || this.loading) return
      
      this.loading = true
      this.history.push({ role: 'user', content: this.input })
      this.history.push({ role: 'assistant', content: '' })
      
      try {
        this.controller = new AbortController()
        const response = await fetch('https://www.huanswurst.top/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            messages: [
              {
                role: "system",
                content: ""
              },
              ...this.history.filter(m => m.role !== 'assistant')
            ],
            stream: true
          }),
          signal: this.controller.signal
        })

        const reader = response.body.getReader()
        const decoder = new TextDecoder()
        let assistantIndex = this.history.length - 1

        while (true) {
          const { done, value } = await reader.read()
          if (done) break
          
          const chunk = decoder.decode(value)
          const lines = chunk.split('\n').filter(l => l.startsWith('data: '))
          
          lines.forEach(line => {
            try {
              const data = JSON.parse(line.replace('data: ', ''))
              if (data.choices?.[0]?.delta?.content) {
                this.history[assistantIndex].content += data.choices[0].delta.content
              }
            } catch (e) {
              console.warn('解析错误:', e)
            }
          })
        }
      } catch (error) {
        if (error.name !== 'AbortError') {
          this.history[assistantIndex].content = '请求失败，请重试'
        }
      } finally {
        this.loading = false
        this.input = ''
        localStorage.setItem('chatHistory', JSON.stringify(this.history))
      }
    }
  },
  beforeUnmount() {
    if (this.controller) {
      this.controller.abort()
    }
  }
}
</script>

<style>
.chat-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.messages {
  height: 60vh;
  overflow-y: auto;
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
}

.message {
  display: flex;
  gap: 12px;
  margin: 15px 0;
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
  flex-shrink: 0;
}

.content {
  max-width: 70%;
  padding: 12px;
  border-radius: 12px;
  line-height: 1.6;
}

.message.user .content {
  background: #409eff;
  color: white;
}

.message.assistant .content {
  background: #f8f9fa;
  border: 1px solid #eee;
}

.input-area {
  display: flex;
  gap: 10px;
}

input {
  flex: 1;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
}

button {
  padding: 12px 24px;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

button:disabled {
  background: #a0cfff;
  cursor: not-allowed;
}

.loading {
  color: #666;
  text-align: center;
  padding: 10px;
}
</style>
