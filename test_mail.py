from flask_mail import Mail, Message
from flask import Flask
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['MAIL_SERVER'] = os.environ.get("MAIL_SERVER")
app.config['MAIL_PORT'] = int(os.environ.get("MAIL_PORT", 465))
app.config['MAIL_USE_SSL'] = os.environ.get("MAIL_USE_SSL") == "True"
app.config['MAIL_USE_TLS'] = os.environ.get("MAIL_USE_TLS") == "True"
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get("MAIL_DEFAULT_SENDER")

mail = Mail(app)

with app.app_context():
    try:
        print(os.environ.get("MAIL_SERVER"))
        msg = Message(
            subject="Тестовое письмо",
            recipients=[os.environ.get("MAIL_USERNAME")],  # себе
            body="Это тест, проверка соединения с SMTP"
        )
        mail.send(msg)
        print("Письмо отправлено успешно!")
    except Exception as e:
        print("Ошибка при отправке письма:", e)
