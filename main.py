from flask import Flask, redirect, url_for, render_template, request, abort, make_response, jsonify
from werkzeug.utils import secure_filename
from data import db_session, news_api
from data.users import User
from data.news import News
from data.imgs import Img
from data.messages import Message
from forms.user import RegisterForm
from forms.login import LoginForm
from forms.news import NewsForm
from forms.profile import Profile
from forms.friend import FriendForm
from forms.message import MessageForm
from flask_login import LoginManager, current_user, login_user, logout_user, login_required


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).filter(User.id == user_id).first()


def main():
    db_session.global_init('db/project.db')
    app.register_blueprint(news_api.blueprint)
    app.run(port=8080, host='127.0.0.1')


@app.route('/')
@app.route('/news')
def list_of_news():
    db_sess = db_session.create_session()
    news = db_sess.query(News).all()
    base_foto = url_for('static', filename='img/profile_foto.jpg')
    return render_template('list_of_news.html', link_css=url_for('static', filename='css/style_news.css'),
                           title='Новости', news=news, link_css_base=url_for('static', filename='css/style_base.css'),
                           base_foto=base_foto)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template('register.html', title='Регистрация', message='Пароли не совпадают',
                                   link_css=url_for('static', filename='css/style_register_form.css'), form=form,
                                   link_css_base=url_for('static', filename='css/style_base.css'))
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   message='Пользователь с данной почтой уже есть',
                                   link_css=url_for('static', filename='css/style_register_form.css'), form=form,
                                   link_css_base=url_for('static', filename='css/style_base.css'))

        if db_sess.query(User).filter(User.alias == form.alias.data).first():
            return render_template('register.html', title='Регистрация',
                                   message='Пользователь с данным псевдонимом уже есть',
                                   link_css=url_for('static', filename='css/style_register_form.css'), form=form,
                                   link_css_base=url_for('static', filename='css/style_base.css'))

        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            city=form.city.data,
            email=form.email.data,
            sex=form.sex.data,
            alias=form.alias.data
        )
        user.set_password(form.password.data)
        if form.foto.data:
            file = request.files['foto'].read()
            if not db_sess.query(Img).filter(Img.img == file).first():
                img = Img()
                img.name = secure_filename(request.files['foto'].filename)
                img.minetype = request.files['foto'].mimetype
                img.img = file
                db_sess.add(img)
                db_sess.commit()
            user.foto = db_sess.query(Img).filter(Img.img == file).first().id
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация',
                           link_css=url_for('static', filename='css/style_register_form.css'), form=form,
                           link_css_base=url_for('static', filename='css/style_base.css'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/news')
        return render_template('login.html', title='Авторизация', message='Неправильный логин или пароль',
                               link_css=url_for('static', filename='css/style_login_form.css'), form=form,
                               link_css_base=url_for('static', filename='css/style_base.css'))
    return render_template('login.html', title='Авторизация',
                           link_css=url_for('static', filename='css/style_login_form.css'), form=form,
                           link_css_base=url_for('static', filename='css/style_base.css'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/add_news', methods=['POST', 'GET'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if form.img.data:
            file = request.files['img'].read()
            if not db_sess.query(Img).filter(Img.img == file).first():
                img = Img()
                img.name = secure_filename(request.files['img'].filename)
                img.minetype = request.files['img'].mimetype
                img.img = file
                db_sess.add(img)
                db_sess.commit()
        news = News()
        news.user_id = current_user.id
        news.about = form.about.data
        news.is_private = form.is_private.data
        if form.img.data:
            news.img_id = db_sess.query(Img).filter(Img.img == file).first().id
        db_sess.add(news)
        db_sess.commit()
        return redirect('/news')
    return render_template('news.html', link_css=url_for('static', filename='css/style_news_form.css'),
                           title='Добавление новости', form=form,
                           link_css_base=url_for('static', filename='css/style_base.css'))


@app.route('/get_image/<int:img_id>')
def get_image(img_id):
    db_sess = db_session.create_session()
    img = db_sess.query(Img).filter(Img.id == img_id).first()
    if img:
        h = make_response(img.img)
        h.headers['Content-Type'] = img.minetype
        return h


@app.route('/profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    form = Profile()
    foto = None
    standard = True
    if request.method == 'GET':
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == user_id).first()
        if user:
            form.surname.data = user.surname
            form.name.data = user.name
            form.age.data = user.age
            form.sex.data = user.sex
            form.city.data = user.city
            if user.foto != 0:
                foto = user.foto
                standard = False
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == user_id).first()
        if user:
            user.surname = form.surname.data
            user.name = form.name.data
            user.age = form.age.data
            user.sex = form.sex.data
            user.city = form.city.data
            if form.foto.data:
                file = request.files['foto'].read()
                if not db_sess.query(Img).filter(Img.img == file).first():
                    img = Img()
                    img.name = secure_filename(request.files['foto'].filename)
                    img.minetype = request.files['foto'].mimetype
                    img.img = file
                    db_sess.add(img)
                    db_sess.commit()
                user.foto = db_sess.query(Img).filter(Img.img == file).first().id
            db_sess.commit()
            return redirect('/news')
        else:
            abort(404)
    base_foto = url_for('static', filename='img/profile_foto.jpg')
    return render_template('profile.html', title='Профиль',
                           link_css=url_for('static', filename='css/style_profile.css'), form=form,
                           foto=foto, standard=standard, base_foto=base_foto,
                           link_css_base=url_for('static', filename='css/style_base.css'))


@app.route('/chat/<int:user_id>/<int:second_user_id>', methods=['POST', 'GET'])
@login_required
def chat(user_id, second_user_id):
    db_sess = db_session.create_session()
    user_now = db_sess.query(User).filter(User.id == user_id).first()
    users = []
    messages = []
    for message in db_sess.query(Message).filter(Message.second_user_id == second_user_id,
                                                 Message.first_user_id == user_id):
        messages.append(message)
    for message in db_sess.query(Message).filter(Message.second_user_id == user_id,
                                                 Message.first_user_id == second_user_id):
        messages.append(message)
    messages = sorted(messages, key=lambda x: x.created_time)
    base_foto = url_for('static', filename='img/profile_foto.jpg')
    if user_now:
        for friend_id in user_now.friends.split():
            friend = db_sess.query(User).filter(User.id == friend_id).first()
            if friend:
                users.append(friend)
    else:
        abort(404)
    form_message = MessageForm()
    if form_message.validate_on_submit():
        if second_user_id != 0:
            new_message = Message()
            new_message.text = form_message.text.data
            new_message.first_user_id = user_id
            new_message.second_user_id = second_user_id
            db_sess.add(new_message)
            db_sess.commit()
        return redirect('/chat/' + str(user_id) + '/' + str(second_user_id))
    form_friend = FriendForm()
    if form_friend.validate_on_submit():
        user_friend = db_sess.query(User).filter(User.alias == form_friend.alias.data).first()
        if not user_friend:
            return render_template('chat_base.html', users=users, form_friend=form_friend, base_foto=base_foto,
                                   link_css=url_for('static', filename='css/style_chat_base.css'),
                                   form_message=form_message, title='Чат',
                                   link_css_base=url_for('static', filename='css/style_base.css'),
                                   message='Пользователя с таким псевдонимом не существует', messages=messages)
        if str(user_friend.id) not in current_user.friends.split():
            current_user.friends += ' ' + str(user_friend.id)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/chat/' + str(user_id) + '/' + str(second_user_id))
    return render_template('chat_base.html', users=users, form_friend=form_friend, base_foto=base_foto, title='Чат',
                           link_css=url_for('static', filename='css/style_chat_base.css'), form_message=form_message,
                           link_css_base=url_for('static', filename='css/style_base.css'), messages=messages)


if __name__ == '__main__':
    main()