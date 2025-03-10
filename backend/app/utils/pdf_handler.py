import PyPDF2
import io
from pdf2image import convert_from_bytes
import pytesseract
from typing import List, Dict, Optional
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from io import BytesIO

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
            pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
        except:
            print("Không thể đăng ký font Arial. Sử dụng font mặc định.")
    
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
        try:
            # Tạo mapping từ số trang đến nội dung đã dịch
            translations = {}
            for item in translated_texts:
                if "page" in item and "translated_content" in item:
                    translations[item["page"]] = item["translated_content"]
            
            # Đọc file PDF gốc
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(original_file))
            pdf_writer = PyPDF2.PdfWriter()
            
            # Tạo PDF mới kết hợp nội dung gốc với bản dịch
            for i in range(len(pdf_reader.pages)):
                page_num = i + 1
                
                # Lấy nội dung đã dịch cho trang này
                translated_content = translations.get(page_num, "")
                
                if translated_content:
                    # Trước tiên, thêm trang gốc
                    pdf_writer.add_page(pdf_reader.pages[i])
                    
                    # Sau đó tạo trang mới chứa bản dịch
                    packet = BytesIO()
                    can = canvas.Canvas(packet, pagesize=A4)
                    
                    # Tạo style cho văn bản tiếng Việt
                    styles = getSampleStyleSheet()
                    vn_style = ParagraphStyle(
                        'vietnamese',
                        fontName='Helvetica',
                        fontSize=12,
                        leading=14,
                        firstLineIndent=0,
                        alignment=4  # justify
                    )
                    
                    # Vẽ tiêu đề cho trang dịch
                    can.setFont("Helvetica-Bold", 16)
                    can.drawString(72, 800, f"Bản dịch - Trang {page_num}")
                    
                    # Vẽ nội dung đã dịch
                    text_object = can.beginText(72, 760)
                    text_object.setFont("Helvetica", 12)
                    
                    # Chia văn bản thành các dòng để tránh tràn trang
                    lines = []
                    for line in translated_content.split('\n'):
                        # Giới hạn độ dài mỗi dòng
                        chunks = [line[i:i+80] for i in range(0, len(line), 80)]
                        lines.extend(chunks)
                    
                    for line in lines:
                        text_object.textLine(line)
                    
                    can.drawText(text_object)
                    can.save()
                    
                    # Di chuyển về đầu buffer
                    packet.seek(0)
                    
                    # Tạo PDF từ buffer
                    new_pdf = PdfReader(packet)
                    
                    # Thêm trang dịch
                    pdf_writer.add_page(new_pdf.pages[0])
                else:
                    # Nếu không có bản dịch, chỉ thêm trang gốc
                    pdf_writer.add_page(pdf_reader.pages[i])
            
            # Lưu kết quả vào buffer
            output = BytesIO()
            pdf_writer.write(output)
            output.seek(0)
            
            return output.getvalue()
        except Exception as e:
            error_msg = f"Lỗi khi tạo file PDF đã dịch: {str(e)}"
            print(error_msg)
            raise Exception(error_msg) 