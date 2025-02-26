from flask import Flask, request, render_template_string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import logging

# Загрузка переменных окружения
load_dotenv()

app = Flask(__name__)

# Получение переменных из .env
EMAIL_USER = os.getenv("EMAIL_USER")  # Ваш email на Яндексе (например, example@yandex.ru)
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Пароль или прикладной пароль
TO_EMAIL = os.getenv("TO_EMAIL")  # Email, куда будут отправляться сообщения

# Логирование ошибок
logging.basicConfig(filename='app.log', level=logging.DEBUG)

html_template = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Репетитор по химии | Шакирова Ирина Хабировна</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>
    <!-- Раскрывающееся меню -->
    <header>
        <nav>
            <!-- <div class="logo">
                <img src="logo.png" alt="Логотип" style="width: 50px;">
            </div> -->
            <button id="menu-toggle" onclick="toggleMenu()">☰</button>
            <ul class="nav-links" id="nav-menu">
                <li><a href="index.html">Главная</a></li>
                <li><a href="about.html">Обо мне</a></li>
                <li><a href="services.html">Услуги</a></li>
                <li><a href="resources.html">Ресурсы</a></li>
                <li><a href="contact.html">Контакты</a></li>
            </ul>
        </nav>
    </header>

    <!-- Основной контент -->
    <main>
        <section id="hero">
            <h1>Постижение химии: личный подход к каждому ученику</h1>
            <p>Репетитор по химии с опытом работы учителем 3 года</p>
            <button onclick="window.location.href='contact.html'">Записаться на урок</button>
        </section>
        
        <!-- Галерея фото -->
        <!-- <section id="gallery">
            <h2>Галерея</h2>
            <div class="photo-grid">
                <img src="https://images.unsplash.com/photo-1551632647-fef2f79d4bb3?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1974&q=80" alt="Лаборатория">
                <img src="https://images.unsplash.com/photo-1518791841217-8f162f1e1131?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1950&q=80" alt="Молекулы">
                <img src="https://images.unsplash.com/photo-1526336024174-e58f5cdd8e1b?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1950&q=80" alt="Периодическая таблица">
            </div>
        </section> -->

        <!-- Цитаты -->
        <section id="quotes">
            <h2>Химия — это когда просто два атома встретились,<br> понравились друг другу и создали молекулу!</h2>
            <blockquote>
                <i>"Наука — это не только знание, но и постоянный поиск."</i>
                <footer>— Мария Кюри</footer>
            </blockquote>
            <blockquote>
                <i>"Всякий раз, когда я делаю что-то новое, я чувствую себя ребенком, играющим в лаборатории."</i>
                <footer>— Даниэль Шехтман</footer>
            </blockquote>
        </section>
    </main>

    <footer>
        <p>&copy; 2025 Репетитор по химии | Шакирова Ирина Хабировна</p>
    </footer>

    <script src="script.js"></script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_template)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if not name or not email:
        return "Ошибка: пожалуйста, заполните все обязательные поля."

    try:
        send_email(name, email, message)
        return "Сообщение успешно отправлено!"
    except Exception as e:
        logging.error(f"Ошибка отправки письма: {str(e)}")
        return f"Ошибка отправки сообщения: {str(e)}"

def send_email(name, email, message):
    msg = MIMEMultipart()
    msg['From'] = f"Репетитор по химии <{EMAIL_USER}>"
    msg['To'] = TO_EMAIL
    msg['Subject'] = "Новое сообщение с сайта репетитора"
    msg['Reply-To'] = email  # Указываем email отправителя для ответа

    body = f"""
    Вы получили новое сообщение от {name} ({email}):\n
    {message}
    """

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Используем SSL (порт 465)
        with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as server:
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, TO_EMAIL, msg.as_string())
    except Exception as e:
        logging.error(f"Ошибка отправки письма через SSL: {str(e)}")
        raise

if __name__ == '__main__':
    app.run(debug=True)