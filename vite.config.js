import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import VueDevTools from 'vite-plugin-vue-devtools'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    VueDevTools(),
    vue()
  ],
  define: {
    'process.env': {}
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    port: 5173,
    host: 'localhost', // 仅允许本地访问
    strictPort: true, // 如果端口被占用则报错
    hmr: {
      protocol: 'ws',
      host: 'localhost'
    }
  },
  build: {
    sourcemap: false, // 生产环境关闭sourcemap
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true, // 移除console.log
        drop_debugger: true // 移除debugger
      }
    }
  }
})
