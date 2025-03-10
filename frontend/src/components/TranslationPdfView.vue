<template>
  <div class="flex flex-col gap-4">
    <TabView>
      <TabPanel header="Nội dung gốc">
        <div class="grid grid-cols-1 gap-4">
          <div v-for="(item, index) in content" :key="index" class="bg-white rounded-lg p-4 shadow">
            <p class="text-gray-900">{{ item.content }}</p>
          </div>
        </div>
      </TabPanel>
      <TabPanel header="Bản dịch">
        <div class="grid grid-cols-1 gap-4">
          <div v-for="(item, index) in content" :key="index" class="bg-white rounded-lg p-4 shadow">
            <Textarea
              v-model="translations[index]"
              :autoResize="true"
              rows="3"
              class="w-full"
              @input="handleTranslationChange(index)"
            />
          </div>
        </div>
      </TabPanel>
    </TabView>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType, ref, watch } from 'vue'
import type { DocumentContent, TranslationViewProps, TranslationViewEmits } from '@/types'

export default defineComponent({
  name: 'TranslationPdfView',
  
  props: {
    content: {
      type: Array as PropType<DocumentContent[]>,
      required: true
    },
    translatedContent: {
      type: Array as PropType<DocumentContent[] | null>,
      default: null
    }
  },

  emits: {
    'update:translatedContent': (value: DocumentContent[]) => Array.isArray(value)
  },

  setup(props: TranslationViewProps, { emit }) {
    const translations = ref<string[]>([])

    // Khởi tạo translations từ translatedContent hoặc content
    watch(() => props.content, (newContent) => {
      translations.value = newContent.map(item => 
        item.translated_content || item.content
      )
    }, { immediate: true })

    // Cập nhật khi có thay đổi từ bên ngoài
    watch(() => props.translatedContent, (newTranslated) => {
      if (newTranslated) {
        translations.value = newTranslated.map(item => 
          item.translated_content || item.content
        )
      }
    })

    const handleTranslationChange = (index: number) => {
      const updatedContent = props.content.map((item, i) => ({
        ...item,
        translated_content: translations.value[i]
      }))
      emit('update:translatedContent', updatedContent)
    }

    return {
      translations,
      handleTranslationChange
    }
  }
})
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