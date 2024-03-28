from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime
from tgbot import bot_thread
from models import db


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sadsad-dfs-dsafdsa-**asd+-'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aisha_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

from models import Users, Profiles, Reviews
from tgbot import bot

@app.route('/')
def index():
    return render_template('index.html', title='Главная')

@app.route('/about')
def about():
    return render_template('about.html', title='О нас')

@app.route('/telegram')
def telegram():
    return render_template('telegram.html', title='Телеграм Бот')


@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    reviews = Reviews.query.all()
    if request.method == 'POST':
        title = request.form["name"]
        content = request.form["content"]

        review = Reviews(title=title, content=content)
        try:
            db.session.add(review)
            db.session.commit()
            flash('Успешно отправлено')
            return redirect('/reviews')
        except Exception as e:
            flash('Произошла ошибка при отправке')
            return redirect('/reviews')
    else:
        return render_template('reviews.html', title='Отзывы и пожелания', reviews = reviews)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            hash = generate_password_hash(request.form['password'])
            user = Users(email=request.form['email'], password=hash)
            db.session.add(user)
            db.session.flush()

            profile = Profiles(name=request.form['name'], age=request.form['age'],
                         city=request.form['city'], user_id=user.id)
            db.session.add(profile)
            db.session.commit()
            flash('Регистрация прошла успешно')
        except Exception as e:
            db.session.rollback()
            print('Ошибка при отправлении данных в БД:', str(e))
    return render_template('register.html', title='Регистрация')

@app.route('/download')
def download():
    return render_template('download.html', title='Скачивания')

@app.errorhandler(404)
def page_not_found():
    return render_template('')

if __name__ == '__main__':
    bot_thread.start()
    app.run(debug=True)
