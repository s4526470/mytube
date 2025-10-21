from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_migrate import Migrate
from flask_uploads import UploadSet
from flask_restful import Api
from authlib.integrations.flask_client import OAuth

import mytube.settings as settings

# Flask-SQLAlchemy
db = SQLAlchemy()

# Flask-Migrate
migrate = Migrate()

# Flask-RESTFul
api = Api()

# Flask-Uploads
allowed_uploads = tuple(settings.ALLOWED_UPLOAD_TYPES.split(','))
videos = UploadSet('videos', allowed_uploads)

# Flask-Admin
admin = Admin(name=settings.FLASK_ADMIN_NAME, template_mode=settings.FLASK_ADMIN_TEMPLATE_MODE)

# OAuth (Auth0)
oauth = OAuth()
auth = oauth.register(
    name=settings.AUTH_NAME,
    client_id=settings.AUTH_CLIENT_ID,
    client_secret=settings.AUTH_CLIENT_SECRET,
    api_base_url=f"https://{settings.AUTH_DOMAIN}",
    access_token_url=f"https://{settings.AUTH_DOMAIN}/oauth/token",
    authorize_url=f"https://{settings.AUTH_DOMAIN}/authorize",
    userinfo_endpoint=f"https://{settings.AUTH_DOMAIN}/userinfo",
    client_kwargs={
        "scope": "openid profile email"
    }
)
