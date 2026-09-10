import datetime
import pandas as pd
import sqlite3 as sq
import calculation
import functions
import DataWork

connection = sq.connect('datas/finance.db')


# df_expenses = pd.read_sql('SELECT * FROM Debits', connection)

# print(df_expenses)


# print(datetime.datetime.now().strftime('%Y.%m.%d'))

# print(datetime.date.today())


# print(calculation.BALANCE)



# print(calculation.last_month_income)

# print(calculation.group_by_the_category_expenses_sum())

# for _, row in calculation.group_by_the_category_expenses_sum().iterrows():
#     print('ikinci:   ' , row)
    

# print(calculation.df_debits_un_paid)
# print(calculation.load_expenses_df())
# print(sum(calculation.load_expenses_df()['amount']))
# print(calculation.df_income)

# print(calculation.df_working)


DataWork.update_balance()



# import sqlite3 as sq

# def reset_tables():
#     try:
#         with sq.connect('datas/finance.db') as conn:
#             cursor = conn.cursor()
            
#             # Debits cədvəlini sil
#             cursor.execute("DROP TABLE IF EXISTS Debits")
#             print("✅ Debits cədvəli silindi")
            
#             # Income cədvəlini sil
#             cursor.execute("DROP TABLE IF EXISTS Income")
#             print("✅ Income cədvəli silindi")
            
#             conn.commit()
#             print("\n🎉 Hər iki cədvəl uğurla silindi!")
            
#     except Exception as e:
#         print(f"❌ Xəta: {e}")

# if __name__ == "__main__":
#     confirm = input("⚠️  Debits və Income cədvəlləri silinəcək. Davam etmək istəyirsiniz? (y/n): ")
#     if confirm.lower() == 'y':
#         reset_tables()
#     else:
#         print("❌ Əməliyyat ləğv edildi")