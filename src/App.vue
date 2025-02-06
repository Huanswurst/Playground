<template>
  <router-view />
</template>

<script setup>
</script>

<style>
/* 导入字体 */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');

#app {
  font-family: 'Source Han Sans CN', 'PingFang SC', 'Microsoft YaHei', 'Inter', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;  color: #2c3e50;
}

/* 定义字体层级 */
:root {
  --font-primary: 'Source Han Sans CN', sans-serif;
  --font-secondary: 'Inter', sans-serif;
}

/* 标题字体 */
h1, h2, h3 {
  font-family: var(--font-primary);
  font-weight: 500;
}

/* 正文字体 */
body {
  font-family: var(--font-primary);
  font-weight: 400;
}

/* 代码和数字字体 */
code, .number {
  font-family: var(--font-secondary);
  font-weight: 500;
}

/* 响应式字体大小 */
@media screen and (max-width: 768px) {
  html {
    font-size: 14px;
  }
}
</style>
