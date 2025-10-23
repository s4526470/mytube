import werkzeug
import werkzeug.utils
import werkzeug.datastructures

# --- 👇 加上这一段 monkey patch 来兼容旧版 flask_uploads ---
werkzeug.secure_filename = werkzeug.utils.secure_filename
werkzeug.FileStorage = werkzeug.datastructures.FileStorage
# ----------------------------------------------------------

from flask import Flask
from flask_uploads import configure_uploads

from mytube.extensions import videos
import mytube.settings as settings

from mytube.extensions import (
    db,
    migrate,
    admin,
    oauth,
    api,
)


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)
    oauth.init_app(app)
    api.init_app(app)
    configure_uploads(app, videos)


def create_app(config_object="mytube.settings"):
    print("AUTH CALLBACK URL:", settings.AUTH_CALLBACK_URL)
    app = Flask(__name__, static_folder=settings.STATIC_DIR)
    app.config.from_object(config_object)

    # Register blueprints
    from mytube.views.main import main_routes
    from mytube.views.auth import auth_routes
    app.register_blueprint(main_routes)
    app.register_blueprint(auth_routes, url_prefix='/auth')

    # Register Flask-RESTFul endpoints
    import mytube.api as api_resource
    api.add_resource(
        api_resource.Comment,
        '/api/comments/<int:video_id>',
        '/api/comments'
    )

    # Make utils available in any Flask template.
    @app.context_processor
    def inject_utils():
        import mytube.utils as utils
        return dict(utils=utils, title='MyTube')

    # Register extensions at the end.
    register_extensions(app)

    return app



# if __name__ == '__main__':
#     create_app().run(debug=True)
