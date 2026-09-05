import datetime
import pandas as pd
import sqlite3 as sq
import calculation

connection = sq.connect('datas/finance.db')


# df_expenses = pd.read_sql('SELECT * FROM Debits', connection)

# print(df_expenses)


# print(datetime.datetime.now().strftime('%Y.%m.%d'))

# print(datetime.date.today())


# print(calculation.BALANCE)



print(calculation.last_month_income)

