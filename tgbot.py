from threading import Thread
from datetime import datetime
from flask import Flask
from telebot import TeleBot
from models import db, Telegram
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sadsad-dfs-dsafdsa-**asd+-'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aisha_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

bot = TeleBot('6386690858:AAHC2IT-wPsZzsMjwjXZzB7WVj_ZpG9ggjU')

def get_news():
    api_key = '5f9f6bda686f44deb23dc37120b121ca'
    url = f'https://newsapi.org/v2/top-headlines?country=ru&apiKey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])
        if articles:
            news = []
            for article in articles[:5]:  
                title = article.get('title', '')
                description = article.get('description', '')
                news.append(f'{title}\n{description}\n')
            return '\n'.join(news)
        else:
            return 'Не удалось получить новости'
    else:
        return 'Ошибка при запросе к API новостей'



@bot.message_handler(commands=['start'])
def start(message):
    time_=datetime.now()
    bot.send_message(message.chat.id,
    f'''Привет, {message.from_user.first_name},
Меня зовут Аиша, я голосовой ассистент
/help - получить список доступных команд   ''')
    user = Telegram(chat_id=message.from_user.id, name=message.from_user.first_name, 
                    datetime=time_)
    with app.app_context():
        db.session.add(user)
        db.session.commit()

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id,
    '''Доступные команды:
/start - начать взаимодействие с ботом
/info - получить информацию о пользователе
/reminder - установить напоминание
/weather - получить текущую погоду
/news - получить последние новости''')

from models import db, Telegram  

@bot.message_handler(commands=['info'])
def info_command(message):
    user_info = Telegram.query.filter_by(chat_id=message.from_user.id).first()
    if user_info:
        info_text = f'Имя: {user_info.name}\nID: {user_info.chat_id}\nДата регистрации: {user_info.datetime}'
        bot.send_message(message.chat.id, info_text)
    else:
        bot.send_message(message.chat.id, 'Информация о пользователе не найдена')


@bot.message_handler(commands=['reminder'])
def reminder_command(message):
    bot.send_message(message.chat.id, 'Для установки напоминания введите дату и время в формате ГГГГ-ММ-ДД ЧЧ:ММ')

@bot.message_handler(func=lambda message: message.text.startswith('20') and len(message.text) == 16)
def set_reminder(message):
    try:
        reminder_time = datetime.strptime(message.text, '%Y-%m-%d %H:%M')
        bot.send_message(message.chat.id, f'Напоминание установлено на {reminder_time}')
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат даты и времени. Попробуйте снова.')

@bot.message_handler(commands=['weather'])
def weather_command(message):
    city = message.text.split('/weather', 1)[1].strip() if len(message.text.split()) > 1 else None
    
    if city:
        api_key = '70a71ba09a677e5b50cfc658fdc1a36b'  
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if 'weather' in data:
                weather_description = data['weather'][0]['description']
                temperature = data['main']['temp']
                bot.send_message(message.chat.id, f"Погода в городе {city}: {weather_description}. Температура: {temperature} градусов Цельсия")
            else:
                bot.send_message(message.chat.id, "Ошибка получения данных о погоде")
        else:
            bot.send_message(message.chat.id, "Ошибка при запросе к API погоды")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, укажите название города после команды /weather")


@bot.message_handler(commands=['news'])
def news_command(message):
    news = get_news()
    bot.send_message(message.chat.id, news)

def run_bot():
    bot.infinity_polling()

bot_thread = Thread(target=run_bot)

if __name__ == '__main__':
    bot_thread.start()
