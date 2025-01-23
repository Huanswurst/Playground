<template>
  <el-footer class="footer">
    <div class="footer-content">
      <p class="text">© 2025 Your Company. All rights reserved.</p>
      <el-link 
        class="icp"
        type="info"
        :underline="false"
        href="https://beian.miit.gov.cn" 
        target="_blank">
        苏ICP备2025157736号-1
      </el-link>
    </div>
  </el-footer>
</template>

<script>
export default {
  name: 'FooterComponent'
}
</script>

<style scoped>
.footer {
  --el-footer-padding: 20px 0;
  text-align: center;
  background-color: var(--el-bg-color-page);
  border-top: 1px solid var(--el-border-color-light);
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
}

.text {
  color: var(--el-text-color-regular);
  font-size: 14px;
  margin-bottom: 8px;
}

.icp {
  font-size: 12px;
}
</style>
