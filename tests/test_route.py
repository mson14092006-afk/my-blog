# test_route.py — Kiểm tra các HTTP route
# Tên file là test_route.py (không có s) để khớp với file bạn đang có


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
