# Đăng ký app Flask và SQLAlchemy, tạo bảng trong SQLite nếu chưa có
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_migrate import Migrate
import os

# db là object SQLAlchemy dùng chung, import ở models.py và các nơi khác
db = SQLAlchemy()
migrate = Migrate()

def create_app(env="default"): 
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config[env]) # Lấy config tương ứng với môi trường (development, production, testing) trong config.py

    # Gán biến môi trường DATABASE_URL vào config SQLAlchemy sau khi đã load config từ config.py 
    if env in ("development", "production"): # Chỉ set DATABASE_URL trong môi trường dev và prod, không set trong test để dùng SQLite in-memory
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
    # Gắn SQLAlchemy vào app
    db.init_app(app)
    # Gán Flask-Migrate vào app và db
    migrate.init_app(app, db)

    # Đăng ký Blueprint — mỗi blueprint là một nhóm route
    from app.route.main import main_bp
    from app.route.blog import blog_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(blog_bp, url_prefix="/blog")

    return app