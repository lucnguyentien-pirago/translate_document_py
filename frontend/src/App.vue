<template>
  <div class="min-h-screen flex flex-column">
    <Toast />
    <header class="bg-primary text-white py-4 px-6 shadow-4">
      <div class="text-center">
        <h1 class="text-4xl font-bold mb-2">Ứng dụng Dịch Tài liệu</h1>
        <p class="text-xl">Dịch tài liệu từ nhiều ngôn ngữ sang tiếng Việt</p>
      </div>
    </header>
    <main class="flex-grow-1 p-4 w-full">
      <div class="container">
        <router-view />
      </div>
    </main>
    <footer class="bg-white py-3 text-center text-sm text-color-secondary border-top-1 surface-border">
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

<style>
.container {
  max-width: var(--app-max-width);
  margin: 0 auto;
  width: 100%;
}
</style>