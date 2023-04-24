import flask
from flask import jsonify, request
from . import db_session
from .news import News


blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/news/<int:news_id>', methods=['GET'])
def get_one_job(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).get(news_id)
    if not news:
        return jsonify({'error': 'Not found'})
    return jsonify({
        'news': news.to_dict(only=('id', 'about'))
    })
