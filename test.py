import datetime
import pandas as pd
import sqlite3 as sq
import calculation
import functions

connection = sq.connect('datas/finance.db')


# df_expenses = pd.read_sql('SELECT * FROM Debits', connection)

# print(df_expenses)


# print(datetime.datetime.now().strftime('%Y.%m.%d'))

# print(datetime.date.today())


# print(calculation.BALANCE)



# print(calculation.last_month_income)

# print(calculation.group_by_the_category_expenses_sum())

# for _, row in calculation.group_by_the_category_expenses_sum().iterrows():
#     print('ikinci:   ' , row)
    

print(calculation.df_debits)
