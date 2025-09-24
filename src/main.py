import pandas as pd
from excel import export_to_excel
import db
import emailService.mailService as mailService
import os
from dotenv import load_dotenv

load_dotenv()
origin, password, destiny, subject, attachment_path = os.getenv("EMAIL_origin"), os.getenv("EMAIL_pwd"), os.getenv("EMAIL_destiny"), os.getenv("EMAIL_subject"), os.getenv("EMAIL_attachment_path")

with open("emailService/emailBody.html", "r", encoding="utf-8") as f:
    htmlbody = f.read()
with open("../queries/rev_report.sql", "r", encoding="utf-8") as f:
    query = f.read()

df = db.run_query(query)

export_to_excel(df, "../output/rev_report.xlsx")

mailService.send_email(origin, password, destiny, subject, htmlbody, attachment_path)
