<template>
  <div class="pdf-translation-container">
    <TabView>
      <TabPanel header="Xem trước">
        <div class="pdf-preview">
          <div v-for="(page, index) in translatedPages" :key="index" class="pdf-page">
            <div class="page-header">
              <h3>Trang {{ page.page }}</h3>
            </div>
            <div class="page-content">
              <div class="original-content">
                <h4>Nội dung gốc</h4>
                <div class="content-box">{{ getOriginalContent(page.page) }}</div>
              </div>
              <div class="translated-content">
                <h4>Bản dịch</h4>
                <div class="content-box">{{ page.translated_content }}</div>
              </div>
            </div>
          </div>
        </div>
      </TabPanel>
      <TabPanel header="Chỉnh sửa">
        <div class="pdf-edit">
          <div v-for="(page, index) in translatedPages" :key="index" class="pdf-page-edit">
            <div class="page-header">
              <h3>Trang {{ page.page }}</h3>
            </div>
            <div class="page-content-edit">
              <div class="original-content">
                <h4>Nội dung gốc</h4>
                <div class="content-box">{{ getOriginalContent(page.page) }}</div>
              </div>
              <div class="translated-content">
                <h4>Bản dịch</h4>
                <Textarea
                  v-model="translatedPages[index].translated_content"
                  :autoResize="true"
                  rows="10"
                  class="w-full"
                  @input="updateTranslation"
                />
              </div>
            </div>
          </div>
        </div>
      </TabPanel>
    </TabView>
  </div>
</template>

<script>
export default {
  name: 'TranslationPdfView',
  props: {
    content: {
      type: Array,
      required: true
    },
    translatedContent: {
      type: Array,
      default: null
    }
  },
  data() {
    return {
      translatedPages: []
    };
  },
  watch: {
    translatedContent: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.translatedPages = [...newVal];
        }
      }
    }
  },
  methods: {
    getOriginalContent(pageNumber) {
      const page = this.content.find(p => p.page === pageNumber);
      return page ? page.content : '';
    },
    updateTranslation() {
      console.log('Cập nhật nội dung đã dịch PDF:', this.translatedPages);
      this.$emit('update:translatedContent', this.translatedPages);
    }
  }
};
</script>

<style scoped>
.pdf-translation-container {
  width: 100%;
}

.pdf-preview, .pdf-edit {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.pdf-page, .pdf-page-edit {
  border: 1px solid var(--surface-border);
  border-radius: 6px;
  overflow: hidden;
  background-color: var(--surface-card);
}

.page-header {
  background-color: var(--primary-color);
  color: var(--primary-color-text);
  padding: 0.5rem 1rem;
}

.page-header h3 {
  margin: 0;
  font-size: 1.2rem;
}

.page-content, .page-content-edit {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  padding: 1rem;
}

.original-content, .translated-content {
  display: flex;
  flex-direction: column;
}

.content-box {
  border: 1px solid var(--surface-border);
  border-radius: 4px;
  padding: 1rem;
  background-color: var(--surface-ground);
  min-height: 100px;
  white-space: pre-wrap;
  overflow-wrap: break-word;
}

h4 {
  margin-top: 0;
  margin-bottom: 0.5rem;
  color: var(--text-color-secondary);
}

@media (max-width: 768px) {
  .page-content, .page-content-edit {
    grid-template-columns: 1fr;
  }
}
</style> 