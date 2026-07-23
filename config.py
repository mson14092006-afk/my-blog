import os
# Luôn lấy vị trí thật của file config.py, không quan tâm chạy ở đâu, để tránh lỗi khi chạy gunicorn
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Cấu hình app Flask và SQLAlchemy
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-prod")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_DIR = os.path.join(BASE_DIR, "posts")
    BLOG_AUTHOR = "Son Nguyen"
    BLOG_TITLE = "Son's DevOps Blog"
    BLOG_DESCRIPTION = "Notes on cloud infrastructure, Kubernetes, and the journey from student to engineer."
# Cấu hình riêng cho môi trường development và production (Kế thừa từ Config)
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
# Chọn config dựa trên biến môi trường FLASK_ENV, mặc định là development
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}