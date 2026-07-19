from flask import Blueprint, render_template
from app.models import Post
# Blueprint cho các route chính của app (không phải blog)
main_bp = Blueprint("main", __name__)
# Route cho trang chủ của app
@main_bp.route("/")
def home():
    # Lấy 3 bài mới nhất để hiện ở trang chủ
    recent_posts = Post.query.filter_by(published=True) \
        .order_by(Post.created.desc()).limit(3).all()
    return render_template("home.html", recent_posts=recent_posts)