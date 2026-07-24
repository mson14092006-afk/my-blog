# conftest.py — Cấu hình pytest và fixtures dùng chung cho toàn bộ test suite
# Pytest tự động load file này trước khi chạy bất kỳ test nào
 
import pytest
from app import create_app, db
from app.models import Post
<<<<<<< HEAD
 
# @pytest.fixture: Chuẩn bị môi trường trước khi test
@pytest.fixture(scope="session") # scope= "session" -> chạy đúng 1 lần duy nhất toàn bộ quá trình chạy test
=======
  
@pytest.fixture(scope="session")
>>>>>>> 359d77e (Edit config.py)
def app():
    """
    Tạo Flask app với config test:
    - TESTING=True: Flask trả về lỗi thay vì trang 500
    - SQLite in-memory: không tạo file, tự reset sau mỗi session
    Truyền env="default" vào create_app() đúng như signature của bạn.
    """
<<<<<<< HEAD
    app = create_app(env="default") # Tạo Flask app
    app.config.update({ # ghi đè config.py
        "TESTING": True, # Bật chế độ test
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:", # Tạo một Database nằm trong RAM. Khi test xong, DB biến mất -> Test nhanh
        "SECRET_KEY": "test-secret",
    })
 
=======
    app = create_app(env="testing")
    
>>>>>>> 359d77e (Edit config.py)
    with app.app_context():
        db.create_all() # Trước khi test chạy, tạo ra database trống chứa các bảng
        yield app # Trong khi test chạy, gặp lênh yield app -> hàm fixture tạm dừng và giao biến app cho hàm test
        db.drop_all() # Cleanup
 
 
@pytest.fixture(scope="function") # scope="function" -> Chạy lại trước mỗi hàm test
def client(app):
    """HTTP test client — dùng để gọi route như browser."""
    return app.test_client() # Test request 
 
 
@pytest.fixture(scope="function")
def db_session(app): # Mỗi test, một session mới
    """
    DB session sạch cho mỗi test function.
    Xóa toàn bộ Post sau mỗi test để các test không ảnh hưởng nhau.
    """
    with app.app_context():
        yield db
        db.session.rollback()
        db.session.query(Post).delete()
        db.session.commit()
<<<<<<< HEAD

=======
  
>>>>>>> 359d77e (Edit config.py)
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

