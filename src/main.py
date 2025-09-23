import pandas as pd
import db
from excel import export_to_excel

with open("../queries/rev_report.sql", "r", encoding="utf-8") as f:
    query = f.read()

df = db.run_query(query)

export_to_excel(df, "../output/rev_report.xlsx")

print(df.head())
