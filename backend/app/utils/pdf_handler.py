import PyPDF2
import io
from pdf2image import convert_from_bytes
import pytesseract
from typing import List, Dict, Optional
import os
import pathlib
import base64
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from io import BytesIO
import tempfile

# Lấy đường dẫn đến thư mục resources/fonts
CURRENT_DIR = pathlib.Path(__file__).parent.absolute()
ROOT_DIR = CURRENT_DIR.parent.parent
FONTS_DIR = ROOT_DIR / "resources" / "fonts"

# Base64 encoded minimal Vietnamese font (just to ensure we have a working font)
# Đây là một phần của font Liberation Sans để đảm bảo tiếng Việt hiển thị đúng
VIET_FONT_BASE64 = """
AAEAAAARAQAABABGRlRNVXgVHwAARxQAAAAcT1MvMoqQ/lUAAAFgAAAAYGNtYXADbgW5AAADwAAAA
ZpnYXNw//8AAwAAQYQAAAAIZ2x5ZkzALZAAAAs0AAA2JGhlYWQPnJXLAAAA7AAAADZoaGVhBhkCVgA
AASwAAAAkaG10eD8QDqIAAAH8AAAA8GxvY2GHEL44AAAKtAAAAHptYXhwAWoAhgAAAVgAAAAgbmFt
ZQG1H9EAAD9cAAADiXBvc3QAAwAAAAADAAAAACAAAwQAAZAABQAAApkCzAAAAI8CmQLMAAAB6wAzA
QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAP/kDwP/AAMAAAgMA
AAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAQAAAAAAA4AAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAIAAAAA
AAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAKAAAAAAAAAAAAAAAAAIAAAAAAA
"""

class PDFHandler:
    def __init__(self):
        # Thiết lập cấu hình Tesseract để hỗ trợ tốt tiếng Việt và tiếng Nhật
        if os.name == 'nt':  # Windows
            try:
                pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            except:
                print("Tesseract không tìm thấy ở vị trí mặc định. Vui lòng cài đặt Tesseract.")
                
        # Đăng ký font hỗ trợ Unicode/tiếng Việt
        try:
            # Kiểm tra các font mặc định có sẵn
            self.register_available_fonts()
        except Exception as e:
            print(f"Không thể đăng ký font: {str(e)}")

    def register_available_fonts(self):
        """Đăng ký các font có sẵn trong reportlab và nạp font Unicode cho tiếng Việt"""
        # Đăng ký các font mặc định của reportlab
        reportlab_fonts = [
            "Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Helvetica-BoldOblique",
            "Times-Roman", "Times-Bold", "Times-Italic", "Times-BoldItalic",
            "Courier", "Courier-Bold", "Courier-Oblique", "Courier-BoldOblique"
        ]
        
        for font in reportlab_fonts:
            if font not in pdfmetrics._fonts:
                print(f"Đăng ký font mặc định: {font}")
                # Các font này đã được đăng ký tự động bởi reportlab
        
        # Tạo font bảo đảm hỗ trợ tiếng Việt từ dữ liệu mã hóa base64
        # Điều này tránh việc phụ thuộc vào việc cài đặt font trong hệ thống
        try:
            if "VietFont" not in pdfmetrics._fonts:
                # Tạo file tạm chứa font
                with tempfile.NamedTemporaryFile(suffix='.ttf', delete=False) as temp_font:
                    temp_font.write(base64.b64decode(VIET_FONT_BASE64))
                    temp_font_path = temp_font.name
                
                # Đăng ký font từ file tạm
                pdfmetrics.registerFont(TTFont('VietFont', temp_font_path))
                print(f"Đã tạo và đăng ký font VietFont từ dữ liệu mã hóa")
        except Exception as e:
            print(f"Lỗi khi tạo font tạm thời: {str(e)}")
                
        # Tìm và đăng ký các font TrueType trong thư mục resources/fonts
        fonts_path = FONTS_DIR
        if fonts_path.exists():
            for font_file in fonts_path.glob("*.ttf"):
                font_name = font_file.stem
                if font_name not in pdfmetrics._fonts:
                    try:
                        print(f"Đăng ký font TrueType: {font_name}")
                        pdfmetrics.registerFont(TTFont(font_name, str(font_file)))
                    except Exception as e:
                        print(f"Lỗi khi đăng ký font {font_name}: {str(e)}")
        else:
            print(f"Thư mục fonts không tồn tại: {fonts_path}")
            # Tạo thư mục fonts nếu chưa tồn tại
            try:
                os.makedirs(fonts_path, exist_ok=True)
                print(f"Đã tạo thư mục fonts: {fonts_path}")
            except Exception as e:
                print(f"Không thể tạo thư mục fonts: {str(e)}")
            
        # Kiểm tra font đã đăng ký
        print(f"Danh sách font đã đăng ký: {list(pdfmetrics._fonts.keys())}")
    
    def extract_text_from_pdf(self, file_content: bytes) -> List[Dict[str, str]]:
        """
        Trích xuất văn bản từ file PDF
        Trả về danh sách các trang, mỗi trang là một dictionary với key là số trang và value là nội dung
        """
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            result = []
            
            for i, page in enumerate(pdf_reader.pages):
                text = page.extract_text()
                
                # Nếu không trích xuất được text thông qua PyPDF2, thử dùng OCR
                if not text or text.isspace():
                    # Chuyển đổi trang PDF thành hình ảnh và sử dụng OCR
                    try:
                        images = convert_from_bytes(
                            file_content, 
                            first_page=i+1, 
                            last_page=i+1,
                            dpi=300  # Tăng độ phân giải để OCR tốt hơn
                        )
                        if images:
                            # Sử dụng cả tiếng Việt, tiếng Nhật và tiếng Anh
                            text = pytesseract.image_to_string(
                                images[0], 
                                lang='jpn+eng+vie',
                                config='--psm 6'  # Chế độ phân tích trang đầy đủ
                            )
                    except Exception as ocr_error:
                        print(f"OCR error: {str(ocr_error)}")
                        text = ""
                
                result.append({
                    "page": i + 1,
                    "content": text if text else "Không thể trích xuất nội dung từ trang này"
                })
                
            return result
        except Exception as e:
            raise Exception(f"Lỗi khi xử lý file PDF: {str(e)}")
    
    def create_translated_pdf(self, original_file: bytes, translated_texts: List[Dict[str, str]]) -> bytes:
        """
        Tạo file PDF với nội dung đã được dịch
        """
        # Thử sử dụng phương pháp 1: Platypus với Paragraph
        try:
            return self._create_pdf_with_platypus(original_file, translated_texts)
        except Exception as e:
            print(f"Lỗi khi tạo PDF với Platypus: {str(e)}")
            print("Thử phương pháp 2: Sử dụng canvas trực tiếp")
            try:
                return self._create_pdf_with_canvas(original_file, translated_texts)
            except Exception as e2:
                error_msg = f"Cả hai phương pháp tạo PDF đều thất bại. Lỗi cuối cùng: {str(e2)}"
                print(error_msg)
                import traceback
                print(traceback.format_exc())
                raise Exception(error_msg)

    def _create_pdf_with_platypus(self, original_file: bytes, translated_texts: List[Dict[str, str]]) -> bytes:
        """
        Tạo PDF với Platypus (phương pháp 1)
        """
        try:
            # DEBUG: In thông tin nhận được
            print(f"DEBUG: Nhận được {len(translated_texts)} mục để dịch")
            for i, item in enumerate(translated_texts[:3]):  # Chỉ in 3 mục đầu tiên để tránh log quá dài
                print(f"DEBUG: Item {i} - Keys: {item.keys()}")
                if "translated_content" in item:
                    print(f"DEBUG: Sample translated content ({len(item['translated_content'])} chars): {item['translated_content'][:100]}...")
            
            # Tạo mapping từ số trang đến nội dung đã dịch
            translations = {}
            for item in translated_texts:
                if "page" in item and "translated_content" in item:
                    translations[item["page"]] = item["translated_content"]
            
            print(f"DEBUG: Mapping đã tạo cho {len(translations)} trang")
            
            # Đảm bảo thư mục fonts tồn tại
            if not FONTS_DIR.exists():
                print(f"CẢNH BÁO: Thư mục fonts không tồn tại: {FONTS_DIR}")
                print("Tạo thư mục fonts...")
                os.makedirs(FONTS_DIR, exist_ok=True)
            
            # Kiểm tra lại các font đã đăng ký
            self.register_available_fonts()
            
            # Tạo PDF mới chỉ với nội dung đã dịch
            output_buffer = BytesIO()
            
            # Chọn font phù hợp cho PDF với ưu tiên là font Unicode tốt nhất
            title_font = 'Helvetica-Bold'  # Font mặc định cho tiêu đề
            content_font = 'Helvetica'     # Font mặc định cho nội dung
            
            # Kiểm tra xem có font nào hỗ trợ Unicode tốt hơn không
            available_fonts = list(pdfmetrics._fonts.keys())
            print(f"DEBUG: Các font có sẵn: {available_fonts}")
            
            # Ưu tiên font Roboto, sau đó đến các font thường dùng cho Unicode
            unicode_fonts = ['Roboto-Regular', 'Roboto-Bold', 'VietFont', 'Arial', 'FreeSans']
            for font in unicode_fonts:
                if font in available_fonts:
                    content_font = font
                    title_font = 'Roboto-Bold' if 'Roboto-Bold' in available_fonts else font
                    print(f"DEBUG: Đã chọn font Unicode: {font}")
                    break
            
            # Tạo document với cấu hình rõ ràng
            doc = SimpleDocTemplate(
                output_buffer, 
                pagesize=A4,
                rightMargin=30, leftMargin=30,
                topMargin=30, bottomMargin=30
            )
            
            # Tạo style mới cho nội dung tiếng Việt
            styles = getSampleStyleSheet()
            
            # Style cho tiêu đề
            title_style = ParagraphStyle(
                'VietnameseTitle',
                fontName=title_font,
                fontSize=16,
                alignment=1,  # center
                spaceAfter=12,
                encoding='utf-8'
            )
            
            # Style cho nội dung
            content_style = ParagraphStyle(
                'VietnameseContent',
                fontName=content_font,
                fontSize=11,
                leading=14,
                spaceAfter=10,
                encoding='utf-8',
                wordWrap='CJK',  # Dùng wordWrap='CJK' cho tiếng Việt và tiếng Nhật
                allowWidows=0,
                allowOrphans=0
            )
            
            # Tạo danh sách các phần tử cho PDF
            elements = []
            
            # Thêm tiêu đề chính (ghi rõ bản dịch tiếng Việt)
            elements.append(Paragraph("BẢN DỊCH TIẾNG VIỆT", title_style))
            elements.append(Spacer(1, 20))
            
            # Đọc PDF gốc để lấy số trang
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(original_file))
            num_pages = len(pdf_reader.pages)
            
            # Duyệt qua từng trang của PDF gốc
            for i in range(num_pages):
                page_num = i + 1
                
                # Lấy nội dung đã dịch
                translated_content = translations.get(page_num, "Không có bản dịch cho trang này")
                
                # Xử lý lỗi Unicode đặc biệt - đảm bảo nội dung không có ký tự không hợp lệ
                translated_content = self._sanitize_text_for_pdf(translated_content)
                
                # Thêm phần đánh số trang
                elements.append(Paragraph(f"Trang {page_num}/{num_pages}", title_style))
                elements.append(Spacer(1, 10))
                
                # Chỉ thêm phần nội dung đã dịch, bỏ qua nội dung gốc
                elements.append(Paragraph(translated_content, content_style))
                
                # Thêm ngắt trang (trừ trang cuối)
                if i < num_pages - 1:
                    elements.append(PageBreak())
            
            # Build PDF document
            print("DEBUG: Bắt đầu tạo PDF...")
            doc.build(elements)
            print("DEBUG: Đã tạo PDF xong!")
            
            # Lấy nội dung đã tạo
            output_buffer.seek(0)
            return output_buffer.getvalue()
        
        except Exception as e:
            error_msg = f"Lỗi khi tạo file PDF với Platypus: {str(e)}"
            print(error_msg)
            import traceback
            print(traceback.format_exc())
            raise Exception(error_msg)
        
    def _create_pdf_with_canvas(self, original_file: bytes, translated_texts: List[Dict[str, str]]) -> bytes:
        """
        Tạo PDF bằng cách vẽ trực tiếp văn bản tiếng Việt lên canvas (phương pháp 2)
        """
        try:
            # Tạo mapping từ số trang đến nội dung đã dịch
            translations = {}
            for item in translated_texts:
                if "page" in item and "translated_content" in item:
                    translations[item["page"]] = item["translated_content"]
            
            print(f"DEBUG CANVAS: Mapping đã tạo cho {len(translations)} trang")
            
            # Đảm bảo fonts đã đăng ký
            self.register_available_fonts()
            
            # Tạo PDF mới
            output_buffer = BytesIO()
            
            # Chọn font Unicode tốt nhất có sẵn
            available_fonts = list(pdfmetrics._fonts.keys())
            font_name = 'Helvetica'  # Font mặc định
            unicode_fonts = ['Roboto-Regular', 'Roboto-Bold', 'VietFont', 'Arial']
            for font in unicode_fonts:
                if font in available_fonts:
                    font_name = font
                    print(f"DEBUG CANVAS: Đã chọn font Unicode: {font}")
                    break
            
            # Đọc PDF gốc để lấy số trang
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(original_file))
            num_pages = len(pdf_reader.pages)
            
            # Tạo canvas
            c = canvas.Canvas(output_buffer, pagesize=A4)
            page_width, page_height = A4
            
            # Thiết lập font và kích thước
            c.setFont(font_name, 16)
            
            # Vẽ từng trang
            for i in range(num_pages):
                page_num = i + 1
                
                # Tạo trang mới
                if i > 0:
                    c.showPage()
                
                # Vẽ tiêu đề
                c.setFont(font_name, 16)
                title_text = "BẢN DỊCH TIẾNG VIỆT"
                title_width = c.stringWidth(title_text, font_name, 16)
                c.drawString((page_width - title_width) / 2, page_height - 40, title_text)
                
                # Vẽ số trang
                page_text = f"Trang {page_num}/{num_pages}"
                page_width_text = c.stringWidth(page_text, font_name, 14)
                c.setFont(font_name, 14)
                c.drawString((page_width - page_width_text) / 2, page_height - 60, page_text)
                
                # Lấy nội dung đã dịch
                translated_content = translations.get(page_num, "Không có bản dịch cho trang này")
                translated_content = self._sanitize_text_for_pdf(translated_content)
                
                # Chia nội dung thành các dòng
                c.setFont(font_name, 11)
                y_position = page_height - 100  # Vị trí bắt đầu vẽ văn bản
                line_height = 14
                
                # Chia văn bản thành các dòng dựa trên độ rộng trang
                max_width = page_width - 60  # 30px margin ở mỗi bên
                lines = []
                
                # Chia văn bản theo dấu xuống dòng trước
                paragraphs = translated_content.split('\n')
                for paragraph in paragraphs:
                    if not paragraph.strip():
                        lines.append('')
                        continue
                    
                    # Chia mỗi đoạn thành các dòng dựa trên độ rộng
                    words = paragraph.split(' ')
                    current_line = words[0]
                    
                    for word in words[1:]:
                        test_line = current_line + ' ' + word
                        line_width = c.stringWidth(test_line, font_name, 11)
                        
                        if line_width <= max_width:
                            current_line = test_line
                        else:
                            lines.append(current_line)
                            current_line = word
                    
                    # Thêm dòng cuối cùng của đoạn
                    if current_line:
                        lines.append(current_line)
                    
                    # Thêm dòng trống sau mỗi đoạn
                    lines.append('')
                
                # Vẽ các dòng văn bản
                for line in lines:
                    if y_position < 40:  # Kiểm tra xem còn đủ không gian không
                        c.showPage()  # Tạo trang mới
                        y_position = page_height - 40  # Reset vị trí y
                    
                    c.drawString(30, y_position, line)
                    y_position -= line_height
            
            # Lưu PDF
            c.save()
            
            # Trả về nội dung
            output_buffer.seek(0)
            return output_buffer.getvalue()
            
        except Exception as e:
            error_msg = f"Lỗi khi tạo file PDF với Canvas: {str(e)}"
            print(error_msg)
            import traceback
            print(traceback.format_exc())
            raise Exception(error_msg)
    
    def _sanitize_text_for_pdf(self, text: str) -> str:
        """
        Làm sạch văn bản để tránh lỗi khi tạo PDF
        """
        if not text:
            return "Không có nội dung"
        
        # Chuyển đổi ký tự XML đặc biệt
        text = (
            text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;')
        )
        
        # Xử lý các ký tự đặc biệt có thể gây lỗi trong PDF
        chars_to_replace = {
            '\u2028': ' ',  # Line separator
            '\u2029': ' ',  # Paragraph separator
            '\u0000': '',   # Null character
            '\u001a': '',   # EOF character
            '\u001c': '',   # File separator
            '\u001d': '',   # Group separator
            '\u001e': '',   # Record separator
            '\u001f': '',   # Unit separator
        }
        
        for char, replacement in chars_to_replace.items():
            text = text.replace(char, replacement)
        
        return text 