import pandas as pd
import sqlite3 as sq


with sq.connect('datas/finance.db') as connection:

    #expenses 

    df_expenses = pd.read_sql('SELECT * FROM Expenses', connection)


    sum_this_month_expenses = pd.read_sql('''SELECT SUM(amount) FROM Expenses
                                        WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')''',connection).iloc[0,0]

    print(f'This mons expenses: {sum_this_month_expenses}')


    #income 

    df_income = pd.read_sql('SELECT * FROM Income', connection)
    print(df_income)
    sum_this_month_income = pd.read_sql('''SELECT SUM(amount) FROM Income
                                        WHERE strftime('%Y-%m', date) = strftime('&Y-%m', 'now') ''', connection).iloc[0,0]

    print(f'sum of this month income : {sum_this_month_income}')

    #balance

    df_balance = pd.read_sql('''
                    SELECT balance from Balance
                    ORDER BY id DESC LIMIT 1

                    ''', connection)

    BALANCE = df_balance['balance'].iloc[0] if not df_balance.empty else 0

    df_last_month_balance = pd.read_sql('''SELECT avg(balance) as avg_balance FROM Balance 

                WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now', '-1 month')

                ''', connection)

    LAST_MONTH_BALANCE = df_last_month_balance['avg_balance'].iloc[0] if not df_last_month_balance.empty else 0

    DELTA_FOR_BALANCE = LAST_MONTH_BALANCE / BALANCE * 100

