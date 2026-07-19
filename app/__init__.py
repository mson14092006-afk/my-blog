# Đăng ký app Flask và SQLAlchemy, tạo bảng trong SQLite nếu chưa có
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

# db là object SQLAlchemy dùng chung, import ở models.py và các nơi khác
db = SQLAlchemy()

def create_app(env="default"): 
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config[env])

    # Gắn SQLAlchemy vào app
    db.init_app(app)
    # Đăng ký Blueprint — mỗi blueprint là một nhóm route
    from app.route.main import main_bp
    from app.route.blog import blog_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(blog_bp, url_prefix="/blog")

    # Tạo bảng trong SQLite nếu chưa có
    with app.app_context():
        db.create_all()

    return app