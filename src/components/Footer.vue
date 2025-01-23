<template>
  <footer class="footer">
    <div class="footer-content">
      <a href="https://beian.miit.gov.cn" target="_blank">苏ICP备2025157736号-1</a>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'AppFooter'
}
</script>

<style scoped>
.footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 50px;
  background-color: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
}

.footer-content {
  text-align: center;
}

.footer a {
  color: #666;
  text-decoration: none;
}

.footer a:hover {
  color: #333;
}
</style>
