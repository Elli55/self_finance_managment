import datetime
import pandas as pd
import sqlite3 as sq
import calculation
import functions
import DataWork

connection = functions.connection



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



# for _, line in calculation.un_paid_working_hours().iterrows():
#     print(line)

# print(sum(calculation.un_paid_working_hours()['salary']))


# print(pd.DataFrame())



# def nese():

#     a = None

#     return print(a) or print(2)

# nese()



# for _, line in calculation.load_expenses_df().tail(10).iloc[::-1].iterrows():
#     print(line['name'])

# df_work_hours = pd.read_sql('SELECT * FROM WorkHours', connection)

# total_chek = 0
# for _, line in df_work_hours.iterrows():

#     if line['company'] == 'BrinkGeherMeyer':
#         total_chek += line['total_hours']

# print(total_chek) 


def un_paid_working_hours():

    df_work_hours = pd.read_sql('SELECT * FROM WorkHours', connection)

    work_hours = {'BrinkGeherMeyer':{'workhours':0, 'nominal':13}}

    for _, line in df_work_hours.iterrows():

      if line['company'] == 'BrinkGeherMeyer':
         work_hours['BrinkGeherMeyer'] += line['total_hours']

      else:
        try:
         
            grouped_by_company = pd.read_sql('''
         
                SELECT company, SUM(total_hours * salary_per_hour)  as salary, SUM(total_hours) as hours, salary_per_hour as nominal  FROM WorkHours
                WHERE payed = 0
                GROUP BY company
                ''', connection)
         
            sum_of_salary = sum(grouped_by_company['salary'])
         
            return grouped_by_company, sum_of_salary
         
        except Exception as e:
                functions.erro_logger(e, 'calculation/un_paid_working_hours')
                grouped_by_company = pd.DataFrame()
                sum_of_salary = 0
                return grouped_by_company, sum_of_salary   
          


def fix_monthly_salary_from_companies(company,month, salary_hours):

    df__monthly = pd.read_sql('''SELECT * FROM WorkHours
                                WHERE company = ?
                                AND strftime('%m.%Y', date_of_work) = ?  ''',
                                connection, params=(company, month))

    working_hours = 0
    
    for _, line in df__monthly.iterrows():

        working_hours += line['total_hours']

    print(working_hours)

        



fix_monthly_salary_from_companies('BrinkGeherMeyer', '09.2026', 0)    

    


    




# print(datetime.datetime.month.setter('September'))