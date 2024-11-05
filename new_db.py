import sqlite3
import pandas as pd

df=pd.read_csv("transaction_records_1000.csv")

con = sqlite3.connect('records.db')

with open('records.sql') as f:
    con.executescript(f.read())

cur = con.cursor()

for index, row in df.iterrows():
    cur.execute("INSERT INTO records (transaction_id, transaction_type, category, amount, transaction_date, notes) VALUES (?, ?, ?, ?, ?, ?)",
                (row.transaction_id, row.transaction_type, row.category ,row.amount ,row.transaction_date, row.notes)
    )

con.commit()
con.close()