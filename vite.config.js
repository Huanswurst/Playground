import { fileURLToPath, URL } from 'node:url';
import { defineConfig } from 'vite';
import VueDevTools from 'vite-plugin-vue-devtools';
import vue from '@vitejs/plugin-vue';
import fs from 'fs'; // 导入 fs 模块
import path from 'path'; // 导入 path 模块

// https://vite.dev/config/s
export default defineConfig({
  plugins: [
    VueDevTools(),
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
server: {
  host: '0.0.0.0', // 允许外部访问
  port: 5173, // 使用 HTTP 端口
  hmr: {
    host: 'huanswurst.top', // 允许的域名
    port: 5173, // 确保端口一致
    protocol: 'wss', // 使用 WebSocket Secure
  },
},
define: {
  'process.env': {
    VITE_AMAP_KEY: JSON.stringify(env.VITE_AMAP_KEY)
  }
}

});