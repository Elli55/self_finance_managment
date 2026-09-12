import pandas as pd
import sqlite3 as sq
import functions


connection = functions.connection


# balance
def calculate_current_balance():
    try:
        income = pd.read_sql(
            'SELECT SUM(amount) as total FROM Income',
            connection
        ).iloc[0, 0] or 0.0

        expenses = pd.read_sql(
            'SELECT SUM(amount) as total FROM Expenses',
            connection
        ).iloc[0, 0] or 0.0

        return round(float(income) - float(expenses), 2)

    except Exception as e:
        functions.erro_logger(e, 'calculation/calculate_current_balance')
        return 0.0


def calculate_last_month_balance_and_delta_for_balance():
    try:

        df_last_month_balance = pd.read_sql('''SELECT avg(balance) as avg_balance FROM Balance 

                        WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now', '-1 month')

                        ''', connection)

        last_month_balance = df_last_month_balance['avg_balance'].iloc[0].round(2) if not df_last_month_balance.empty else 0

        delta_for_balance = round((last_month_balance - calculate_current_balance()) / last_month_balance * 100, 2)

    except Exception as e:
        functions.erro_logger(e, 'calculation/calculate_last_month_balance_and_delta_of_balance')
        delta_for_balance = 0
        last_month_balance = 0
    return last_month_balance, delta_for_balance


# expenses

def load_expenses_df():
    return pd.read_sql('SELECT * FROM Expenses', connection)


def calculate_sum_of_this_month_expense():
    try:
        sum_this_month_expenses = pd.read_sql('''SELECT SUM(amount) FROM Expenses
                                            WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')''',
                                            connection).iloc[0,0].round(2)
    except Exception as e:
        functions.erro_logger(e, 'calculation/calculate_sum_of_this_month_expenses')
        sum_this_month_expenses = 0

    return sum_this_month_expenses


def group_by_the_category_expenses_sum():

    try:
        df = pd.read_sql('''SELECT * FROM Expenses
                            WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')''', connection)
        df_grouped_with_cat = df.groupby(by='category')['amount'].sum().sort_values(ascending=False).reset_index()

    except Exception as e:
        functions.erro_logger(e, 'calculation/group_by_the_category_expenses_sum')
        df_grouped_with_cat = None
    return df_grouped_with_cat


def last_month_expenses_and_delta():

    try:
        df_last_month_expenses = pd.read_sql('''

                                SELECT SUM(amount) as sum_amount FROM Expenses
                                WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now', '-1 month')

                            ''', connection)
        last_month_expenses = df_last_month_expenses['sum_amount'].iloc[0].round(2) if not df_last_month_expenses.empty else 0

        delta_for_expenses =round((last_month_expenses - calculate_sum_of_this_month_expense()) /  last_month_expenses * 100, 2)

    except Exception as e:
        functions.erro_logger(e, 'calculation/last_month_expenses_and_delta')
        delta_for_expenses = 0
        last_month_expenses = 0
    return last_month_expenses, delta_for_expenses


def sum_month_expenses(month):
        return pd.read_sql(f'''SELECT SUM(amount) FROM Expenses
                                    where strftime('%Y-%m', date) = strftime('%Y-%m', {month})''', connection).iloc[0,0]


# income

def calculate_sum_of_this_month_income():

    try:

        df_income = pd.read_sql('SELECT * FROM Income', connection)

        sum_this_month_income = pd.read_sql('''SELECT SUM(amount) FROM Income
                                            WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now') ''', connection).iloc[0,0]

    except Exception as e:
        functions.erro_logger(e, 'calculation/calculate_sum_income')
        sum_this_month_income = 0

    return sum_this_month_income


def calculate_last_month_income_and_delta():

    try:

        df_last_month_income = pd.read_sql('''

                                                SELECT SUM(amount) as total FROM Income
                                                WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now', '-1 month')

                                        ''', connection)


        last_month_income = df_last_month_income['total'].iloc[0].round(2) if not df_last_month_income.empty else 0

        delta_for_income = round((last_month_income - calculate_sum_of_this_month_income()) / last_month_income * 100, 2)
    except Exception as e:
        functions.erro_logger(e, 'calculation/calculate_last_month_income_and_delta')

        last_month_income = 0
        delta_for_income = 0
    return last_month_income, delta_for_income


# debits

def df_debits_and_unpaid_debits():

    try:
        df_debits = pd.read_sql('SELECT * FROM Debits', connection)
        df_debits_un_paid = pd.read_sql('SELECT * FROM Debits WHERE status = 0', connection)
    except  Exception as e:
        functions.erro_logger(e, 'calculation/df_debits_and_unpaid_debits')
        df_debits = None
        df_debits_un_paid = pd.DataFrame()
    return df_debits, df_debits_un_paid


# working

df_work_hours = pd.read_sql('SELECT * FROM WorkHours', connection)

def un_paid_working_hours():

    try:

        grouped_by_company = pd.read_sql('''

                            SELECT company, SUM(total_hours * salary_per_hour)  as salary, SUM(total_hours) as hours, salary_per_hour as nominal  FROM WorkHours
                            WHERE payed = 0
                            GROUP BY company

                            ''', connection)

        return grouped_by_company

    except Exception as e:
        functions.erro_logger(e, 'calculation/un_paid_working_hours')
        grouped_by_company = pd.DataFrame()
        return grouped_by_company