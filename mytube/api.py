from flask import session, make_response, request, jsonify
from flask_restful import Resource

from mytube.views.utils import get_video, get_user
from mytube.models import VideoComment, db


def get_video_comments(video_id):
    video = get_video(video_id)

    # Sort comments with latest at the front of the list.
    video.comments = sorted(video.comments, key=lambda x: x.created_at, reverse=True)

    comments = []

    for comment in video.comments:
        document = {
            'id': comment.id,
            'value': comment.value,
            'created_at': comment.created_at,
            'user': {
                'id': comment.user.id,
                'given_name': comment.user.given_name,
                'family_name': comment.user.family_name,
                'picture_url': comment.user.picture_url
            }
        }
        comments.append(document)

    return comments


class Comment(Resource):
    def get(self, video_id):
        comments = get_video_comments(video_id)

        return make_response(jsonify(comments))

    def post(self):
        if 'profile' in session:
            body = request.get_json()

            user = get_user()
            comment = VideoComment(value=body['comment'], video_id=body['video_id'], user_id=user.id)
            db.session.add(comment)
            db.session.commit()

            # Return the new set of comments.
            comments = get_video_comments(body['video_id'])
            return make_response(jsonify(comments), 201)
        return make_response({'error': 'not authenticated'}, 403)
