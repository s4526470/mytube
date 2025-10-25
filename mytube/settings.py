import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 判断运行环境
ENV = os.environ.get("FLASK_ENV", "development")
IS_PRODUCTION = ENV == "production"

####################################
# 🌐 Flask 基础配置
####################################
STATIC_DIR = os.environ.get("STATIC_DIR", "static/")
SECRET_KEY = os.environ.get("SECRET_KEY", "a-very-bad-secret-key-please-use-something-else")

# Flask-Session
FLASK_SESSION_TYPE = os.environ.get("FLASK_SESSION_TYPE", "filesystem")

####################################
# 🗄️ 数据库配置
####################################
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///mytube.sqlite3")
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", "False").lower() == "true"

####################################
# 🧱 Flask-Admin
####################################
FLASK_ADMIN_NAME = os.environ.get("FLASK_ADMIN_NAME", "MyTube Admin")
FLASK_ADMIN_TEMPLATE_MODE = os.environ.get("FLASK_ADMIN_TEMPLATE_MODE", "bootstrap3")

####################################
# 📁 上传配置
####################################
UPLOADS_DEFAULT_DEST = os.environ.get("UPLOADS_DEFAULT_DEST", "mytube/static/")
ALLOWED_UPLOAD_TYPES = os.environ.get("UPLOADED_FILES_ALLOW", "mp4,m4v,flv")

####################################
# 🔐 Auth0 配置
####################################
AUTH_NAME = os.environ.get("AUTH_NAME", "auth0")
AUTH_CLIENT_ID = os.environ.get("AUTH_CLIENT_ID")
AUTH_CLIENT_SECRET = os.environ.get("AUTH_CLIENT_SECRET")
AUTH_DOMAIN = os.environ.get("AUTH_DOMAIN")

# 🚀 动态回调 URL：优先取环境变量，否则根据环境自动判断
AUTH_CALLBACK_URL = os.environ.get("AUTH_CALLBACK_URL")

if not AUTH_CALLBACK_URL:
    if IS_PRODUCTION:
        AUTH_CALLBACK_URL = "https://video.strongestben.com/auth/callback"
    else:
        AUTH_CALLBACK_URL = "http://127.0.0.1:5000/auth/callback"

# 登出与基础地址
AUTH_LOGOUT_URL = f"https://{AUTH_DOMAIN}/v2/logout"
AUTH_BASE_URL = f"https://{AUTH_DOMAIN}"
