# Fonts cho PDF Export

Thư mục này chứa các font được sử dụng để hiển thị đúng các ký tự Unicode, bao gồm tiếng Việt trong file PDF xuất ra.

## Danh sách font

- **DejaVuSans.ttf**: Font DejaVu Sans Regular - hỗ trợ tốt cho Unicode và tiếng Việt
- **DejaVuSans-Bold.ttf**: Font DejaVu Sans Bold - phiên bản đậm của DejaVu Sans
- **NotoSans-Regular.ttf**: Font Noto Sans Regular của Google - hỗ trợ đa ngôn ngữ

## Cách thêm font mới

Để thêm font mới, chỉ cần tải file font TTF vào thư mục này. Hệ thống sẽ tự động phát hiện và sử dụng font này khi tạo PDF.

## Cách thay đổi font mặc định

Để thay đổi font mặc định, bạn có thể sửa trong file `backend/app/utils/pdf_handler.py`. Tìm biến `unicode_fonts` và thay đổi thứ tự ưu tiên font. 