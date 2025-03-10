from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from .routers import documents

app = FastAPI(
    title="Document Translation API",
    description="API để dịch các tài liệu từ nhiều định dạng khác nhau",
    version="1.0.0"
)

# Cấu hình CORS (Cross-Origin Resource Sharing) chi tiết hơn
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],  # Chỉ cho phép frontend
    allow_credentials=True,
    allow_methods=["*"],  # Hoặc chỉ định cụ thể: ["GET", "POST", "PUT", "DELETE"]
    allow_headers=["*"],  # Hoặc chỉ định cụ thể các header cần thiết
)

# Thêm router
app.include_router(documents.router)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Chào mừng đến với Document Translation API"}

# Tạo thư mục uploads nếu không tồn tại
os.makedirs("uploads", exist_ok=True)

# Khởi chạy ứng dụng với uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 