<template>
  <div class="word-translation-container">
    <TabView>
      <TabPanel header="Xem trước">
        <div class="word-preview">
          <div v-for="(paragraph, index) in translatedParagraphs" :key="index" class="word-paragraph">
            <div class="paragraph-header">
              <h3>Đoạn {{ paragraph.paragraph }}</h3>
            </div>
            <div class="paragraph-content">
              <div class="original-content">
                <h4>Nội dung gốc</h4>
                <div class="content-box">{{ paragraph.content }}</div>
              </div>
              <div class="translated-content">
                <h4>Bản dịch</h4>
                <div class="content-box">{{ paragraph.translated_content }}</div>
              </div>
            </div>
          </div>
        </div>
      </TabPanel>
      <TabPanel header="Chỉnh sửa">
        <div class="word-edit">
          <div v-for="(paragraph, index) in translatedParagraphs" :key="index" class="word-paragraph-edit">
            <div class="paragraph-header">
              <h3>Đoạn {{ paragraph.paragraph }}</h3>
            </div>
            <div class="paragraph-content-edit">
              <div class="original-content">
                <h4>Nội dung gốc</h4>
                <div class="content-box">{{ paragraph.content }}</div>
              </div>
              <div class="translated-content">
                <h4>Bản dịch</h4>
                <Textarea
                  v-model="translatedParagraphs[index].translated_content"
                  :autoResize="true"
                  rows="5"
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
  name: 'TranslationWordView',
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
      translatedParagraphs: []
    };
  },
  watch: {
    translatedContent: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.translatedParagraphs = [...newVal];
        }
      }
    }
  },
  methods: {
    updateTranslation() {
      this.$emit('update:translatedContent', this.translatedParagraphs);
    }
  }
};
</script>

<style scoped>
.word-translation-container {
  width: 100%;
}

.word-preview, .word-edit {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.word-paragraph, .word-paragraph-edit {
  border: 1px solid var(--surface-border);
  border-radius: 6px;
  overflow: hidden;
  background-color: var(--surface-card);
}

.paragraph-header {
  background-color: var(--primary-color);
  color: var(--primary-color-text);
  padding: 0.5rem 1rem;
}

.paragraph-header h3 {
  margin: 0;
  font-size: 1.2rem;
}

.paragraph-content, .paragraph-content-edit {
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
  min-height: 50px;
  white-space: pre-wrap;
  overflow-wrap: break-word;
}

h4 {
  margin-top: 0;
  margin-bottom: 0.5rem;
  color: var(--text-color-secondary);
}

@media (max-width: 768px) {
  .paragraph-content, .paragraph-content-edit {
    grid-template-columns: 1fr;
  }
}
</style> 