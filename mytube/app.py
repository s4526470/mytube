import werkzeug
import werkzeug.utils
import werkzeug.datastructures

# --- 👇 monkey patch 兼容 flask_uploads ---
werkzeug.secure_filename = werkzeug.utils.secure_filename
werkzeug.FileStorage = werkzeug.datastructures.FileStorage
# ----------------------------------------------------------

from flask import Flask
from flask_uploads import configure_uploads

from mytube.extensions import videos, db, migrate, admin, oauth, api
import mytube.settings as settings


def register_extensions(app):
    """初始化 Flask 扩展"""
    db.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)
    oauth.init_app(app)   # ✅ 初始化 OAuth
    api.init_app(app)
    configure_uploads(app, videos)

    # ✅ 在初始化 OAuth 之后，注册 Auth0 客户端
    with app.app_context():
        oauth.register(
            name='auth0',
            client_id=settings.AUTH_CLIENT_ID,
            client_secret=settings.AUTH_CLIENT_SECRET,
            client_kwargs={'scope': 'openid profile email'},
            server_metadata_url=f'https://{settings.AUTH_DOMAIN}/.well-known/openid-configuration'
        )


def create_app(config_object="mytube.settings"):
    """创建 Flask 应用实例"""
    print("AUTH CALLBACK URL:", settings.AUTH_CALLBACK_URL)
    app = Flask(__name__, static_folder=settings.STATIC_DIR)
    app.config.from_object(config_object)

    # ✅ 初始化扩展
    register_extensions(app)

    # ✅ 注册蓝图（一定要放在 register_extensions 之后）
    from mytube.views.main import main_routes
    from mytube.views.auth import auth_routes
    app.register_blueprint(main_routes)
    app.register_blueprint(auth_routes, url_prefix='/auth')

    # ✅ 注册 Flask-RESTful 接口
    import mytube.api as api_resource
    api.add_resource(
        api_resource.Comment,
        '/api/comments/<int:video_id>',
        '/api/comments'
    )

    # ✅ 模板上下文工具
    @app.context_processor
    def inject_utils():
        import mytube.utils as utils
        return dict(utils=utils, title='MyTube')

    return app
