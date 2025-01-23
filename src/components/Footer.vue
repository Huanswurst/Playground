<template>
  <footer class="footer">
    <div class="footer-content">
      <a href="https://beian.miit.gov.cn" target="_blank" rel="noopener noreferrer">
        苏ICP备2025157736号-1
      </a>
    </div>
  </footer>
</template>

<script setup>
</script>

<style scoped>
.footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 40px;
  background-color: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
  border-top: 1px solid #e4e7ed;
  z-index: 1000;
}

.footer-content {
  font-size: 14px;
  color: #606266;
}

.footer-content a {
  color: inherit;
  text-decoration: none;
}

.footer-content a:hover {
  color: #409eff;
}
</style>
