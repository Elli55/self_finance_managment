import streamlit as st
import pandas as pd
import functions
import DataWork




st.set_page_config(page_title='Finance Tracker', page_icon='💵', layout='wide')

with st.sidebar:
    st.title('Sections')
    page = st.radio('',functions.PAGE_NAMES)


if page == functions.PAGE_NAMES[1]:
  

        

    st.subheader('Input Area')


    col1, col2, col3 =st.columns([5,5,5])

    with col1:
        with st.form('WriteExpense'):
            st.subheader('Write Expenses')
            name_of_expense = st.text_input('Expense name', placeholder='Weekly...', max_chars=50)
            category = st.selectbox('Category', functions.CATEGORY_FOR_EXPENSES )
            amount_of_expense = st.number_input('Amount ', min_value=0.0, max_value=100000.0, step=0.05, value=0.0)
            note_of_expense = st.text_input('Note : ', value='None')

            if st.form_submit_button('Write'):
                if not name_of_expense:
                    st.warning('Add the NAME pls')
                elif not amount_of_expense:
                    st.warning('add the AMOUNT pls')

                else:
                    DataWork.write_expenses(name_of_expense, amount_of_expense, category, note_of_expense)
                    st.success(f'{amount_of_expense} - {name_of_expense} added to Expenses Table')

    with col2:

        with st.container(border=True):
            st.subheader('Write Income')
            name_of_income = st.selectbox('Soruce : ', options=functions.INCOME_SOURCE)

            if name_of_income == functions.INCOME_SOURCE[0]:
                with st.form(f'WriteIncome{functions.INCOME_SOURCE[0]}'):
                    company = st.selectbox('Company : ', functions.WORKED_COMPANIES)
                    from_when = st.date_input('From when : ', DataWork.DATE_OF_DAY )
                    to_when = st.date_input('To when : ', DataWork.DATE_OF_DAY )
                    if st.form_submit_button('Write'):
                        DataWork.payed_from_works(company, from_when, to_when)

            elif  name_of_income == functions.INCOME_SOURCE[1]:
                with st.form(f'WriteIncome{functions.INCOME_SOURCE[1]}'):
                    donor = st.selectbox('Soruce :', functions.DONOR_SCHOLLERSHIPS)
                    amount_from_donor = st.number_input('Amount : ', min_value=0.0 , max_value=10000.0, step=1.0)
                    if st.form_submit_button('Write'):
                        DataWork.write_income(donor,amount_from_donor, functions.INCOME_SOURCE[1])

            elif name_of_income == functions.INCOME_SOURCE[2]:
                with st.form(f'WriteIncome{functions.INCOME_SOURCE[2]}'):
                    work_place = st.selectbox('Where : ', functions.WORKED_COMPANIES)
                    amoun_of_tip = st.number_input('Amount : ', min_value=0.0, max_value=100000.0, step=1.0)
                    if st.form_submit_button('Write'):
                        DataWork.write_income(work_place, amoun_of_tip, functions.INCOME_SOURCE[2])
            elif name_of_income == functions.INCOME_SOURCE[3]:
                with st.form(f'WriteIncome{functions.INCOME_SOURCE[3]}'):
                    from_who = st.text_input('From : ', max_chars=50)
                    amoun_of_debit = st.number_input('Amount : ', max_value=10000.0, min_value=0.0, step=1.0)
                    deadline = st.date_input('Deadline : ', DataWork.DATE_OF_DAY)
                    if st.form_submit_button('Write'):
                        DataWork.write_income(from_who, amoun_of_debit, functions.INCOME_SOURCE[3])
                        DataWork.write_debits(from_who,amoun_of_debit,deadline)



    with col3:

        with st.form('WriteWorkHours'):

            st.subheader('Write Working Hours')

            company_name = st.selectbox('Company : ', functions.WORKED_COMPANIES)
            date_of_working_day = st.date_input('Date', value=DataWork.DATE_OF_DAY)
            working_hours = st.number_input('Hours : ', value=5.5 ,max_value=10000.2, min_value=0.0, step=1.0)
            salary_per_hour = st.number_input('Salary per HOUR : ', value=13.0,min_value=0.0 , max_value=10000.0, step=1.0)
            if st.form_submit_button('Write'):
                if working_hours == 0:
                    st.warning('Add the WORKING HOURS pls')
                elif salary_per_hour == 0:
                    st.warning('Add the SALARY PER HOURS pls')
                else:
                    DataWork.write_work_hours(company_name, date_of_working_day, working_hours, salary_per_hour)
                    st.success(f'For {working_hours} hours total {working_hours * salary_per_hour} earned from {company_name}')







