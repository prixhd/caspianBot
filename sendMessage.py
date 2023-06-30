import smtplib
from email.mime.text import MIMEText


def send_email(message):
    sender = "manap.aminov@gmail.com"
    password = "gndpjofwpzilqmbd"
    to = "caspian.tech@mail.ru"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(message)
        msg["Subject"] = "Форма вакансия на нового участника!"
        server.sendmail(sender, to, msg.as_string())

        return "Сообщение успешно отправилось!"
    except Exception as _ex:
        return f"{_ex}\nПроверьте логин или пароль пожалуйста"


def main():
    print(send_email(message="hello world"))


if __name__ == '__main__':
    main()
