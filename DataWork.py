import sqlite3 as sq
import functions
import pandas as pd
from datetime import datetime



def update_balance():

    try:
        with sq.connect('datas/finance.db', check_same_thread=False) as db:

            sum_of_expenses = pd.read_sql('SELECT SUM(amount) FROM Expenses', db).iloc[0, 0]
            sum_of_income = pd.read_sql('SELECT SUM(amount) FROM Income', db).iloc[0,0]
            balance =  sum_of_income - sum_of_expenses

            corsor = db.cursor()

            corsor.execute('''

                        CREATE TABLE IF NOT EXISTS Balance(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date  TEXT,
                        balance REAL 
                        )

                        ''')

            corsor.execute('''INSERT INTO Balance(date, balance)
                                VALUES(?,?)

                                    ''', (functions.DATE_OF_DAY, balance))

            functions.proces_logger(f'for {functions.DATE_OF_DAY} balance refreshed currrent Balance : {balance}', 'DataWork/update_balance')

    except Exception as e:

        functions.erro_logger(e, 'DataWork/update_balance')


        


def write_expenses(expense, amount, category, date,note):
    


    try:
        with sq.connect('datas/finance.db', check_same_thread=False) as db:
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

                    INSERT INTO Expenses(name, amount,category,  date, note) VALUES(?,?,?,?,?)''',
                      (expense,amount,category, date, note))
            update_balance()

        functions.proces_logger(f'{amount} - {expense} for {functions.DATE_OF_DAY} added to Expenses Table ', 'DataWork/write_expenses' )
    except Exception as e:
        functions.erro_logger(e, 'DataWork/write_expenses')



def write_income(source,  amount,date, note):


    try:

        with sq.connect('datas/finance.db', check_same_thread=False) as db:

            corsor = db.cursor()

            corsor.execute('''
                CREATE TABLE IF NOT EXISTS Income(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                amount REAL,
                date TEXT,
                note TEXT)
                ''')

            corsor.execute(f'''

                INSERT INTO Income(source,  amount, date,note) VALUES (?,?,?,?)''',
                  (source,amount,date,note)

                )

            update_balance()

            functions.proces_logger(f'{amount} EUR from {source} added to Income Table', 'DataWork/write_income')
    except Exception as e:

        functions.erro_logger(e, 'DataWork/write_income')            


def write_work_hours(company, date_of_work, start_time, end_time, salary_per_hour):
    try:
        
        
        fmt = '%H:%M:%S'
        start = datetime.strptime(str(start_time), fmt)
        end   = datetime.strptime(str(end_time),   fmt)
        total_hours = round((end - start).total_seconds() / 3600, 2)

        if total_hours <= 0:
            functions.erro_logger('End time must be after start time', 'DataWork/write_work_hours')
            return

        with sq.connect('datas/finance.db', check_same_thread=False) as db:
            cursor = db.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS WorkHours(
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    company         TEXT,
                    date_of_work    TEXT,
                    start_time      TEXT,
                    end_time        TEXT,
                    total_hours     REAL,
                    salary_per_hour REAL,
                    payed           INTEGER DEFAULT 0,
                    date_of_day     TEXT)
            ''')
            cursor.execute(
                '''INSERT INTO WorkHours
                   (company, date_of_work, start_time, end_time, total_hours, salary_per_hour, payed, date_of_day)
                   VALUES(?,?,?,?,?,?,0,?)''',
                (company, str(date_of_work), str(start_time), str(end_time),
                 total_hours, salary_per_hour, functions.DATE_OF_DAY)
            )

        functions.proces_logger(
            f'{company} | {date_of_work} | {start_time}-{end_time} | {total_hours}h added',
            'DataWork/write_work_hours'
        )

    except Exception as e:
        functions.erro_logger(e, 'DataWork/write_work_hours')


def payed_from_works(work_place, start_date, end_date):
    try:
        with sq.connect('datas/finance.db', check_same_thread=False) as db:
            cursor = db.cursor()
            cursor.execute(
                '''UPDATE WorkHours SET payed = 1
                   WHERE company = ? AND DATE(date_of_work) BETWEEN DATE(?) AND DATE(?)''',
                (work_place, str(start_date), str(end_date))
            )
            df = pd.read_sql(
                '''SELECT SUM(total_hours * salary_per_hour) as total
                   FROM WorkHours
                   WHERE company = ? AND DATE(date_of_work) BETWEEN DATE(?) AND DATE(?)''',
                db,
                params=(work_place, str(start_date), str(end_date))
            )
            total = float(df.iloc[0][0] or 0)
            write_income(work_place, total, f'From {work_place}: {start_date} - {end_date}')

        functions.proces_logger(f'{work_place} | {start_date}-{end_date} paid', 'DataWork/payed_from_works')

    except Exception as e:
        functions.erro_logger(e, 'DataWork/payed_from_works')



def write_debits(name, amount, deadline,date):

    try:    

        with sq.connect('datas/finance.db', check_same_thread=False) as db:

            corsor = db.cursor()

            corsor.execute('''

                CREATE TABLE IF NOT EXISTS Debits(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                amount REAL,
                deadline TEXT,
                status INTEGER,
                added_date TEXT)

                ''')

            corsor.execute(f'''

                INSERT INTO Debits(name, amount, deadline, status, added_date)
                Values(?,?,?,?,?)''',(name, amount,  deadline, 0, date)

                )

            update_balance()

            functions.proces_logger(f'For {name} {amount} EUR added to Debits Table ','DataWork/write_debits' )

    except Exception as e:
        functions.erro_logger(e, 'DataWork/write_debits')


def change_debit_status(iid):

    try:
        with sq.connect('datas/finance.db', check_same_thread=False) as db:

            corsor = db.cursor()

            corsor.execute('''

                    UPDATE Debits
                    SET status = 1
                    WHERE id = ? 

                    ''', (iid,))
            
            functions.proces_logger(f'for {iid} of debit status changed', 'functions/change_debit_status')
    except Exception as e:
        functions.erro_logger(e, 'functions/change_debit_status')            


