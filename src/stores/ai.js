import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getCurrentInstance } from 'vue'

export const useAIStore = defineStore('ai', () => {
  const { $config } = getCurrentInstance().appContext.config.globalProperties
  const apiClient = $config.apiClient

  const conversation = ref([])
  const isLoading = ref(false)

  const sendMessage = async (message) => {
    try {
      isLoading.value = true
      conversation.value.push({ role: 'user', content: message })

      const response = await apiClient.post('/chat', {
        message: message
      })

      conversation.value.push({ role: 'assistant', content: response.data.message })
    } catch (error) {
      console.error('Error sending message:', error)
      conversation.value.push({ role: 'assistant', content: '抱歉，出错了，请稍后再试' })
    } finally {
      isLoading.value = false
    }
  }

  return {
    conversation,
    isLoading,
    sendMessage
  }
})
