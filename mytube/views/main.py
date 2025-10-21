from flask import Blueprint, session, redirect, url_for, jsonify, request, Response, render_template, flash
from flask_uploads import UploadNotAllowed

from uuid import uuid4

from mytube.views.auth import require_auth
from mytube.models import Video, db
from mytube.views.utils import get_user, get_video
from mytube.extensions import videos, allowed_uploads

main_routes = Blueprint('main_routes', __name__)


@main_routes.route('/', methods=['GET', 'POST'])
def home():
    search = request.form.get('search')
    user = get_user()
    if search:
        videos = Video.query.filter(Video.title.contains(search))
    else:
        videos = Video.query.order_by(Video.upload_datetime.desc()).all()

    return render_template('main/home/index.html', user=user, videos=videos)


@main_routes.route('/dashboard', methods=['GET', 'POST'])
@require_auth
def dashboard():
    user = get_user()

    if request.method == 'POST' and 'video' in request.files:
        video_title = request.form.get('title')
        uploaded_video = request.files['video']

        # Original uploaded file name to be saved to database.
        original_filename = uploaded_video.filename

        # Give it a new unique file name.
        file_extension = original_filename.split('.')[-1]
        uploaded_video.filename = f'{uuid4()}.{file_extension}'

        try:
            filename = videos.save(uploaded_video)

            video = Video(title=video_title, filename=filename, original_filename=original_filename)
            user.videos.append(video)
            db.session.add(user)
            db.session.commit()

            flash('Video uploaded successfully', 'card-panel green lighten-4')
        except UploadNotAllowed:
            flash(f'Video upload failed. Only {allowed_uploads} file extensions allowed.', 'card-panel red lighten-4')

    # Sort videos by upload date and time with latest videos at the front.
    user.videos = sorted(user.videos, key=lambda x: x.upload_datetime, reverse=True)

    for video in user.videos:
        print(video.upload_datetime)

    return render_template('main/video_dashboard/index.html', user=user, allowed_uploads=allowed_uploads)


@main_routes.route('/videos/<int:video_id>')
def video_page(video_id):
    video = get_video(video_id)
    user = get_user()

    return render_template('main/video/index.html', video=video, user=user)
