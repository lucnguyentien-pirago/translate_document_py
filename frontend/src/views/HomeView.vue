<template>
  <div class="home-container">
    <Card class="upload-card">
      <template #title>
        Tải lên tài liệu
      </template>
      <template #content>
        <div class="upload-section">
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
          >
            <template #empty>
              <p>Kéo và thả file PDF, Word hoặc Excel vào đây để tải lên.</p>
              <p>Hỗ trợ dịch từ tiếng Nhật và các ngôn ngữ khác sang tiếng Việt.</p>
            </template>
          </FileUpload>
        </div>
      </template>
    </Card>

    <div v-if="isLoading" class="loading-container">
      <ProgressSpinner />
      <p>{{ loadingMessage }}</p>
    </div>

    <div v-if="documentContent && !isLoading" class="document-content">
      <Card>
        <template #title>
          <div class="card-header">
            <span>Nội dung tài liệu</span>
            <div class="card-actions">
              <Button 
                label="Xuất file đã dịch" 
                icon="pi pi-download" 
                @click="exportDocument" 
                :disabled="!translatedContent"
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

<script>
import axios from 'axios';
import TranslationPdfView from '@/components/TranslationPdfView.vue';
import TranslationExcelView from '@/components/TranslationExcelView.vue';
import TranslationWordView from '@/components/TranslationWordView.vue';

// Cấu hình API URL
const API_URL = 'http://localhost:8000';

export default {
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
      documentContent: null,
      translatedContent: null,
      fileType: null,
      originalFile: null,
      originalFilename: ''
    };
  },
  methods: {
    async handleFileUpload(event) {
      try {
        this.isLoading = true;
        this.loadingMessage = 'Đang tải lên và xử lý tài liệu...';
        this.documentContent = null;
        this.translatedContent = null;
        
        const file = event.files[0];
        this.originalFile = file;
        this.originalFilename = file.name;
        
        const formData = new FormData();
        formData.append('file', file);
        
        // Gửi file lên server để xử lý - sử dụng URL tuyệt đối
        const response = await axios.post(`${API_URL}/api/documents/upload`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        
        if (response.data.success) {
          this.documentContent = response.data.content;
          this.fileType = response.data.file_type;
          
          // Tự động dịch nội dung
          await this.translateDocument();
        } else {
          this.$toast.add({
            severity: 'error',
            summary: 'Lỗi',
            detail: 'Không thể xử lý tài liệu',
            life: 3000
          });
        }
      } catch (error) {
        console.error('Error uploading file:', error);
        this.$toast.add({
          severity: 'error',
          summary: 'Lỗi',
          detail: error.response?.data?.detail || 'Đã xảy ra lỗi khi tải lên tài liệu',
          life: 3000
        });
      } finally {
        this.isLoading = false;
      }
    },
    
    async translateDocument() {
      try {
        this.isLoading = true;
        this.loadingMessage = 'Đang dịch tài liệu...';
        
        const formData = new FormData();
        formData.append('file_type', this.fileType);
        formData.append('content', JSON.stringify(this.documentContent));
        formData.append('original_filename', this.originalFilename);
        
        const response = await axios.post(`${API_URL}/api/documents/translate`, formData);
        
        if (response.data.success) {
          this.translatedContent = response.data.translated_content;
          this.$toast.add({
            severity: 'success',
            summary: 'Thành công',
            detail: 'Tài liệu đã được dịch thành công',
            life: 3000
          });
        } else {
          this.$toast.add({
            severity: 'error',
            summary: 'Lỗi',
            detail: 'Không thể dịch tài liệu',
            life: 3000
          });
        }
      } catch (error) {
        console.error('Error translating document:', error);
        this.$toast.add({
          severity: 'error',
          summary: 'Lỗi',
          detail: error.response?.data?.detail || 'Đã xảy ra lỗi khi dịch tài liệu',
          life: 3000
        });
      } finally {
        this.isLoading = false;
      }
    },
    
    updateTranslatedContent(newContent) {
      this.translatedContent = newContent;
    },
    
    async exportDocument() {
      try {
        this.isLoading = true;
        this.loadingMessage = 'Đang xuất tài liệu...';
        
        // Debug kiểm tra dữ liệu trước khi gửi
        console.log('File type:', this.fileType);
        console.log('Original filename:', this.originalFilename);
        console.log('Translated content structure:', this.translatedContent);
        
        const formData = new FormData();
        formData.append('file_type', this.fileType);
        formData.append('translated_content', JSON.stringify(this.translatedContent));
        formData.append('original_file', this.originalFile);
        
        const response = await axios.post(`${API_URL}/api/documents/export`, formData, {
          responseType: 'blob',
          headers: {
            'Content-Type': 'multipart/form-data',
            'Accept': '*/*'
          }
        });
        
        // Tạo URL cho blob và tải xuống
        const contentDisposition = response.headers['content-disposition'];
        let filename = `translated_${this.originalFilename}`;
        
        // Xử lý filename từ header nếu có
        if (contentDisposition && contentDisposition.includes('filename*=UTF-8')) {
          const filenameRegex = /filename\*=UTF-8''([^;]*)/;
          const matches = filenameRegex.exec(contentDisposition);
          if (matches && matches[1]) {
            filename = decodeURIComponent(matches[1]);
          }
        }
        
        const url = window.URL.createObjectURL(new Blob([response.data], { 
          type: response.headers['content-type'] 
        }));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', filename);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        this.$toast.add({
          severity: 'success',
          summary: 'Thành công',
          detail: 'Tài liệu đã được xuất thành công',
          life: 3000
        });
      } catch (error) {
        console.error('Error exporting document:', error);
        this.$toast.add({
          severity: 'error',
          summary: 'Lỗi',
          detail: error.response?.data?.detail || 'Đã xảy ra lỗi khi xuất tài liệu',
          life: 3000
        });
      } finally {
        this.isLoading = false;
      }
    }
  }
};
</script>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.upload-card {
  width: 100%;
}

.upload-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  gap: 1rem;
}

.document-content {
  width: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
}
</style> 