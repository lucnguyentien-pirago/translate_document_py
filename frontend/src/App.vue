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

<style>
body {
  margin: 0;
  padding: 0;
  font-family: var(--font-family);
  background-color: var(--surface-ground);
  color: var(--text-color);
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-header {
  background-color: var(--primary-color);
  color: var(--primary-color-text);
  padding: 1rem 2rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.app-title {
  text-align: center;
}

.app-title h1 {
  margin: 0;
  font-size: 1.8rem;
}

.app-title p {
  margin: 0.5rem 0 0;
  font-size: 1rem;
  opacity: 0.9;
}

.app-content {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.app-footer {
  background-color: var(--surface-section);
  padding: 1rem;
  text-align: center;
  font-size: 0.9rem;
  color: var(--text-color-secondary);
  border-top: 1px solid var(--surface-border);
}
</style> 