# Ứng dụng Dịch Tài liệu

Ứng dụng web giúp dịch các tài liệu PDF, Excel và Word từ nhiều ngôn ngữ (đặc biệt là tiếng Nhật) sang tiếng Việt.

## Tính năng

- Tải lên và xử lý các file PDF, Excel và Word
- Dịch nội dung từ nhiều ngôn ngữ sang tiếng Việt
- Xem trước và chỉnh sửa bản dịch
- Xuất file đã dịch với định dạng gốc

## Cấu trúc dự án

Dự án được chia thành hai phần chính:

- **Backend**: Sử dụng Python với FastAPI
  - `backend/resources/fonts`: Thư mục chứa font cho PDF
  - `backend/app`: Mã nguồn chính của backend
  - `backend/setup_fonts.py`: Script cài đặt font
- **Frontend**: Sử dụng Vue.js 3 với PrimeVue

## Yêu cầu hệ thống

- Python 3.8+
- Node.js 14+
- Tesseract OCR (cho xử lý PDF)
- Poppler (cho xử lý PDF)

## Cài đặt

### Backend

1. Cài đặt các thư viện Python:

```bash
cd backend
pip install -r ../requirements.txt
```

2. Cài đặt fonts cho tiếng Việt:

```bash
cd backend
python setup_fonts.py
```

Script này sẽ tự động tải font Roboto và kiểm tra môi trường của bạn.

3. Cài đặt Tesseract OCR:
   - Windows: Tải từ https://github.com/UB-Mannheim/tesseract/wiki
   - Linux: `sudo apt-get install tesseract-ocr tesseract-ocr-jpn tesseract-ocr-vie`
   - macOS: `brew install tesseract tesseract-lang`

4. Cài đặt Poppler:
   - Windows: Tải từ https://github.com/oschwartz10612/poppler-windows/releases/
   - Linux: `sudo apt-get install poppler-utils`
   - macOS: `brew install poppler`

### Frontend

```bash
cd frontend
npm install
```

## Chạy ứng dụng

### Backend

```bash
cd backend
python run.py
```

Backend sẽ chạy tại http://localhost:8000

### Frontend

```bash
cd frontend
npm run dev
```

Frontend sẽ chạy tại http://localhost:8080

## Cách sử dụng

1. Mở trình duyệt và truy cập http://localhost:8080
2. Tải lên tài liệu PDF, Excel hoặc Word
3. Hệ thống sẽ tự động trích xuất và dịch nội dung
4. Xem trước và chỉnh sửa bản dịch nếu cần
5. Nhấn nút "Xuất file đã dịch" để tải xuống tài liệu đã dịch

## Xử lý lỗi phổ biến

### Lỗi hiển thị tiếng Việt trong PDF

Nếu PDF xuất ra hiển thị các ô vuông thay vì ký tự tiếng Việt:

1. **Chạy script setup_fonts.py**:
   ```bash
   cd backend
   python setup_fonts.py
   ```
   Script này sẽ tự động tải font Roboto hỗ trợ tiếng Việt.

2. **Kiểm tra thư mục fonts**:
   Đảm bảo thư mục `backend/resources/fonts` chứa các file:
   - Roboto-Regular.ttf
   - Roboto-Bold.ttf

3. **Sửa phương pháp tạo PDF**:
   Mặc định, hệ thống sẽ thử hai phương pháp tạo PDF (Platypus và Canvas) để đảm bảo tiếng Việt hiển thị đúng. Nếu vẫn có vấn đề, bạn có thể chỉnh sửa file `backend/app/utils/pdf_handler.py` để chỉ sử dụng phương pháp Canvas.

### Lỗi kết nối từ Frontend đến Backend

Nếu frontend không thể kết nối tới backend, hãy kiểm tra:
- Backend đang chạy ở địa chỉ và cổng đúng
- Không có tường lửa chặn kết nối
- URL API đã được cấu hình đúng trong file `frontend/src/views/HomeView.vue`

## Lưu ý

- Đối với file PDF, ứng dụng sẽ dịch từng trang
- Đối với file Excel, ứng dụng sẽ dịch từng ô
- Đối với file Word, ứng dụng sẽ dịch từng đoạn văn

## Giấy phép

MIT 