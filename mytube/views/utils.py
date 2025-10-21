from flask import session

from mytube.models import User, Video


def get_user():
    if 'profile' in session:
        user = User.query.filter_by(user_id=session['profile']['user_id']).first()
        return user
    return None


def get_video(id):
    video = Video.query.filter_by(id=id).first()
    return video
