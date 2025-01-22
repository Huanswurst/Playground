import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store/index.ts'
import config from './config'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)

// 全局配置
app.config.globalProperties.$http = config.apiClient
app.config.globalProperties.$apiEndpoints = config.apiEndpoints

// 全局错误处理
app.config.errorHandler = (err, vm, info) => {
  console.error('Global error:', err)
  store.commit('SET_ERROR', err.message)
}

// 使用插件
app.use(ElementPlus)
app.use(router)
app.use(store)

// 挂载应用
app.mount('#app')
