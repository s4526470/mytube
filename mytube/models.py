from datetime import datetime

from mytube.extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), index=True, unique=True, nullable=False)
    given_name = db.Column(db.String(64), nullable=False)
    family_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(320), unique=True, nullable=False)
    picture_url = db.Column(db.String(200))

    def __repr__(self):
        return f'<{self.given_name} {self.family_name}>'


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    filename = db.Column(db.String(64), nullable=False)
    original_filename = db.Column(db.String(64), nullable=False)
    upload_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content_type = db.Column(db.String(32), nullable=False, default='video/mp4')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('videos', lazy=True))

    def __repr__(self):
        return f'<{self.title} - {self.filename}>'


class VideoComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    video = db.relationship('Video', backref=db.backref('comments', lazy=True))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('comments', lazy=True))

    def __repr__(self):
        return f'<{self.value} - {self.created_at}>'
