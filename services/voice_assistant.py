
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QPushButton
import speech_recognition as sr
import pyttsx3
import requests
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThread, pyqtSignal
from datetime import datetime


current_time = datetime.now().strftime("%H:%M")

QA_pairs = {
    "привет": "Привет! Чем могу помочь?",
    "как дела": "Спасибо, что спросили. У меня всё отлично!",
    "что ты можешь делать": "Я могу отвечать на вопросы, рассказывать о погоде, выполнять поиск в интернете и многое другое.",
    "как тебя зовут": "Меня зовут Аиша, я ваш голосовой ассистент.",
    "спасибо": "Пожалуйста! Если у вас ещё что-то появится, обращайтесь.",
    "пока": "До свидания! Хорошего дня!",
    "сколько времени": f"Сейчас я могу сказать только текущее время: {current_time}",
    "сколько сейчас время":f"Сейчас я могу сказать только текущее время: {current_time}",
    "который час":f"Сейчас я могу сказать только текущее время: {current_time}",
    "который час сейчас":f"Сейчас я могу сказать только текущее время: {current_time}",
    "сейчас который час":f"Сейчас я могу сказать только текущее время: {current_time}",
    "сейчас какое время":f"Сейчас я могу сказать только текущее время: {current_time}",
    "подскажи время":f"Сейчас я могу сказать только текущее время: {current_time}",
    "подскажи пожалуйста время":f"Сейчас я могу сказать только текущее время: {current_time}",
    "подскажи время пожалуйста":f"Сейчас я могу сказать только текущее время: {current_time}",
    "расскажи анекдот": "Конечно! Вот один анекдот: Кто рано встаёт, тому сон мешает, а кто поздно ложится, тому жизнь.",
    "открой Google": "К сожалению, я не могу открывать внешние приложения. Но я могу выполнить поиск для вас прямо здесь!",
    "какой смысл жизни": "Это философский вопрос, на который каждый человек может найти свой ответ.",
    "как проехать в центр города": "Для получения информации о маршрутах и общественном транспорте рекомендую воспользоваться приложением Гугл Карты.",
    "какая столица Франции": "Столица Франции - Париж.",
    "кто такой Эйнштейн": "Эйнштейн был известным физиком, создателем теории относительности.",
    "что такое ИИ": "ИИ - искусственный интеллект, область информатики, изучающая создание интеллектуальных агентов.",
    "продолжи фразу Кто в лес кто по дрова": "Кто в лес, кто по дрова, а кто идёт в гости - все к маме дороги!",
    "Что такое световой год": "Световой год - это расстояние, которое свет проходит за один земной год.",
    "Какие годы длились Великая Отечественная война": "Великая Отечественная война продолжалась с 1941 по 1945 год.",
    "Какой столицей Франции является Париж": "Столицей Франции является город Париж.",
    "Кто написал роман Преступление и наказание": "Роман 'Преступление и наказание' был написан Фёдором Достоевским.",
    "Сколько планет в Солнечной системе": "В Солнечной системе 8 планет.",
    "Как называется самая высокая гора в мире": "Самая высокая гора в мире - это Эверест.",
    "Какого цвета небо": "Небо обычно синего цвета из-за рассеяния света в атмосфере Земли.",
    "какие виды животных существуют": "Существует огромное количество видов животных, включая млекопитающих, птиц, рыб, насекомых, амфибий и рептилий.",
    "какие виды спорта считаются экстремальными": "Экстремальные виды спорта включают бейсджампинг, скейтбординг, паркур, сноубординг, скалолазание и многое другое.",
    "что такое медитация": "Медитация - это практика сосредоточения ума, которая способствует улучшению психического и физического здоровья.",
    "какие виды технологий существуют": "Существует множество видов технологий, включая информационные технологии, медицинскую технику, транспортные технологии, сельское хозяйство и многое другое.",
    "какие языки программирования наиболее популярны": "Среди наиболее популярных языков программирования сегодня можно выделить Python, JavaScript, Java, C++, C# и PHP.",
    "какие книги считаются классикой мировой литературы": "Среди классических произведений мировой литературы можно выделить такие работы, как \"Война и мир\" Льва Толстого, \"Преступление и наказание\" Федора Достоевского, \"Гамлет\" Уильяма Шекспира и многие другие.",
    "что такое экология": "Экология - это наука о взаимодействии организмов между собой и с окружающей средой.",
    "какие виды религий существуют": "Существует множество религий, включая христианство, ислам, буддизм, индуизм, джайнизм, сикхизм и многие другие.",
    "какие виды медитации существуют": "Существует множество видов медитации, включая зен, випассану, трансцендентальную медитацию, йогу и многое другое.",
    "какие технологии будущего ожидаются": "Технологии будущего включают искусственный интеллект, квантовые вычисления, биотехнологии, нанотехнологии и многое другое.",
    "какие приложения пользуются наибольшей популярностью сегодня": "Среди наиболее популярных приложений сегодня можно выделить Instagram, Facebook, WhatsApp, TikTok, YouTube и многие другие.",
    "какие виды искусства существуют": "Существует множество видов искусства, включая живопись, скульптуру, музыку, театр, кино, литературу и многое другое.",
    "какие виды фильмов существуют": "Существует множество жанров фильмов, включая драму, комедию, экшн, ужасы, научную фантастику",
    "что такое робототехника": "Робототехника - это область инженерии и науки, занимающаяся созданием и управлением роботами.",
    "какие виды роботов существуют": "Существует много видов роботов, включая промышленные роботы, роботы-манипуляторы, роботы-пылесосы, дроны и многое другое.",
    "какие профессии будут востребованы в будущем": "В будущем будут востребованы профессии в сфере информационных технологий, зеленой энергетики, здравоохранения, кибербезопасности и других смежных областях.",
    "какие технологии будут преобладать в будущем": "В будущем будут преобладать технологии искусственного интеллекта, интернета вещей, блокчейна, биотехнологий и другие.",
    "что такое криптовалюта": "Криптовалюта - это децентрализованная цифровая валюта, использующая криптографию для обеспечения безопасности транзакций и контроля создания новых единиц.",
    "какие преимущества и недостатки у криптовалюты": "Преимущества криптовалюты включают быстрые и дешевые транзакции, анонимность и децентрализацию. Недостатки включают высокую волатильность, неполную защиту прав потребителей и возможные угрозы безопасности.",
    "какие технологии помогают в борьбе с изменением климата": "Технологии борьбы с изменением климата включают в себя возобновляемые источники энергии, энергоэффективные технологии, карбоновые улавливающие и хранящие технологии и другие.",
    "что такое блокчейн": "Блокчейн - это децентрализованная база данных, используемая для хранения информации о транзакциях, обеспечивающая прозрачность, безопасность и невозможность подделки данных.",
    "какие языки программирования самые востребованные": "Самые востребованные языки программирования включают Python, JavaScript, Java, C++, C# и другие, в зависимости от области применения и потребностей проекта.",
    "какие новые технологии ожидаются в ближайшие годы": "В ближайшие годы ожидаются развитие искусственного интеллекта, квантовых вычислений, биотехнологий, генной редакции, виртуальной и дополненной реальности и другие.",
    "что такое электронная коммерция": "Электронная коммерция - это процесс покупки и продажи товаров и услуг через интернет, включая онлайн-магазины, аукционы",
    "какие виды музыкальных жанров существуют": "Существует множество музыкальных жанров, включая поп-музыку, рок, джаз, классическую музыку, хип-хоп, электронную музыку, регги, кантри и многое другое.",
    "какие виды спортивных игр существуют": "Существует множество видов спортивных игр, включая футбол, баскетбол, теннис, волейбол, гольф, бейсбол, хоккей, гандбол и многое другое.",
    "какие виды транспорта существуют": "Существует множество видов транспорта, включая автомобили, автобусы, мотоциклы, велосипеды, поезда, самолеты, корабли, космические корабли и многое другое.",
    "какие виды домашних животных существуют": "Существует множество видов домашних животных, включая собак, кошек, птиц, рыб, грызунов, рептилий и многое другое.",
    "какие виды профессий существуют": "Существует множество видов профессий, включая врачей, учителей, инженеров, художников, писателей, музыкантов, адвокатов, банкиров и многое другое.",
    "какие виды кухонь существуют": "Существует множество видов кухонь, включая итальянскую, французскую, китайскую, японскую, индийскую, мексиканскую, тайскую, средиземноморскую и многое другое.",
    "какие виды образования существуют": "Существует множество видов образования, включая начальное, среднее, высшее образование, дистанционное обучение, профессиональное образование, вечерние школы и многое другое.",
    "какие виды заболеваний существуют": "Существует множество видов заболеваний, включая инфекционные, вирусные, бактериальные, онкологические, сердечно-сосудистые, психические и многое другое.",
    "какие виды валют существуют": "Существует множество видов валют, включая доллары, евро, фунты стерлингов, иены, юани, рубли, реалы, рупии и многое другое.",
    "какие виды религиозных праздников существуют": "Существует множество видов религиозных праздников, включая Рождество, Пасху, Курбан-байрам, Рамадан, Дивали, Хануку и многое другое.",
    "какие виды общественных организаций существуют": "Существует множество видов общественных организаций, включая благотворительные фонды, волонтерские организации, общественные ассоциации, профсоюзы и многое другое.",
    "какие виды наук существуют": "Существует множество научных дисциплин, включая физику, химию, биологию, математику, астрономию, историю, экономику, социологию и многое другое.",
    "какие виды танцев существуют": "Существует множество видов танцев, включая классический балет, хип-хоп, сальсу, танго, фламенко, брейк-данс, тверк и многое другое.",
    "какие виды экологических проблем существуют": "Существует множество экологических проблем, включая загрязнение воздуха, воды и почвы, вымирание видов, изменение климата, вырубка лесов и многое другое.",
    "какие виды медицинских специальностей существуют": "Существует множество медицинских специальностей, включая терапию, хирургию, анестезиологию, гинекологию, педиатрию, психиатрию, неврологию и многое другое.",
    "какие виды событий существуют": "Существует множество видов событий, включая концерты, выставки, фестивали, конференции, свадьбы, дни рождения, спортивные мероприятия и многое другое.",
    "какие виды социальных сетей существуют": "Существует множество видов социальных сетей, включая Facebook, Instagram, Twitter, LinkedIn, TikTok, Snapchat, Pinterest и многое другое.",
    "какие виды философских направлений существуют": "Существует множество философских направлений, включая метафизику, этику, эпистемологию, онтологию, логику, философию искусства, философию религии и многое другое.",
    "какие виды культурных традиций существуют": "Существует множество культурных традиций, включая обычаи, ритуалы, праздники, кулинарные привычки, народные ремесла, музыкальные стили и многое другое.",
    "какие виды образовательных учреждений существуют": "Существует множество образовательных учреждений, включая школы, колледжи, университеты, академии, институты, курсы дополнительного образования и многое другое.",
    "какие виды кинофильмов существуют": "Существует множество жанров кинофильмов, включая драму, комедию, фэнтези, документальное кино, мультфильмы, мюзиклы, исторические фильмы и многое другое.",
    "какие виды исторических эпох существуют": "Существует множество исторических эпох, включая каменный век, бронзовый век, железный век, древний мир, средневековье, новое время, эпоху Возрождения и многое другое.",
    "какие виды исследований существуют": "Существует множество видов исследований, включая фундаментальные и прикладные исследования, экспериментальные, наблюдательные, теоретические, психологические, социологические и многое другое."
}


class VoiceAssistant:
    """
    Настройки голосового ассистента, включающие имя, пол, язык речи
    """
    name = ""
    sex = ""
    speech_language = ""
    recognition_language = ""

class BackgroundTask(QThread):
    recognitionFinished = pyqtSignal(str)

    def __init__(self, assistant_window):
        super().__init__()
        self.assistant_window = assistant_window

    def run(self):
        recognized_text = self.assistant_window.recognize_speech()
        self.recognitionFinished.emit(recognized_text)

class AssistantWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Голосовой Ассистент")
        self.setGeometry(100, 100, 600, 400)

        authenticator = IAMAuthenticator('l30vv0V3WIq_F1pAKSUiHy0lZT6YqzyzDLqKoxR5BFYv')
        self.assistant = AssistantV2(
            version='2019-02-28',
            authenticator=authenticator
        )
        self.assistant.set_service_url('https://api.au-syd.assistant.watson.cloud.ibm.com/instances/9d6194d3-8619-4423-8180-6b1ed8ef98d1')
        self.assistant_id = '39f97f56-5d2e-4f70-84c7-36b86a8986b0'

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.text_area = QTextEdit()
        self.text_area.setFont(QFont("Arial", 12))
        layout.addWidget(self.text_area)

        self.microphone_button = QPushButton("Активировать микрофон")
        self.microphone_button.setFont(QFont("Arial", 14))
        self.microphone_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px;")
        self.microphone_button.clicked.connect(self.start_recognition)
        layout.addWidget(self.microphone_button)

        
        self.close_button = QPushButton("Закрыть")
        self.close_button.setFont(QFont("Arial", 14))
        self.close_button.setStyleSheet("background-color: #f44336; color: white; border-radius: 10px;")
        self.close_button.clicked.connect(self.close_application)
        layout.addWidget(self.close_button)

    def setup_assistant_voice(self):
        """
        Установка голоса по умолчанию
        """
        voices = ttsEngine.getProperty("voices")

        if assistant.speech_language == "en":
            assistant.recognition_language = "en-US"
            if assistant.sex == "female":
                ttsEngine.setProperty("voice", voices[1].id)
            else:
                ttsEngine.setProperty("voice", voices[2].id)
        else:
            assistant.recognition_language = "ru-RU"
            ttsEngine.setProperty("voice", voices[0].id)

    def speak_text(self, text):
        engine = pyttsx3.init()

        voices = engine.getProperty('voices')
        for voice in voices:
            if "ru" in voice.languages and "female" in voice.name.lower() and "good" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break

        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        engine.setProperty('pitch', 50)  

    
        engine.say(text)
        engine.runAndWait()



    def get_weather(self, city):
        self.api_key = '70a71ba09a677e5b50cfc658fdc1a36b'  
        self.url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric'
        self.response = requests.get(self.url)
        data = self.response.json()
        if 'weather' in data:
            self.weather_description = data['weather'][0]['description']
            self.temperature = data['main']['temp']
            return f"Погода в городе {city}: {self.weather_description}. Температура: {self.temperature} градусов Цельсия"
        else:
            return "Ошибка получения погоды. Проверьте название города и подключение к интернету."

    def search_google(self, query):
        self.api_key = 'AIzaSyAt7P-20NqH5fhpYXgVVOWexpqlDTzSXqY' 
        self.cx = '25d23c93146dd41d1' 

        self.url = f'https://www.googleapis.com/customsearch/v1?q={query}&key={self.api_key}&cx={self.cx}'

        try:
            self.response = requests.get(self.url)
            self.data = self.response.json()
            
            self.search_results = self.data['items']
            
            if self.search_results:
                self.first_result = self.search_results[0]
                self.title = self.first_result['title']
                self.link = self.first_result['link']
                self.snippet = self.first_result['snippet']
                return f"Вот что я нашел: {self.title}. {self.snippet}."
            else:
                return "Извините, ничего не найдено."

        except Exception as e:
            print("Ошибка при выполнении запроса к Google:", e)
            return "Произошла ошибка при выполнении запроса к Google."
        
    def recognize_city(self):
        self.recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.text_area.append("Какой город?")
            audio = self.recognizer.listen(source)
        try:
            self.text_area.append("Вы сказали: " + self.recognizer.recognize_google(audio, language='ru-RU'))
            return self.recognizer.recognize_google(audio, language='ru-RU')
        except sr.UnknownValueError:
            self.text_area.append("Извините, не удалось распознать речь")
        except sr.RequestError:
            self.text_area.append("Извините, сервис распознавания речи недоступен")
    

    def recognize_speech(self):
        self.recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.text_area.append("Говорите что-нибудь:")
            audio = self.recognizer.listen(source)

        try:
            self.text_area.append("Вы сказали: " + self.recognizer.recognize_google(audio, language='ru-RU'))
            return self.recognizer.recognize_google(audio, language='ru-RU')
        except sr.UnknownValueError:
            self.text_area.append("Извините, не удалось распознать речь")
        except sr.RequestError:
            self.text_area.append("Извините, сервис распознавания речи недоступен")

    def start_recognition(self):
        self.background_task = BackgroundTask(self)
        self.background_task.recognitionFinished.connect(self.process_recognized_text)
        self.background_task.start()
    
    def process_recognized_text(self, text):
   
        self.text_area.append(text)

       
        if "погода" in text.lower():
            city = self.recognize_city()
            weather_info = self.get_weather(city)
            self.text_area.append(weather_info)
            self.speak_text(weather_info) 

        if "поиск" in text.lower():
            query = text.lower().replace("поиск", "").strip() 
            search_result = self.search_google(query)
            self.text_area.append(search_result)
            self.speak_text(search_result)  
        
        for key in QA_pairs.keys():
            if text.lower() == key.lower():
                self.text_area.append(QA_pairs.get(key))
                self.speak_text(QA_pairs.get(key))




    
    def send_user_input(self):
        user_input = self.text_edit.text()
        self.text_edit.clear()
        response = self.get_watson_assistant_response(user_input)
        self.text_area.append(f"Пользователь: {user_input}\nАссистент: {response}\n")

    def close_application(self):
        sys.exit()



if __name__ == "__main__":
    
    ttsEngine = pyttsx3.init()

   
    assistant = VoiceAssistant()
    assistant.name = "Alice"
    assistant.sex = "female"
    assistant.speech_language = "ru"

    app = QApplication(sys.argv)
    window = AssistantWindow()
    window.setup_assistant_voice()
    window.show()
    sys.exit(app.exec_())