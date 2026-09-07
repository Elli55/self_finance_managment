import pandas as pd
import sqlite3 as sq


with sq.connect('datas/finance.db') as connection:

    #expenses 

    def load_expenses_df():
        return pd.read_sql('SELECT * FROM Expenses', connection)

    def group_by_the_category_expenses_sum():
        df = pd.read_sql('SELECT * FROM Expenses', connection)
        df_grouped_with_cat = df.groupby(by='category')['amount'].sum().sort_values(ascending=False).reset_index()

        return df_grouped_with_cat



    sum_this_month_expenses = pd.read_sql('''SELECT SUM(amount) FROM Expenses
                                        WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')''',
                                        connection).iloc[0,0].round(2)

    df_last_month_expenses = pd.read_sql('''

                            SELECT AVG(amount) as avg_amount FROM Expenses
                            WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now', '-1 month')

                        ''', connection)
    last_month_expenses = df_last_month_expenses['avg_amount'].iloc[0].round(2) if not df_last_month_expenses.empty else 0

    delta_for_expenses = (100 - (last_month_expenses / sum_this_month_expenses * 100)).round(2)

    def sum__month_expenses(month):
            pd.read_sql(f'''SELECT SUM(amount) FROM Expenses
                                        where strftime('%Y-%m', date) = strftime('%Y-%m', {month})''',connection).iloc[0,0]



   


    #income 

    df_income = pd.read_sql('SELECT * FROM Income', connection)

    sum_this_month_income = pd.read_sql('''SELECT SUM(amount) FROM Income
                                        WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now') ''', connection).iloc[0,0]

    df_last_month_income = pd.read_sql('''

                            SELECT AVG(amount) as avg_amount FROM Income
                            WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now', '-1 month')

                    ''', connection)


    last_month_income = df_last_month_income['avg_amount'].iloc[0].round(2) if not df_last_month_income.empty else 0 

    delta_for_income =(100 - (last_month_income / sum_this_month_income * 100)).round(2)



    #balance

    df_balance = pd.read_sql('''
                    SELECT balance from Balance
                    ORDER BY id DESC LIMIT 1

                    ''', connection)

    BALANCE = df_balance['balance'].iloc[0].round(2) if not df_balance.empty else 0

    df_last_month_balance = pd.read_sql('''SELECT avg(balance) as avg_balance FROM Balance 

                WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now', '-1 month')

                ''', connection)

    last_month_balance = df_last_month_balance['avg_balance'].iloc[0].round(2) if not df_last_month_balance.empty else 0

    delta_for_balance = (100 - (last_month_balance / BALANCE * 100)).round(2)

    

