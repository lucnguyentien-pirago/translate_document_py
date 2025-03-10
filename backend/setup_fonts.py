#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script tự động cài đặt và kiểm tra fonts Unicode cho PDF
"""

import os
import sys
import pathlib
import tempfile
import urllib.request
import platform
import shutil

def main():
    print("===== KIỂM TRA VÀ CÀI ĐẶT FONTS CHO TIẾNG VIỆT =====")
    
    # Đường dẫn đến thư mục fonts
    current_dir = pathlib.Path(__file__).parent.absolute()
    root_dir = current_dir
    fonts_dir = root_dir / "resources" / "fonts"
    
    # Tạo thư mục fonts nếu chưa tồn tại
    if not fonts_dir.exists():
        print(f"Thư mục fonts không tồn tại. Đang tạo: {fonts_dir}")
        os.makedirs(fonts_dir, exist_ok=True)
    
    # Danh sách font cần tải
    fonts = [
        {
            "name": "DejaVuSans.ttf",
            "url": "https://github.com/dejavu-fonts/dejavu-fonts/raw/master/ttf/DejaVuSans.ttf"
        },
        {
            "name": "DejaVuSans-Bold.ttf",
            "url": "https://github.com/dejavu-fonts/dejavu-fonts/raw/master/ttf/DejaVuSans-Bold.ttf" 
        },
        {
            "name": "NotoSansVietnamese-Regular.ttf",
            "url": "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSansVietnamese/NotoSansVietnamese-Regular.ttf"
        }
    ]
    
    # Tải và kiểm tra từng font
    for font in fonts:
        font_path = fonts_dir / font["name"]
        if font_path.exists():
            print(f"Font {font['name']} đã tồn tại.")
        else:
            print(f"Đang tải font {font['name']}...")
            try:
                urllib.request.urlretrieve(font["url"], font_path)
                print(f"Đã tải font {font['name']} thành công.")
            except Exception as e:
                print(f"Lỗi khi tải font {font['name']}: {str(e)}")
    
    # Kiểm tra fonts hệ thống
    system_fonts_found = check_system_fonts()
    
    # Thông báo kết quả
    print("\n===== KẾT QUẢ KIỂM TRA =====")
    
    # Kiểm tra fonts đã tải
    font_files = list(fonts_dir.glob("*.ttf"))
    if font_files:
        print(f"Đã cài đặt {len(font_files)} fonts trong thư mục: {fonts_dir}")
        for font_file in font_files:
            print(f" - {font_file.name}")
    else:
        print(f"CẢNH BÁO: Không tìm thấy font nào trong thư mục {fonts_dir}")
        
    # Kiểm tra ReportLab
    try:
        import reportlab
        print(f"ReportLab đã được cài đặt, phiên bản: {reportlab.__version__}")
    except ImportError:
        print("CẢNH BÁO: ReportLab chưa được cài đặt. Hãy chạy: pip install reportlab")
    
    # Hướng dẫn thêm
    print("\n===== HƯỚNG DẪN BỔ SUNG =====")
    print("Nếu vẫn gặp vấn đề với tiếng Việt trong PDF, hãy thử các cách sau:")
    print("1. Cài đặt thủ công các font hỗ trợ Unicode/Tiếng Việt vào hệ thống.")
    print("2. Kiểm tra lại backend/app/utils/pdf_handler.py và thay đổi phương pháp tạo PDF.")
    print("3. Thử sử dụng phương pháp canvas trực tiếp thay vì phương pháp Platypus.")
    
    print("\nCài đặt hoàn tất!")

def check_system_fonts():
    """Kiểm tra fonts hỗ trợ Unicode trong hệ thống"""
    print("\nĐang kiểm tra fonts hệ thống...")
    system = platform.system()
    
    if system == "Windows":
        fonts_dir = os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "Fonts")
        unicode_fonts = ["Arial.ttf", "calibri.ttf", "times.ttf", "DejaVuSans.ttf"]
        found_fonts = []
        
        for font in unicode_fonts:
            if os.path.exists(os.path.join(fonts_dir, font)):
                found_fonts.append(font)
        
        if found_fonts:
            print(f"Tìm thấy {len(found_fonts)} fonts Unicode trong hệ thống: {', '.join(found_fonts)}")
        else:
            print("Không tìm thấy fonts Unicode phổ biến trong hệ thống.")
            
        return bool(found_fonts)
        
    elif system == "Linux":
        # Kiểm tra các thư mục font phổ biến trên Linux
        font_dirs = [
            "/usr/share/fonts/truetype",
            "/usr/local/share/fonts",
            os.path.expanduser("~/.local/share/fonts")
        ]
        
        found_any = False
        for font_dir in font_dirs:
            if os.path.exists(font_dir):
                ttf_files = [f for f in os.listdir(font_dir) if f.endswith('.ttf')]
                if ttf_files:
                    print(f"Tìm thấy {len(ttf_files)} fonts TrueType trong {font_dir}")
                    found_any = True
        
        if not found_any:
            print("Không tìm thấy fonts TrueType trong các thư mục thông thường.")
        
        return found_any
        
    elif system == "Darwin":  # macOS
        font_dir = "/Library/Fonts"
        if os.path.exists(font_dir):
            ttf_files = [f for f in os.listdir(font_dir) if f.endswith('.ttf')]
            if ttf_files:
                print(f"Tìm thấy {len(ttf_files)} fonts TrueType trong {font_dir}")
                return True
        
        print("Không tìm thấy fonts TrueType trong thư mục thông thường.")
        return False
    
    print(f"Không thể kiểm tra fonts trên hệ điều hành: {system}")
    return False

if __name__ == "__main__":
    main() 