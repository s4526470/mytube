from flask import Blueprint, session, redirect, url_for, request
from six.moves.urllib.parse import urlencode
from functools import wraps
import logging

from mytube.extensions import auth, db
import mytube.settings as settings
from mytube.models import User
from authlib.integrations.flask_client import OAuth

# 创建 Blueprint
auth_routes = Blueprint('auth_routes', __name__)

# ===== ✅ 重新注册 Auth0 客户端，确保包含 server_metadata_url =====
# （Render 上环境初始化时不一定自动带上）
oauth = OAuth()
auth0 = oauth.register(
    'auth0',
    client_id=settings.AUTH_CLIENT_ID,
    client_secret=settings.AUTH_CLIENT_SECRET,
    client_kwargs={'scope': 'openid profile email'},
    server_metadata_url=f'https://{settings.AUTH_DOMAIN}/.well-known/openid-configuration'
)


# ===== 登录保护装饰器 =====
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            logging.info('Redirecting to login page')
            return redirect(url_for('auth_routes.login'))
        logging.info('User already authenticated')
        return f(*args, **kwargs)
    return decorated


# ===== 登录路由 =====
@auth_routes.route('/login', endpoint='login')
def auth_login_handler():
    redirect_uri = settings.AUTH_CALLBACK_URL
    print("🚀 redirect_uri =", redirect_uri)
    return auth0.authorize_redirect(
        redirect_uri=redirect_uri,
        scope="openid profile email"
    )


# ===== 回调路由 =====
@auth_routes.route('/callback')
def auth_callback_handler():
    print("🔍 Callback request args:", request.args)
    token = auth0.authorize_access_token()
    print("🪙 TOKEN:", token)

    user_info = token.get('userinfo') or auth0.get('userinfo').json()
    print("🧩 USER INFO:", user_info)

    session['jwt_payload'] = user_info
    session['profile'] = {'user_id': user_info['sub']}

    # 数据库中创建用户（如果不存在）
    user = User.query.filter_by(user_id=user_info['sub']).first()
    if not user:
        user = User(
            user_id=user_info['sub'],
            given_name=user_info.get('given_name', ''),
            family_name=user_info.get('family_name', ''),
            email=user_info.get('email', ''),
            picture_url=user_info.get('picture', '')
        )
        db.session.add(user)
        db.session.commit()

    return redirect(url_for('main_routes.home'))


# ===== 登出路由 =====
@auth_routes.route('/logout', methods=['GET'])
def logout():
    session.clear()
    params = {
        'returnTo': url_for('main_routes.home', _external=True),
        'client_id': settings.AUTH_CLIENT_ID
    }
    return redirect(f"https://{settings.AUTH_DOMAIN}/v2/logout?" + urlencode(params))
