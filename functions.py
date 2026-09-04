# for functions, API connection and AI

import pandas as pd
import sqlite3 as sq

connection = sq.connect('datas/finance.db')


CATEGORY_FOR_EXPENSES = ['Food', 'Alchohol', 'Education', 'Debitor', 'Cleaning Staff', 'Maintenance Staff', 'Familie']

INCOME_SOURCE = ['Work', 'Schollership', 'Tips', 'Debit']

WORKED_COMPANIES = ['BrinkGeherMeyer'] 

DONOR_SCHOLLERSHIPS = ['BaFög', 'IPS']

PAGE_NAMES = ['Dayly Dashboard', 'Data Entery', 'Math']

LIST_OF_DATES_FOR_EXPENSES = pd.read_sql('''SELECT strftime('%Y-%m', date) as month FROM Expenses ''', connection)['month'].unique().tolist()

def sum__mont_expenses(month):
    pd.read_sql(f'''SELECT SUM(amount) FROM Expenses
                                    where strftime('%Y-%m', date) = strftime('%Y-%m', {month})''',connection).iloc[0,0]

