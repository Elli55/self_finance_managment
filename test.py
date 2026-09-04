import datetime
import pandas as pd
import sqlite3 as sq
import calculation

connection = sq.connect('datas/finance.db')


df_expenses = pd.read_sql('SELECT * FROM Debits', connection)

print(df_expenses)


# print(datetime.datetime.now().strftime('%Y.%m.%d'))

# print(datetime.date.today())


print(calculation.BALANCE)








import sqlite3 as sq
import random
import pandas as pd
from datetime import datetime, timedelta

def generate_income_data():
    # Bu ay və ötən ay üçün tarix aralığı
    today = datetime.today()
    
    # Ötən ayın ilk günü
    first_day_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
    # Bu ayın ilk günü
    first_day_this_month = today.replace(day=1)
    
    # Bütün tarixlər (ötən ay + bu ay)
    dates = []
    current = first_day_last_month
    while current <= today:
        dates.append(current.strftime('%Y-%m-%d'))
        current += timedelta(days=1)
    
    # Random məlumat mənbələri
    sources = ['Maaş', 'Təqaüd', 'Freelance', 'Bahşiş', 'Müştəri', 
               'Proyekt', 'Hədiyyə', 'Debit', 'Kredit', 'Dividend']
    
    with sq.connect('datas/finance.db') as db:
        cursor = db.cursor()
        
        # Income cədvəlinə random məlumat əlavə et
        count = 0
        for date in dates:
            # Hər gün üçün 0-3 ədəd random gəlir
            num_entries = random.randint(0, 3)
            
            for _ in range(num_entries):
                source = random.choice(sources)
                amount = round(random.uniform(10.0, 1500.0), 2)
                note = f"Random gəlir {random.randint(1, 100)}"
                
                cursor.execute('''
                    INSERT INTO Income (source, date, amount, note)
                    VALUES (?, ?, ?, ?)
                ''', (source, date, amount, note))
                count += 1
        
        db.commit()
        print(f"✅ Income cədvəlinə {count} random məlumat əlavə edildi!")
        print(f"📅 Tarix aralığı: {first_day_last_month.strftime('%Y-%m-%d')} - {today.strftime('%Y-%m-%d')}")

# İŞLƏT
generate_income_data()