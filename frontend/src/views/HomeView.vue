<template>
  <div class="flex flex-col gap-8">
    <Card>
      <template #title>
        Tải lên tài liệu
      </template>
      <template #content>
        <div class="flex flex-col items-center">
          <FileUpload
            name="file"
            :customUpload="true"
            @uploader="handleFileUpload"
            :auto="true"
            chooseLabel="Chọn tài liệu"
            uploadLabel="Tải lên"
            cancelLabel="Hủy"
            :maxFileSize="10000000"
            accept=".pdf,.docx,.doc,.xlsx,.xls"
            class="w-full"
          >
            <template #empty>
              <p class="text-center text-gray-600">Kéo và thả file PDF, Word hoặc Excel vào đây để tải lên.</p>
              <p class="text-center text-gray-600">Hỗ trợ dịch từ tiếng Nhật và các ngôn ngữ khác sang tiếng Việt.</p>
            </template>
          </FileUpload>
        </div>
      </template>
    </Card>

    <div v-if="isLoading" class="flex flex-col items-center justify-center p-8 gap-4">
      <ProgressSpinner />
      <p class="text-gray-600">{{ loadingMessage }}</p>
    </div>

    <div v-if="documentContent && !isLoading" class="w-full">
      <Card>
        <template #title>
          <div class="flex justify-between items-center w-full">
            <span>Nội dung tài liệu</span>
            <div class="flex gap-2">
              <Button 
                label="Xuất file đã dịch" 
                icon="pi pi-download" 
                @click="exportDocument" 
                :disabled="!translatedContent"
                class="p-button-primary"
              />
            </div>
          </div>
        </template>
        <template #content>
          <div v-if="fileType === 'pdf'">
            <TranslationPdfView 
              :content="documentContent" 
              :translatedContent="translatedContent"
              @update:translatedContent="updateTranslatedContent"
            />
          </div>
          <div v-else-if="fileType === 'excel'">
            <TranslationExcelView 
              :content="documentContent" 
              :translatedContent="translatedContent"
              @update:translatedContent="updateTranslatedContent"
            />
          </div>
          <div v-else-if="fileType === 'word'">
            <TranslationWordView 
              :content="documentContent" 
              :translatedContent="translatedContent"
              @update:translatedContent="updateTranslatedContent"
            />
          </div>
        </template>
      </Card>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import axios from 'axios'
import TranslationPdfView from '@/components/TranslationPdfView.vue'
import TranslationExcelView from '@/components/TranslationExcelView.vue'
import TranslationWordView from '@/components/TranslationWordView.vue'
import type { DocumentContent } from '@/types'

// Cấu hình API URL
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
console.log('API URL:', API_URL)

export default defineComponent({
  name: 'HomeView',
  components: {
    TranslationPdfView,
    TranslationExcelView,
    TranslationWordView
  },
  data() {
    return {
      isLoading: false,
      loadingMessage: '',
      documentContent: null as DocumentContent[] | null,
      translatedContent: null as DocumentContent[] | null,
      fileType: null as string | null,
      originalFile: null as File | null,
      originalFilename: ''
    }
  },
  methods: {
    async handleFileUpload(event: { files: File[] }) {
      try {
        this.isLoading = true
        this.loadingMessage = 'Đang tải lên và xử lý tài liệu...'
        this.documentContent = null
        this.translatedContent = null
        
        const file = event.files[0]
        this.originalFile = file
        this.originalFilename = file.name
        
        const formData = new FormData()
        formData.append('file', file)
        
        const response = await axios.post(`${API_URL}/api/documents/upload`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        
        if (response.data.success) {
          this.documentContent = response.data.content
          this.fileType = response.data.file_type
          
          await this.translateDocument()
        } else {
          this.$toast.add({
            severity: 'error',
            summary: 'Lỗi',
            detail: 'Không thể xử lý tài liệu',
            life: 3000
          })
        }
      } catch (error: any) {
        console.error('Error uploading file:', error)
        this.$toast.add({
          severity: 'error',
          summary: 'Lỗi',
          detail: error.response?.data?.detail || 'Đã xảy ra lỗi khi tải lên tài liệu',
          life: 3000
        })
      } finally {
        this.isLoading = false
      }
    },
    
    async translateDocument() {
      try {
        this.isLoading = true
        this.loadingMessage = 'Đang dịch tài liệu...'
        
        const formData = new FormData()
        formData.append('file_type', this.fileType as string)
        formData.append('content', JSON.stringify(this.documentContent))
        formData.append('original_filename', this.originalFilename)
        
        const response = await axios.post(`${API_URL}/api/documents/translate`, formData)
        
        if (response.data.success) {
          this.translatedContent = response.data.translated_content
          this.$toast.add({
            severity: 'success',
            summary: 'Thành công',
            detail: 'Tài liệu đã được dịch thành công',
            life: 3000
          })
        } else {
          this.$toast.add({
            severity: 'error',
            summary: 'Lỗi',
            detail: 'Không thể dịch tài liệu',
            life: 3000
          })
        }
      } catch (error: any) {
        console.error('Error translating document:', error)
        this.$toast.add({
          severity: 'error',
          summary: 'Lỗi',
          detail: error.response?.data?.detail || 'Đã xảy ra lỗi khi dịch tài liệu',
          life: 3000
        })
      } finally {
        this.isLoading = false
      }
    },
    
    updateTranslatedContent(newContent: DocumentContent[]) {
      console.log('HomeView: Cập nhật translated content', newContent)
      
      // Kiểm tra cấu trúc dữ liệu
      if (Array.isArray(newContent)) {
        // Kiểm tra từng phần tử trong mảng
        const validItems = newContent.filter(item => 
          item && typeof item === 'object' && 
          ('translated_content' in item || 'content' in item)
        )
        
        console.log(`HomeView: Dữ liệu hợp lệ? ${validItems.length === newContent.length}`)
        
        // Gán dữ liệu mới
        this.translatedContent = newContent
      } else {
        console.error('HomeView: Dữ liệu không phải dạng mảng', newContent)
      }
    },
    
    async exportDocument() {
      try {
        this.isLoading = true
        this.loadingMessage = 'Đang xuất tài liệu...'
        
        // Debug kiểm tra dữ liệu trước khi gửi
        console.log('File type:', this.fileType)
        console.log('Original filename:', this.originalFilename)
        console.log('Translated content structure:', this.translatedContent)
        
        // Đảm bảo cấu trúc dữ liệu đúng
        let translatedContentToSend = this.translatedContent
        
        // Kiểm tra và sửa dữ liệu nếu cần
        if (this.fileType === 'pdf' && Array.isArray(this.translatedContent)) {
          // Kiểm tra xem mỗi item có thuộc tính translated_content không
          const allItemsHaveTranslation = this.translatedContent.every(
            item => item && typeof item === 'object' && 'translated_content' in item
          )
          
          console.log('Tất cả items có thuộc tính translated_content:', allItemsHaveTranslation)
          
          if (!allItemsHaveTranslation) {
            console.warn('Cần sửa cấu trúc dữ liệu translated_content')
            
            // Sửa cấu trúc dữ liệu
            translatedContentToSend = this.translatedContent.map(item => {
              if (!('translated_content' in item) && 'content' in item) {
                return {
                  ...item,
                  translated_content: item.content
                }
              }
              return item
            })
            
            console.log('Dữ liệu đã được sửa:', translatedContentToSend)
          }
        }
        
        const formData = new FormData()
        formData.append('file_type', this.fileType as string)
        formData.append('translated_content', JSON.stringify(translatedContentToSend))
        formData.append('original_file', this.originalFile as File)
        
        const response = await axios.post(`${API_URL}/api/documents/export`, formData, {
          responseType: 'blob',
          headers: {
            'Content-Type': 'multipart/form-data',
            'Accept': '*/*'
          }
        })
        
        // Tạo URL cho blob và tải xuống
        const contentDisposition = response.headers['content-disposition']
        let filename = `translated_${this.originalFilename}`
        
        // Xử lý filename từ header nếu có
        if (contentDisposition && contentDisposition.includes('filename*=UTF-8')) {
          const filenameRegex = /filename\*=UTF-8''([^;]*)/
          const matches = filenameRegex.exec(contentDisposition)
          if (matches && matches[1]) {
            filename = decodeURIComponent(matches[1])
          }
        }
        
        const url = window.URL.createObjectURL(new Blob([response.data], { 
          type: response.headers['content-type'] 
        }))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', filename)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        
        this.$toast.add({
          severity: 'success',
          summary: 'Thành công',
          detail: 'Tài liệu đã được xuất thành công',
          life: 3000
        })
      } catch (error: any) {
        console.error('Error exporting document:', error)
        this.$toast.add({
          severity: 'error',
          summary: 'Lỗi',
          detail: error.response?.data?.detail || 'Đã xảy ra lỗi khi xuất tài liệu',
          life: 3000
        })
      } finally {
        this.isLoading = false
      }
    }
  }
})
</script> 