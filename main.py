import datetime

from flask import (
    Flask,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
)
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
    mixins,
)
from data import db_session
from data.models import *

from forms.login import LoginForm
from forms.register import RegisterForm
from forms.add_text import TextForm
import translators as ts
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = "yandexlyceum_secret_key"
login_manager = LoginManager()
login_manager.init_app(app)


@app.context_processor
def utility_processor():
    def translate_tat_to_rus(word):
        word = str(word)
        return ts.google(word, from_language='tt', to_language='ru')

    return dict(translate_tat_to_rus=translate_tat_to_rus)


def translate_js(word):
    word = str(word)
    return ts.google(word, from_language='tt', to_language='ru')


@app.route("/get_translate", methods=["POST"])
def get_translate():
    text = json.loads(request.data)["text"]
    print(text)
    # select_text = request.form.get("selectText")
    # return jsonify({"translateText": translate_test(select_text)})
    return json.dumps({"translate": translate_js(text)})


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    """Получение текущего пользователся"""
    db_sess = db_session.create_session()
    return db_sess.query(Users).get(user_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Users).filter(Users.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', message='Неправильный логин или пароль', form=form)
    return render_template('login.html', form=form, title='Авторизация')


@app.route("/register", methods=["GET", "POST"])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Пароли не совпадают",
            )
        db_sess = db_session.create_session()
        if db_sess.query(Users).filter(Users.email == form.email.data).first():
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Такой пользователь уже есть",
            )
        user = Users()
        user.login = form.login.data
        user.email = form.email.data
        user.tg_username = form.tg_username.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect("/login")
    return render_template("register.html", title="Регистрация", form=form)


@app.route("/profile")
@login_required
def profile():
    created_time = datetime.datetime(year=current_user.creation_date.year,
                                     month=current_user.creation_date.month,
                                     days=current_user.creation_date.days)
    print(created_time, type(created_time))
    using_time = str(datetime.datetime.now() - created_time)
    print(using_time)
    # using_time = using_time[:-3] + "ч " + using_time[-2:] + "мин"
    try:
        word_count = len(current_user.words.split(","))
    except:
        word_count = 0
    items_list = [
        ["Имя", current_user.login],
        ["Почта", current_user.email],
        [
            "Телеграм",
            current_user.tg_username
            if current_user.tg_username is not None
            else "Не указан",
        ],
        ["Дата создания", str(created_time)],
        ["Время использования", using_time],
        ["Кол-во слов", word_count],
    ]
    return render_template("profile.html", items_list=items_list)


@app.route("/book_view")
@login_required
def book_view():
    return render_template("book_view.html")


def main():
    db_session.global_init(user_name='postgres', user_password='123', host='localhost', port='5432',
                           db_name='tatlib_db')
    app.run(port=8080, host="127.0.0.1")


if __name__ == "__main__":
    main()
