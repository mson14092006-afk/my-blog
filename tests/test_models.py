# test_models.py — Kiểm tra logic của model Post
import pytest
from sqlalchemy.exc import IntegrityError
from app.models import Post


class TestPostModel:

    def test_create_post(self, db_session):
        """Tạo post mới và lưu vào DB thành công."""
        post = Post(slug="new-post", title="New Post", content="Some content.")
        db_session.session.add(post)
        db_session.session.commit()

        saved = Post.query.filter_by(slug="new-post").first()
        assert saved is not None
        assert saved.title == "New Post"

    def test_published_default_is_true(self, db_session):
        """published mặc định là True khi không set."""
        post = Post(slug="default-pub", title="T", content="C")
        db_session.session.add(post)
        db_session.session.commit()

        assert Post.query.filter_by(slug="default-pub").first().published is True

    def test_created_timestamp_auto_set(self, db_session):
        """created timestamp tự động set khi tạo mới."""
        post = Post(slug="ts-post", title="T", content="C")
        db_session.session.add(post)
        db_session.session.commit()

        assert post.created is not None

    def test_slug_must_be_unique(self, db_session):
        """Hai post không thể có cùng slug."""
        db_session.session.add(Post(slug="dup", title="First", content="C"))
        db_session.session.commit()

        db_session.session.add(Post(slug="dup", title="Second", content="C"))
        with pytest.raises(IntegrityError):
            db_session.session.commit()
        db_session.session.rollback()

    def test_title_is_required(self, db_session):
        """title nullable=False — không được để trống."""
        post = Post(slug="no-title", title=None, content="C")
        db_session.session.add(post)
        with pytest.raises(Exception):
            db_session.session.commit()
        db_session.session.rollback()

    def test_content_is_required(self, db_session):
        """content nullable=False — không được để trống."""
        post = Post(slug="no-content", title="T", content=None)
        db_session.session.add(post)
        with pytest.raises(Exception):
            db_session.session.commit()
        db_session.session.rollback()

    def test_summary_is_optional(self, db_session):
        """summary có thể để None."""
        post = Post(slug="no-summary", title="T", content="C", summary=None)
        db_session.session.add(post)
        db_session.session.commit()

        assert Post.query.filter_by(slug="no-summary").first() is not None
