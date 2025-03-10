<template>
  <div class="flex flex-col gap-4">
    <TabView>
      <TabPanel header="Nội dung gốc">
        <div class="overflow-x-auto">
          <DataTable :value="content" responsiveLayout="scroll" class="min-w-full">
            <Column v-for="col in columns" :key="col.field" :field="col.field" :header="col.header" />
          </DataTable>
        </div>
      </TabPanel>
      <TabPanel header="Bản dịch">
        <div class="overflow-x-auto">
          <DataTable :value="translatedRows" responsiveLayout="scroll" class="min-w-full">
            <Column v-for="col in columns" :key="col.field" :field="col.field" :header="col.header">
              <template #body="{ data, field }">
                <Textarea
                  v-model="data[field]"
                  :autoResize="true"
                  rows="2"
                  class="w-full"
                  @input="handleTranslationChange(data, field)"
                />
              </template>
            </Column>
          </DataTable>
        </div>
      </TabPanel>
    </TabView>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType, ref, computed, watch } from 'vue'
import type { DocumentContent } from '@/types'

interface ExcelColumn {
  field: string;
  header: string;
}

interface ExcelRow {
  [key: string]: string;
}

export default defineComponent({
  name: 'TranslationExcelView',
  
  props: {
    content: {
      type: Array as PropType<ExcelRow[]>,
      required: true
    },
    translatedContent: {
      type: Array as PropType<ExcelRow[] | null>,
      default: null
    }
  },

  emits: {
    'update:translatedContent': (value: ExcelRow[]) => Array.isArray(value)
  },

  setup(props, { emit }) {
    const columns = ref<ExcelColumn[]>([])
    const translatedRows = ref<ExcelRow[]>([])

    // Tạo cấu trúc cột từ dữ liệu đầu vào
    watch(() => props.content, (newContent) => {
      if (newContent && newContent.length > 0) {
        // Lấy tất cả các key từ row đầu tiên
        const firstRow = newContent[0]
        columns.value = Object.keys(firstRow).map(key => ({
          field: key,
          header: key
        }))
      }
    }, { immediate: true })

    // Khởi tạo dữ liệu dịch
    watch([() => props.content, () => props.translatedContent], ([newContent, newTranslated]) => {
      if (newContent) {
        if (newTranslated) {
          translatedRows.value = [...newTranslated]
        } else {
          translatedRows.value = newContent.map(row => ({ ...row }))
        }
      }
    }, { immediate: true })

    const handleTranslationChange = (row: ExcelRow, field: string) => {
      emit('update:translatedContent', translatedRows.value)
    }

    return {
      columns,
      translatedRows,
      handleTranslationChange
    }
  }
})
</script> 