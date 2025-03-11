<template>
  <div class="translation-view">
    <TabView>
      <TabPanel header="Nội dung gốc">
        <div class="grid">
          <div v-for="(item, index) in content" :key="index" class="col-12 mb-3">
            <div class="surface-card border-round-md p-3 shadow-2">
              <p class="text-color line-height-3">{{ item.content }}</p>
            </div>
          </div>
        </div>
      </TabPanel>
      <TabPanel header="Bản dịch">
        <div class="grid">
          <div v-for="(item, index) in content" :key="index" class="col-12 mb-3">
            <div class="surface-card border-round-md p-3 shadow-2">
              <Textarea
                v-model="translations[index]"
                :autoResize="true"
                rows="3"
                class="w-full"
                @input="handleTranslationChange(index)"
              />
            </div>
          </div>
        </div>
      </TabPanel>
    </TabView>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from 'vue'
import type { PropType } from 'vue'
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