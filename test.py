import datetime
import pandas as pd
import sqlite3 as sq
import calculation
import functions
import DataWork

connection = sq.connect('datas/finance.db')


# df_expenses = pd.read_sql('SELECT * FROM Debits', connection)

# print(df_expenses)


# print(datetime.datetime.now().strftime('%Y.%m.%d'))

# print(datetime.date.today())


# print(calculation.BALANCE)



# print(calculation.calculate_last_month_income_and_delta())

# a = 50
# b = 2500
# print(a / b * 100)

# print(calculation.group_by_the_category_expenses_sum())

# for _, row in calculation.group_by_the_category_expenses_sum().iterrows():
#     print('ikinci:   ' , row)
    

# print(calculation.df_debits_un_paid)
# print(calculation.load_expenses_df())
# print(sum(calculation.load_expenses_df()['amount']))
# print(calculation.df_income)

# print(calculation.df_working)


# DataWork.update_balance()



for _, line in calculation.un_paid_working_hours().iterrows():
    print(line)


# print(pd.DataFrame())



# def nese():

#     a = None

#     return print(a) or print(2)

# nese()