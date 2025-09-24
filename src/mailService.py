import smtplib
from email.message import EmailMessage
from pathlib import Path
import ssl

def send_email(_origin, _password, _destiny, _subject, _body, _attachment = None):
    msg = EmailMessage()
    msg["From"] = _origin
    msg["To"] = _destiny
    msg["Subject"] = _subject
    msg.add_alternative(_body, subtype = "html")

    file_path = Path(_attachment)
    with open(file_path, "rb") as f:
        file_data = f.read()
        file_name = file_path.name
    msg.add_attachment(file_data, maintype = "application", subtype = "vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename = file_name)

    with smtplib.SMTP("smtp.office365.com", 587) as smtp:
        smtp.starttls()
        smtp.login(_origin, _password)
        smtp.send_message(msg)


