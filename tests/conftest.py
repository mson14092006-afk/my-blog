# conftest.py — Cấu hình pytest và fixtures dùng chung cho toàn bộ test suite
# Pytest tự động load file này trước khi chạy bất kỳ test nào
 
import pytest
from app import create_app, db
from app.models import Post
  
@pytest.fixture(scope="session")
def app():
    """Tạo app Flask cho toàn bộ test suite."""
    app = create_app(env="testing")
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
 
 
@pytest.fixture(scope="function")
def client(app):
    """HTTP test client — dùng để gọi route như browser."""
    return app.test_client()
 
 
@pytest.fixture(scope="function")
def db_session(app):
    """
    DB session sạch cho mỗi test function.
    Xóa toàn bộ Post sau mỗi test để các test không ảnh hưởng nhau.
    """
    with app.app_context():
        yield db
        db.session.rollback()
        db.session.query(Post).delete()
        db.session.commit()
  
@pytest.fixture
def sample_post(db_session):
    """Tạo một bài viết mẫu đã published vào DB."""
    post = Post(
        slug="test-post",
        title="Test Post Title",
        summary="A short summary for testing.",
        content="# Hello\n\nThis is **markdown** content.",
        published=True,
    )
    db_session.session.add(post)
    db_session.session.commit()
    return post
 
 
@pytest.fixture
def draft_post(db_session):
    """Tạo một bài viết nháp (published=False) — không hiện ra ngoài."""
    post = Post(
        slug="draft-post",
        title="Draft Post",
        summary="This should not be visible.",
        content="Draft content.",
        published=False,
    )
    db_session.session.add(post)
    db_session.session.commit()
    return post

