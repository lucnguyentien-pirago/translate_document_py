from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Form
from fastapi.responses import JSONResponse, StreamingResponse
import io
import os
from typing import List, Dict, Optional
import tempfile
import shutil
import urllib.parse

from ..utils.pdf_handler import PDFHandler
from ..utils.excel_handler import ExcelHandler
from ..utils.word_handler import WordHandler
from ..utils.translator import Translator

router = APIRouter(
    prefix="/api/documents",
    tags=["documents"],
    responses={404: {"description": "Not found"}},
)

pdf_handler = PDFHandler()
excel_handler = ExcelHandler()
word_handler = WordHandler()
translator = Translator()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
):
    """
    Upload a document and extract its content
    """
    try:
        # Đọc nội dung file
        file_content = await file.read()
        file_extension = os.path.splitext(file.filename)[1].lower()
        
        # Xử lý theo loại file
        if file_extension == ".pdf":
            extracted_content = pdf_handler.extract_text_from_pdf(file_content)
            file_type = "pdf"
        elif file_extension in [".xlsx", ".xls"]:
            extracted_content = excel_handler.extract_text_from_excel(file_content)
            file_type = "excel"
        elif file_extension in [".docx", ".doc"]:
            extracted_content = word_handler.extract_text_from_docx(file_content)
            file_type = "word"
        else:
            raise HTTPException(status_code=400, detail="Định dạng file không được hỗ trợ")
        
        # Trả về nội dung đã trích xuất và loại file
        return {
            "success": True,
            "file_type": file_type,
            "content": extracted_content,
            "filename": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/translate")
async def translate_document(
    file_type: str = Form(...),
    content: str = Form(...),
    original_filename: str = Form(...)
):
    """
    Translate document content
    """
    try:
        # Parse JSON content string
        import json
        content_data = json.loads(content)
        
        # Dịch nội dung theo loại file
        if file_type == "pdf":
            translated_content = translator.translate_pdf_content(content_data)
        elif file_type == "excel":
            translated_content = translator.translate_excel_content(content_data)
        elif file_type == "word":
            translated_content = translator.translate_word_content(content_data)
        else:
            raise HTTPException(status_code=400, detail="Loại file không hợp lệ")
        
        return {
            "success": True,
            "translated_content": translated_content,
            "original_filename": original_filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/export")
async def export_document(
    background_tasks: BackgroundTasks,
    file_type: str = Form(...),
    translated_content: str = Form(...),
    original_file: UploadFile = File(...),
):
    """
    Export translated document
    """
    try:
        # Đọc nội dung file gốc
        original_content = await original_file.read()
        
        # Parse JSON của nội dung đã dịch
        import json
        translated_data = json.loads(translated_content)
        
        # Debug thông tin
        print(f"File type: {file_type}")
        print(f"Filename: {original_file.filename}")
        print(f"Translated data structure: {type(translated_data)}")
        if len(translated_data) > 0:
            if file_type == "pdf":
                print(f"Sample translated item: {translated_data[0].keys()}")
                if "translated_content" in translated_data[0]:
                    print(f"Has translated content: {bool(translated_data[0].get('translated_content'))}")
        
        # Tạo file mới với nội dung đã dịch
        if file_type == "pdf":
            output_content = pdf_handler.create_translated_pdf(original_content, translated_data)
            media_type = "application/pdf"
            filename = f"translated_{original_file.filename}"
        elif file_type == "excel":
            output_content = excel_handler.create_translated_excel(original_content, translated_data)
            media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            filename = f"translated_{original_file.filename}"
        elif file_type == "word":
            output_content = word_handler.create_translated_docx(original_content, translated_data)
            media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            filename = f"translated_{original_file.filename}"
        else:
            raise HTTPException(status_code=400, detail="Loại file không hợp lệ")
        
        # Xử lý tên file với mã hóa URL để tránh vấn đề với ký tự tiếng Việt
        encoded_filename = urllib.parse.quote(filename)
        
        # Trả về file đã dịch
        return StreamingResponse(
            io.BytesIO(output_content),
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"}
        )
    except Exception as e:
        # In ra lỗi chi tiết để debug
        import traceback
        error_detail = f"{str(e)}\n{traceback.format_exc()}"
        print(error_detail)
        raise HTTPException(status_code=500, detail=str(e)) 