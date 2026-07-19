# models.py — định nghĩa cấu trúc bảng trong database
# Mỗi class = một bảng, mỗi Column = một cột

from app import db
from datetime import datetime

class Post(db.Model):
    # Tên bảng trong database
    __tablename__ = "posts"
    # Cấu trúc bảng
    id        = db.Column(db.Integer, primary_key=True) # Tạo cột id kiểu Integer, là primary key (không trùng lặp, tự tăng)
    tags      = db.Column(db.String(200)) # Danh sách tag, VD: "python, flask"
    slug      = db.Column(db.String(200), unique=True, nullable=False)  # URL-friendly string VD: "my-first-post"
    title     = db.Column(db.String(300), nullable=False) # Tiêu đề bài viết
    summary   = db.Column(db.String(500))                               
    content   = db.Column(db.Text, nullable=False) # Nội dung bài viết (Markdown)                     
    created   = db.Column(db.DateTime, default=datetime.utcnow) # Ngày tạo bài viết, mặc định là thời điểm hiện tại
    published = db.Column(db.Boolean, default=True) # Bài viết đã được publish chưa, mặc định là True                
    def tag_list(self):
        # Trả về danh sách các tag, VD: "python, flask" → ["python", "flask"]
        if not self.tags:
            return []
        return [t.strip() for t in self.tags.split(",") if t.strip()]