from deep_translator import GoogleTranslator
from typing import List, Dict, Union, Any

class Translator:
    def __init__(self):
        self.translator = GoogleTranslator(source='auto', target='vi')
    
    def translate_text(self, text: str) -> str:
        """
        Dịch văn bản đơn từ bất kỳ ngôn ngữ nào sang tiếng Việt
        """
        if not text or text.isspace():
            return text
        
        try:
            # Giới hạn độ dài văn bản để tránh lỗi từ API
            chunks = self._split_text(text, 4800)  # GoogleTranslator limit ~5000 chars
            translated_chunks = [self.translator.translate(chunk) for chunk in chunks if chunk]
            return ' '.join(translated_chunks)
        except Exception as e:
            print(f"Lỗi khi dịch văn bản: {str(e)}")
            return text
    
    def translate_pdf_content(self, pdf_content: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Dịch nội dung từ file PDF
        """
        result = []
        for page in pdf_content:
            translated_content = self.translate_text(page["content"])
            result.append({
                "page": page["page"],
                "content": page["content"],
                "translated_content": translated_content
            })
        return result
    
    def translate_excel_content(self, excel_content: List[Dict[str, List[Dict[str, str]]]]) -> List[Dict[str, List[Dict[str, str]]]]:
        """
        Dịch nội dung từ file Excel
        """
        result = []
        for sheet_data in excel_content:
            translated_cells = []
            for cell in sheet_data["cells"]:
                translated_content = self.translate_text(cell["content"])
                translated_cells.append({
                    "address": cell["address"],
                    "content": cell["content"],
                    "translated_content": translated_content
                })
            
            result.append({
                "sheet_name": sheet_data["sheet_name"],
                "cells": translated_cells
            })
        
        return result
    
    def translate_word_content(self, word_content: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Dịch nội dung từ file Word
        """
        result = []
        for paragraph in word_content:
            translated_content = self.translate_text(paragraph["content"])
            result.append({
                "paragraph": paragraph["paragraph"],
                "content": paragraph["content"],
                "translated_content": translated_content
            })
        
        return result
    
    def _split_text(self, text: str, max_length: int) -> List[str]:
        """
        Chia văn bản thành các đoạn nhỏ hơn max_length
        """
        # Nếu văn bản ngắn hơn max_length, trả về nguyên văn
        if len(text) <= max_length:
            return [text]
        
        # Chia văn bản thành các đoạn nhỏ
        chunks = []
        
        # Tìm điểm cắt phù hợp (kết thúc câu hoặc khoảng trắng)
        current_pos = 0
        while current_pos < len(text):
            # Tìm điểm kết thúc lý tưởng trong khoảng max_length
            end_pos = min(current_pos + max_length, len(text))
            
            # Nếu đã đến cuối văn bản, thêm phần còn lại và thoát
            if end_pos == len(text):
                chunks.append(text[current_pos:])
                break
            
            # Tìm điểm kết thúc câu gần nhất (.!?)
            last_sentence_end = max(
                text.rfind('.', current_pos, end_pos),
                text.rfind('!', current_pos, end_pos),
                text.rfind('?', current_pos, end_pos)
            )
            
            # Nếu tìm thấy điểm kết thúc câu, dùng điểm đó
            if last_sentence_end > current_pos:
                end_pos = last_sentence_end + 1
            else:
                # Không tìm thấy điểm kết thúc câu, tìm khoảng trắng gần nhất
                last_space = text.rfind(' ', current_pos, end_pos)
                if last_space > current_pos:
                    end_pos = last_space + 1
            
            # Thêm đoạn văn đã cắt vào danh sách
            chunks.append(text[current_pos:end_pos])
            current_pos = end_pos
        
        return chunks 