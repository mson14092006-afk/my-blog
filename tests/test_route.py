# test_route.py — Kiểm tra các HTTP route

class TestHomeRoute:
    """Route / — trang chủ"""

    def test_home_returns_200(self, client):
        r = client.get("/")
        assert r.status_code == 200

    def test_home_shows_author_name(self, client):
        """Trang chủ phải có tên tác giả."""
        r = client.get("/")
        assert b"Son Nguyen" in r.data

    def test_home_shows_recent_posts(self, client, sample_post):
        """Trang chủ hiện bài viết mới nhất."""
        r = client.get("/")
        assert b"Test Post Title" in r.data

    def test_home_hides_drafts(self, client, draft_post):
        """Bài nháp không được hiện ở trang chủ."""
        r = client.get("/")
        assert b"Draft Post" not in r.data


class TestBlogIndexRoute:
    """Route /blog/ — danh sách bài viết"""

    def test_blog_index_returns_200(self, client):
        r = client.get("/blog/")
        assert r.status_code == 200

    def test_blog_index_shows_published_post(self, client, sample_post):
        r = client.get("/blog/")
        assert b"Test Post Title" in r.data

    def test_blog_index_hides_draft(self, client, draft_post):
        """Bài draft không xuất hiện trong danh sách."""
        r = client.get("/blog/")
        assert b"Draft Post" not in r.data


class TestBlogPostRoute:
    """Route /blog/<slug> — chi tiết bài viết"""

    def test_post_detail_returns_200(self, client, sample_post):
        r = client.get("/blog/test-post")
        assert r.status_code == 200

    def test_post_detail_shows_title(self, client, sample_post):
        r = client.get("/blog/test-post")
        assert b"Test Post Title" in r.data

    def test_post_detail_renders_markdown(self, client, sample_post):
        """Markdown phải được convert thành HTML."""
        r = client.get("/blog/test-post")
        assert b"<h1" in r.data
        assert b"<strong>" in r.data

    def test_nonexistent_slug_returns_404(self, client):
        r = client.get("/blog/this-does-not-exist")
        assert r.status_code == 404

    def test_draft_returns_404(self, client, draft_post):
        """Truy cập trực tiếp bài draft phải trả về 404."""
        r = client.get("/blog/draft-post")
        assert r.status_code == 404


# test cho tính năng CRUD ở mục "Edit blog"
class TestBlogManageRoute:
    """Route /blog/manage — trang quản lý bài viết"""

    def test_manage_returns_200(self, client):
        r = client.get("/blog/manage")
        assert r.status_code == 200

    def test_manage_shows_drafts_too(self, client, draft_post):
        """Khác với /blog/, trang manage phải hiện cả bài draft."""
        r = client.get("/blog/manage")
        assert b"Draft Post" in r.data


class TestBlogNewRoute:
    """Route /blog/new — thêm bài viết mới"""

    def test_new_form_returns_200(self, client):
        r = client.get("/blog/new")
        assert r.status_code == 200

    def test_create_post_success(self, client, db_session):
        r = client.post("/blog/new", data={
            "title": "Bai Viet Moi",
            "summary": "Tom tat",
            "tags": "python, flask",
            "content": "Noi dung bai viet moi.",
        }, follow_redirects=True)
        assert r.status_code == 200
        assert b"Bai Viet Moi" in r.data

        from app.models import Post
        post = Post.query.filter_by(title="Bai Viet Moi").first()
        assert post is not None
        assert post.slug  # slug được tự sinh

    def test_create_post_missing_title_shows_error(self, client, db_session):
        r = client.post("/blog/new", data={
            "title": "",
            "content": "Noi dung",
        })
        assert r.status_code == 200
        assert "không được để trống".encode("utf-8") in r.data

    def test_create_post_missing_content_shows_error(self, client, db_session):
        r = client.post("/blog/new", data={
            "title": "Tieu de",
            "content": "",
        })
        assert r.status_code == 200
        assert "không được để trống".encode("utf-8") in r.data


class TestBlogEditRoute:
    """Route /blog/<slug>/edit — sửa bài viết"""

    def test_edit_form_returns_200(self, client, sample_post):
        r = client.get(f"/blog/{sample_post.slug}/edit")
        assert r.status_code == 200
        assert b"Test Post Title" in r.data

    def test_edit_form_nonexistent_returns_404(self, client):
        r = client.get("/blog/khong-ton-tai/edit")
        assert r.status_code == 404

    def test_edit_post_updates_fields(self, client, sample_post):
        r = client.post(f"/blog/{sample_post.slug}/edit", data={
            "title": "Test Post Title",
            "summary": "Tom tat moi",
            "content": "Noi dung da duoc sua.",
        }, follow_redirects=True)
        assert r.status_code == 200

        from app.models import Post
        updated = Post.query.filter_by(id=sample_post.id).first()
        assert updated.content == "Noi dung da duoc sua."
        assert updated.summary == "Tom tat moi"

    def test_edit_post_missing_content_shows_error(self, client, sample_post):
        r = client.post(f"/blog/{sample_post.slug}/edit", data={
            "title": "Test Post Title",
            "content": "",
        })
        assert r.status_code == 200
        assert "không được để trống".encode("utf-8") in r.data


class TestBlogDeleteRoute:
    """Route /blog/<slug>/delete — xoá bài viết"""

    def test_delete_post_removes_it(self, client, sample_post):
        slug = sample_post.slug
        r = client.post(f"/blog/{slug}/delete", follow_redirects=True)
        assert r.status_code == 200

        from app.models import Post
        assert Post.query.filter_by(slug=slug).first() is None

    def test_delete_nonexistent_returns_404(self, client):
        r = client.post("/blog/khong-ton-tai/delete")
        assert r.status_code == 404