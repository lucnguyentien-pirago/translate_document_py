<template>
  <div class="excel-translation-container">
    <TabView>
      <TabPanel header="Xem trước">
        <div class="excel-preview">
          <TabView>
            <TabPanel v-for="(sheet, sheetIndex) in translatedSheets" :key="sheetIndex" :header="sheet.sheet_name">
              <DataTable :value="getTableData(sheet)" stripedRows class="excel-table">
                <Column field="address" header="Ô" style="width: 10%"></Column>
                <Column field="original" header="Nội dung gốc" style="width: 45%"></Column>
                <Column field="translated" header="Bản dịch" style="width: 45%"></Column>
              </DataTable>
            </TabPanel>
          </TabView>
        </div>
      </TabPanel>
      <TabPanel header="Chỉnh sửa">
        <div class="excel-edit">
          <TabView>
            <TabPanel v-for="(sheet, sheetIndex) in translatedSheets" :key="sheetIndex" :header="sheet.sheet_name">
              <div class="sheet-edit-container">
                <div v-for="(cell, cellIndex) in sheet.cells" :key="cellIndex" class="cell-edit-row">
                  <div class="cell-address">{{ cell.address }}</div>
                  <div class="cell-original">{{ cell.content }}</div>
                  <div class="cell-translated">
                    <Textarea
                      v-model="translatedSheets[sheetIndex].cells[cellIndex].translated_content"
                      :autoResize="true"
                      rows="2"
                      class="w-full"
                      @input="updateTranslation"
                    />
                  </div>
                </div>
              </div>
            </TabPanel>
          </TabView>
        </div>
      </TabPanel>
    </TabView>
  </div>
</template>

<script>
export default {
  name: 'TranslationExcelView',
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
      translatedSheets: []
    };
  },
  watch: {
    translatedContent: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.translatedSheets = [...newVal];
        }
      }
    }
  },
  methods: {
    getTableData(sheet) {
      return sheet.cells.map(cell => ({
        address: cell.address,
        original: cell.content,
        translated: cell.translated_content
      }));
    },
    updateTranslation() {
      this.$emit('update:translatedContent', this.translatedSheets);
    }
  }
};
</script>

<style scoped>
.excel-translation-container {
  width: 100%;
}

.excel-preview, .excel-edit {
  width: 100%;
}

.excel-table {
  width: 100%;
}

.sheet-edit-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem 0;
}

.cell-edit-row {
  display: grid;
  grid-template-columns: 10% 45% 45%;
  gap: 1rem;
  align-items: center;
  padding: 0.5rem;
  border-bottom: 1px solid var(--surface-border);
}

.cell-edit-row:nth-child(even) {
  background-color: var(--surface-ground);
}

.cell-address {
  font-weight: bold;
  color: var(--primary-color);
}

.cell-original {
  white-space: pre-wrap;
  overflow-wrap: break-word;
  padding: 0.5rem;
  background-color: var(--surface-card);
  border: 1px solid var(--surface-border);
  border-radius: 4px;
}

.cell-translated {
  width: 100%;
}

@media (max-width: 768px) {
  .cell-edit-row {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
}
</style> 