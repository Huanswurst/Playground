<template>
  <el-footer class="footer">
    <div class="copyright-container">
      <div class="copyright">
        <span>基于图像识别的考勤系统 © 2025</span>
        <el-divider direction="vertical" />
        <el-link 
          type="primary" 
          href="https://beian.miit.gov.cn" 
          target="_blank"
        >
          苏ICP备2025157736号-1
        </el-link>
      </div>
    </div>
  </el-footer>
</template>

<script setup>
import { ElFooter, ElDivider, ElLink } from 'element-plus'
</script>

<style scoped>
.footer {
  position: fixed;
  bottom: 0;
  width: 100%;
  height: 60px;
  background-color: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
