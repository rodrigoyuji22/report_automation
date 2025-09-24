import pandas as pd
from excel import export_to_excel
import db
import mailService
from config import origin, password, destiny, subject, htmlbody, attachment_path


with open("../queries/rev_report.sql", "r", encoding="utf-8") as f:
    query = f.read()

df = db.run_query(query)

export_to_excel(df, "../output/rev_report.xlsx")

mailService.send_email(origin, password, destiny, subject, htmlbody, attachment_path)
