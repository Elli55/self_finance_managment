# for functions, API connection and AI

import pandas as pd
import sqlite3 as sq
import json
import datetime
from pathlib import Path



Path('datas').mkdir(exist_ok=True)
Path('system').mkdir(exist_ok=True)

import streamlit as st

@st.cache_resource
def get_connection():
    return sq.connect('datas/finance.db', check_same_thread=False)

connection = get_connection()


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

CATEGORY_FOR_EXPENSES = ['Food', 'Food Out Side','Alchohol', 'Cigarette', 'Rent','Education','Gift',
                        'Debitor','Invest', 'Cleaning', 'Maintenace Staff','Travel', 'Family']


INCOME_SOURCE = ['Work', 'Schollership', 'Tips', 'Kreditor', 'Invest']

WORKED_COMPANIES = ['BrinkGeherMeyer'] 

DONOR_SCHOLLERSHIPS = ['BaFög', 'IPS']

try:

    LIST_OF_DATES_FOR_EXPENSES = pd.read_sql('''SELECT strftime('%Y-%m', date) as month FROM Expenses ''', connection)['month'].unique().tolist()
except Exception as e:
    LIST_OF_DATES_FOR_EXPENSES = []
    erro_logger(e, 'function/list_of_dates_for_expenses')    




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

 


# graphics 


CATEGORY_LIMITS_FOR_EXPENSES = {'Food': {'low': 150, 'limit':300},
                        'Alchohol': {'low': 25, 'limit':100},
                        'Cigarette':{'low':10, 'limit':30},
                        'Education': {'low': 300, 'limit':1000},
                        'Debitor': {'low': 150, 'limit':200},
                        'Cleaning': {'low': 10, 'limit':50},
                        'Maintenace Staff': {'low': 20, 'limit':50},
                        'Family':{'low': 150, 'limit':300},
                        'Travel':{'low':20, 'limit':100},
                        'Kreditor':{'low':150, 'limit':500},
                        'Gift':{'low':20, 'limit':100},
                        'Rent':{'low':250, 'limit':500},
                        'Invest':{'low':100, 'limit':500},
                        'Food Out Side':{'low':100, 'limit':200}}

def get_category_colour(category, amount):

    limit = CATEGORY_LIMITS_FOR_EXPENSES.get(category, {'low': 200, 'limit': 500})


    if amount < limit['low']:

        colour =  "#19C406" 

    elif amount < limit['limit']:

        colour =  "#FBFF00"  

    else:
        colour = '#ff0000'    

    return colour    


# for debits






