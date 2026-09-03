import sqlite3 as sq
import json
import datetime
import os
from pathlib import Path

Path('datas').mkdir(exist_ok=True)

DATE_OF_DAY = datetime.datetime.now().strftime('%Y.%m.%d')


def logger(e, location):

    data = {
        'time': datetime.datetime.now().strftime('%Y.%m.%d.%H:%M:%S'),
        'type_error':type(e).__name__,
        'error': e,
        'location':  location
    }

    with open('datas/logging.jsonl', 'a', encoding='utf-8') as f:
        json.dump(data, f,  ensure_ascii=False, indent=4 )





def write_expenses(expense, amount, note):
        

    
    data = [expense, DATE_OF_DAY, amount, note]

    try:
        with sq.connect('datas/finance.db') as db:
            corsor = db.cursor()

            corsor.execute('''
                    CREATE TABLE IF NOT EXISTS Expenses(
                    
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        date TEXT,
                        amount REAL,
                        note TEXT)
                        ''')

            corsor.execute('''

                    INSERT INTO Expenses(name, date, amount, note) VALUES(?,?,?,?)''', data)

        print(f'{amount} EUR added for {expense}')
    except Exception as e:
        logger(e, 'calculation/write_expenses')



def write_income(source,  amount, note):

    data = [source, DATE_OF_DAY, amount, note]

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

            corsor.execute('''

                INSERT INTO Income(source, date, amount, note) VALUES (?,?,?,?)

                ''', data)

            print(f'{amount} EUR from {source} added to Income')
    except Exception as e:

        logger(e, 'calculation/write_income')            