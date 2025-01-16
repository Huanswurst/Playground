import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // 确保导入路由
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import config from './config';


const app = createApp(App);
app.use(ElementPlus);
app.use(router); // 使用路由
app.mount('#app');
