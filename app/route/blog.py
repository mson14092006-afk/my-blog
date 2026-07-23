# blog.py — Blueprint cho tất cả route liên quan đến blog (/blog/*)

from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Post
import markdown2
import re

blog_bp = Blueprint("blog", __name__)

def render_markdown(text):
    # Chuyển Markdown → HTML, dùng thư viện markdown2
    return markdown2.markdown(
        text,
        extras=["fenced-code-blocks", "tables", "header-ids", "code-friendly"]
    )

# Helper tạo slug từ tiêu đề bài viết (dùng cho tính năng CRUD)
def slugify(title):
    slug = title.strip().lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "bai-viet"

# Đảm bảo slug không trùng với bài viết khác (thêm hậu tố -2, -3, ... nếu trùng)
def unique_slug(title, exclude_id=None):
    base = slugify(title)
    slug = base
    counter = 1
    while True:
        query = Post.query.filter_by(slug=slug)
        if exclude_id is not None:
            query = query.filter(Post.id != exclude_id)
        if query.first() is None:
            return slug
        counter += 1
        slug = f"{base}-{counter}"
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

# Các route bên dưới phục vụ tính năng CRUD cho mục "Edit blog" trên nav bar

# Route trang quản lý bài viết — /blog/manage (liệt kê tất cả bài viết, kể cả draft)
@blog_bp.route("/manage")
def manage():
    posts = Post.query.order_by(Post.created.desc()).all()
    return render_template("blog/manage.html", posts=posts)

# Route thêm bài viết mới — /blog/new
@blog_bp.route("/new", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        values = request.form
        title = values.get("title", "").strip()
        content = values.get("content", "").strip()
        # Nhan đề và Nội dung là bắt buộc
        if not title or not content:
            return render_template(
                "blog/form.html",
                error="Nhan đề và nội dung không được để trống.",
                form_title="Thêm bài viết",
                values=values,
                post=None,
            )
        post = Post(
            title=title,
            content=content,
            summary=(values.get("summary", "").strip() or None),
            tags=(values.get("tags", "").strip() or None),
            slug=unique_slug(title),
            published=True,
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("blog.manage"))

    empty_values = {"title": "", "summary": "", "tags": "", "content": ""}
    return render_template("blog/form.html", form_title="Thêm bài viết", values=empty_values, post=None)

# Route sửa bài viết — /blog/<slug>/edit
@blog_bp.route("/<slug>/edit", methods=["GET", "POST"])
def edit_post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()

    if request.method == "POST":
        values = request.form
        title = values.get("title", "").strip()
        content = values.get("content", "").strip()
        if not title or not content:
            return render_template(
                "blog/form.html",
                error="Nhan đề và nội dung không được để trống.",
                form_title="Sửa bài viết",
                values=values,
                post=post,
            )
        if title != post.title:
            post.slug = unique_slug(title, exclude_id=post.id)
        post.title = title
        post.content = content
        post.summary = values.get("summary", "").strip() or None
        post.tags = values.get("tags", "").strip() or None
        db.session.commit()
        return redirect(url_for("blog.manage"))

    edit_values = {
        "title": post.title,
        "summary": post.summary or "",
        "tags": post.tags or "",
        "content": post.content,
    }
    return render_template("blog/form.html", form_title="Sửa bài viết", values=edit_values, post=post)

# Route xóa bài viết — /blog/<slug>/delete (chỉ nhận POST để tránh xóa nhầm qua link GET)
@blog_bp.route("/<slug>/delete", methods=["POST"])
def delete_post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("blog.manage"))