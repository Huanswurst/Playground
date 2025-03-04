
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import config from './config';

// 加载环境变量
import.meta.env.VITE_API_BASE_URL = process.env.API_BASE_URL;

const app = createApp(App);
const pinia = createPinia();

// 全局配置
app.config.globalProperties.$config = config;

// 全局错误处理
app.config.errorHandler = (err, vm, info) => {
  console.error('Global error:', err);
  console.log('Component:', vm);
  console.log('Error info:', info);
};

app.use(pinia);
app.use(ElementPlus);
app.use(router);
app.mount('#app');
