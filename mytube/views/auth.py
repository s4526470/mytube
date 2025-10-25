from flask import Blueprint, session, redirect, url_for, request
from six.moves.urllib.parse import urlencode
from functools import wraps
import logging

from mytube.extensions import oauth, db  # ✅ 从 oauth 导入（不是 auth）
import mytube.settings as settings
from mytube.models import User

auth_routes = Blueprint('auth_routes', __name__)

# 🔒 登录保护装饰器
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            logging.info('Redirecting to login page')
            return redirect(url_for('auth_routes.login'))
        logging.info('User already authenticated')
        return f(*args, **kwargs)
    return decorated


# 🚪 登录路由
@auth_routes.route('/login', endpoint='login')
def auth_login_handler():
    redirect_uri = settings.AUTH_CALLBACK_URL
    print("🚀 redirect_uri =", redirect_uri)
    return oauth.auth0.authorize_redirect(   # ✅ 改成 oauth.auth0
        redirect_uri=redirect_uri,
        scope="openid profile email"
    )


# 🎫 回调路由
@auth_routes.route('/callback')
def auth_callback_handler():
    print("🔍 Callback request args:", request.args)
    token = oauth.auth0.authorize_access_token()  # ✅ 改成 oauth.auth0
    print("🪙 TOKEN:", token)

    user_info = token.get('userinfo') or oauth.auth0.get('userinfo').json()
    print("🧩 USER INFO:", user_info)

    session['jwt_payload'] = user_info
    session['profile'] = {'user_id': user_info['sub']}

    # 将新用户写入数据库
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


# 🚪 登出路由
@auth_routes.route('/logout', methods=['GET'])
def logout():
    session.clear()
    params = {
        'returnTo': url_for('main_routes.home', _external=True),
        'client_id': settings.AUTH_CLIENT_ID
    }
    return redirect(f"https://{settings.AUTH_DOMAIN}/v2/logout?" + urlencode(params))
