import sqlite3 as sq
import json
import datetime
import os
import pandas as pd
from pathlib import Path

Path('datas').mkdir(exist_ok=True)

DATE_OF_DAY = datetime.datetime.today()


def erro_logger(e, location):

    data = {
        'time': datetime.datetime.now().strftime('%Y.%m.%d.%H:%M:%S'),
        'type_of_error':type(e).__name__,
        'error': str(e),
        'location':  location
    }

    with open('datas/error_logging.jsonl', 'a', encoding='utf-8') as f:
        json.dump(data, f,  ensure_ascii=False, indent=4 )

def proces_logger(mesagge : str, location : str):

    data = {
        'time': datetime.datetime.now().strftime('%Y.%m.%d.%H:%M:%S'),
        'Location': location,
        'Message': mesagge

    }

    with open('datas/proces_logging.jsonl', 'a', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)




def write_expenses(expense, amount, category, note):
    


    try:
        with sq.connect('datas/finance.db') as db:
            corsor = db.cursor()

            corsor.execute('''
                    CREATE TABLE IF NOT EXISTS Expenses(
                    
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        amount REAL,
                        category TEXT,
                        date TEXT,
                        note TEXT)
                        ''')

            corsor.execute(f'''

                    INSERT INTO Expenses(name, amount,category,  date, note) VALUES(?,?,?,?,?)''', (expense,amount,category, DATE_OF_DAY,note))

        proces_logger(f'{amount} - {expense} for {DATE_OF_DAY} added to Expenses Table ', 'DataWork/write_expenses' )
    except Exception as e:
        erro_logger(e, 'DataWork/write_expenses')



def write_income(source,  amount, note):


    try:

        with sq.connect('datas/finance.db') as db:

            corsor = db.cursor()

            corsor.execute('''
                CREATE TABLE IF NOT EXISTS Income(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                date TEXT,
                amount REAL,
                note TEXT)
                ''')

            corsor.execute(f'''

                INSERT INTO Income(source, date, amount, note) VALUES (?,?,?,?)''', (source,DATE_OF_DAY,amount,note)

                )

            proces_logger(f'{amount} EUR from {source} added to Income Table', 'DataWork/write_income')
    except Exception as e:

        erro_logger(e, 'DataWork/write_income')            


def write_work_hours(name_of_company : str, date_of_work, count_of_hours, salary_per_hour ):

    

    try:
        with sq.connect('datas/finance.db') as db:
            corsor = db.cursor()

            corsor.execute(f'''
                CREATE TABLE IF NOT EXISTS {name_of_company.strip()}(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_of_work TEXT,
                count_of_hours REAL,
                salary_per_hour REAL,
                payed INTEGER, 
                date_of_day TEXT
                )
                ''')

            corsor.execute(f'''

                INSERT INTO WorkHoursInBrink(date_of_work, count_of_hours, salary_per_hour, payed, date_of_day )
                VALUES(?,?,?,?)''', (date_of_work,count_of_hours,salary_per_hour,0,DATE_OF_DAY)
                )

            proces_logger(f'{count_of_hours} Hours for {date_of_work} added to {name_of_company.strip()} Table', 'DataWork/write_hours_from_brink')
    except Exception as e:
        erro_logger(e, 'DataWork/write_hours_from_brink')   


def payed_from_works( work_place :str ,start_date, end_date):

    try:

        with sq.connect('datas/finance.db') as db:

            corsor = db.cursor()

            corsor.execute(f'''

                    UPDATE {work_place.strip()}
                    SET payed = 1
                    WHERE DATE(date) BETWEEN DATE({start_date}) AND DATE({end_date})
                    
                    ''')

            df = pd.read_sql(f'''SELECT SUM(count_of_hours * salary_per_hour) FROM {work_place.strip()}
            
                        WHERE DATE(date) BETWEEN DATE({start_date}) AND DATE({end_date})''', db)

            write_income(work_place, df.iloc[0][0], f'From {work_place} : {start_date} - {end_date} ' )

            proces_logger(f'From  {start_date} - {end_date} added to {work_place.strip()} Table', 'DataWork/payed_from_works' )

    except Exception as e:
        erro_logger(e, 'DataWork/payed_from_works')



def write_debits(name, amount, deadline):

    try:    

        with sq.connect('datas/finance.db') as db:

            corsor = db.cursor()

            corsor.execute('''

                CREATE TABLE IF NOT EXISTS Debits(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                amount REAL,
                deadline TEXT,
                added_date TEXT)

                ''')

            corsor.execute(f'''

                INSERT INTO Debits(name, amount, deadline, added_date)
                Values(?,?,?,?)''',(name, amount,  deadline, DATE_OF_DAY)

                )

            proces_logger(f'For {name} {amount} EUR added to Debits Table ','DataWork/write_debits' )

    except Exception as e:
        erro_logger(e, 'DataWork/write_debits')


        


    