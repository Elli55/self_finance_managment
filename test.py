import datetime
import pandas as pd
import sqlite3 as sq

connection = sq.connect('datas/finance.db')


df_expenses = pd.read_sql('SELECT * FROM Expenses', connection)

print(df_expenses)


# print(datetime.datetime.now().strftime('%Y.%m.%d'))

# print(datetime.date.today())