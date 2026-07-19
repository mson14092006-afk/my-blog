# blog.py — Blueprint cho tất cả route liên quan đến blog (/blog/*)

from flask import Blueprint, render_template, request
from app.models import Post
import markdown2

blog_bp = Blueprint("blog", __name__)

def render_markdown(text):
    # Chuyển Markdown → HTML, dùng thư viện markdown2
    return markdown2.markdown(
        text,
        extras=["fenced-code-blocks", "tables", "header-ids", "code-friendly"]
    )
# Route cho trang chủ của blog
@blog_bp.route("/")
def index():
    # Trang danh sách bài viết
    tag = request.args.get("tag")  # lọc theo tag nếu có

    if tag:
        posts = Post.query.filter(
            Post.published == True,
            Post.tags.contains(tag)
        ).order_by(Post.created.desc()).all()
    else:
        posts = Post.query.filter_by(published=True) \
            .order_by(Post.created.desc()).all()

    # Gom tất cả tags để hiện filter bar
    all_tags = set()
    for p in Post.query.filter_by(published=True).all():
        all_tags.update(p.tag_list())

    return render_template("blog/index.html",
                           posts=posts,
                           all_tags=sorted(all_tags),
                           active_tag=tag)
# Route cho trang chi tiết bài viết
@blog_bp.route("/<slug>")
def post(slug):
    """Trang chi tiết bài viết — /blog/<slug>"""
    p = Post.query.filter_by(slug=slug, published=True).first_or_404()
    p.html_content = render_markdown(p.content)  # convert Markdown → HTML trước khi truyền vào template
    return render_template("blog/post.html", post=p)