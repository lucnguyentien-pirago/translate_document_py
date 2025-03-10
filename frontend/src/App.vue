<template>
  <div class="app-container">
    <Toast />
    <header class="app-header">
      <div class="app-title">
        <h1>Ứng dụng Dịch Tài liệu</h1>
        <p>Dịch tài liệu từ nhiều ngôn ngữ sang tiếng Việt</p>
      </div>
    </header>
    <main class="app-content">
      <router-view />
    </main>
    <footer class="app-footer">
      <p>&copy; 2023 Ứng dụng Dịch Tài liệu</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style lang="scss">
// Các style riêng cho App component
// Các style chung đã được định nghĩa trong main.scss
</style> 