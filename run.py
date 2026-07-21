import os
from app import create_app
# Lấy biến môi trường FLASK_ENV, mặc định là "development"
env = os.environ.get("FLASK_ENV", "development")
# Tạo app Flask
app = create_app(env)

# Để test local, không cần qua gunicorn
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=(env == "development"))
