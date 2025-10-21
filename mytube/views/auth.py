from flask import Blueprint, session, redirect, url_for, jsonify, request, Response
from six.moves.urllib.parse import urlencode

from functools import wraps
import logging

from mytube.extensions import auth
import mytube.settings as settings
from mytube.extensions import db
from mytube.models import User

auth_routes = Blueprint('auth_routes', __name__)


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            logging.info('Redirecting to login page')
            return redirect(url_for('auth_routes.login'))
        logging.info('User already authenticated')
        return f(*args, **kwargs)
    return decorated


# @auth_routes.route('/login')
# def login():
#     return auth.authorize_redirect(redirect_uri=settings.AUTH_CALLBACK_URL)
@auth_routes.route('/login', endpoint='login')
def auth_login_handler():
    redirect_uri = settings.AUTH_CALLBACK_URL
    print("🚀 redirect_uri =", redirect_uri)
    return auth.authorize_redirect(
        redirect_uri=redirect_uri,
        scope="openid profile email"   # ✅ 必须有 openid！
    )


@auth_routes.route('/callback')
def auth_callback_handler():
    print("🔍 Callback request args:", request.args)
    token = auth.authorize_access_token()
    print("🪙 TOKEN:", token)
    user_info = auth.get('userinfo').json()

    print("🧩 USER INFO:", user_info)   # ✅ 打印出来看看

    session['jwt_payload'] = user_info
    session['profile'] = {
        'user_id': user_info['sub']
    }

    # Check if user is in the database, if not, add them.
    user = User.query.filter_by(user_id=user_info['sub']).first()
    if not user:
        user = User(user_id=user_info['sub'], given_name=user_info['given_name'], family_name=user_info['family_name'],
                    email=user_info['email'], picture_url=user_info['picture'])
        db.session.add(user)
        db.session.commit()

    return redirect(url_for('main_routes.home'))


@auth_routes.route('/logout', methods=['GET'])
def logout():
    session.clear()
    params = {'redirect_uri': url_for('main_routes.home', _external=True), 'client_id': settings.AUTH_CLIENT_ID}
    return redirect(settings.AUTH_LOGOUT_URL + '?' + urlencode(params))
