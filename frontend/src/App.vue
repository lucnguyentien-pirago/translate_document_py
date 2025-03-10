<template>
  <div class="min-h-screen flex flex-col">
    <Toast />
    <header class="bg-primary text-white py-4 px-8 shadow-md">
      <div class="text-center">
        <h1 class="text-3xl font-semibold m-0">Ứng dụng Dịch Tài liệu</h1>
        <p class="text-base mt-2 opacity-90">Dịch tài liệu từ nhiều ngôn ngữ sang tiếng Việt</p>
      </div>
    </header>
    <main class="flex-1 p-8 max-w-7xl mx-auto w-full">
      <router-view />
    </main>
    <footer class="bg-surface-section py-4 text-center text-sm text-gray-600 border-t border-surface-border">
      <p>&copy; 2023 Ứng dụng Dịch Tài liệu</p>
    </footer>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'App'
})
</script>

<style lang="scss">
// Các style riêng cho App component
// Các style chung đã được định nghĩa trong main.scss
</style> 