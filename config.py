import os
# Luôn lấy vị trí thật của file config.py, không quan tâm chạy ở đâu, để tránh lỗi khi chạy gunicorn
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Cấu hình app Flask và SQLAlchemy
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-prod")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_DIR = os.path.join(BASE_DIR, "posts")
    BLOG_AUTHOR = "Son Nguyen"
    BLOG_TITLE = "Son's DevOps Blog"
    BLOG_DESCRIPTION = "Notes on cloud infrastructure, Kubernetes, and the journey from student to engineer."
# Cấu hình riêng cho môi trường development và production (Kế thừa từ Config)
class DevelopmentConfig(Config):
    DEBUG = True # Hiển thị lỗi chi tiết khi chạy app trong môi trường development
 
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory" # Sử dụng database SQLite trong môi trường test
    SECRET_KEY = "test-secret" # Khóa bí mật cho môi trường test, không quan trọng

class ProductionConfig(Config):
    DEBUG = False # Tắt chế độ debug trong môi trường production
config = {
    "testing": TestingConfig,
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
