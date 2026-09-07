# for functions, API connection and AI

import pandas as pd
import sqlite3 as sq
import json
import datetime
from pathlib import Path

connection = sq.connect('datas/finance.db')

Path('datas').mkdir(exist_ok=True)
Path('system').mkdir(exist_ok=True)


# logging

def erro_logger(e, location):

    data = {
        'time': datetime.datetime.now().strftime('%Y.%m.%d.%H:%M:%S'),
        'type_of_error':type(e).__name__,
        'error': str(e),
        'location':  location
    }

    with open('system/error_logging.jsonl', 'a', encoding='utf-8') as f:
        json.dump(data, f,  ensure_ascii=False, indent=4 )

def proces_logger(mesagge : str, location : str):

    data = {
        'time': datetime.datetime.now().strftime('%Y.%m.%d.%H:%M:%S'),
        'Location': location,
        'Message': mesagge

    }

    with open('system/proces_logging.jsonl', 'a', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)





# globals

DATE_OF_DAY = datetime.datetime.today().strftime('%Y-%m-%d')

PAGE_NAMES = ['Dayly Dashboard', 'Data Entery', 'Math']

CATEGORY_FOR_EXPENSES = ['Food', 'Alchohol', 'Education', 'Debitor', 'Cleaning Staff', 'Maintenance Staff', 'Familie']

INCOME_SOURCE = ['Work', 'Schollership', 'Tips', 'Debit']

WORKED_COMPANIES = ['BrinkGeherMeyer'] 

DONOR_SCHOLLERSHIPS = ['BaFög', 'IPS']

LIST_OF_DATES_FOR_EXPENSES = pd.read_sql('''SELECT strftime('%Y-%m', date) as month FROM Expenses ''', connection)['month'].unique().tolist()




# css 
def load_css():
    with open('style.css') as f:
        return f'<style> {f.read()} </style>'


# html works    


def generate_metric_card(titel : str, value : float, delta: float, delta_sign : str,  ineverse : bool = False):

   try:
        

        delta_title = '▲' if delta > 0 else '▼'

        if ineverse is False:
            background_colour = 'background_positive' if value <= 0 else 'background_negative' 
            font_colour = 'font_positive' if value <= 0 else 'font_negative' 

        else:
            
            background_colour = 'background_positive' if value > 0 else 'background_negative' 
            font_colour = 'font_positive' if value > 0 else 'font_negative' 


        proces_logger(f'for {titel} the metric card generated','functions/generate_metric_card')


        return  f'''<section class='metric_card {background_colour}'>
            <p class='title_of_matric_card'> {titel} </p>
            <h2 class='value_of_metric_card {font_colour}'> {value} </h2>
            <p class='delta_of_metric_card'> {delta_title} {delta} {delta_sign} </p>
            </section>
            '''    
        
   except Exception as e:
       erro_logger(e, 'functions/generate_matric_card')

 

    




