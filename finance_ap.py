import streamlit as st
import pandas as pd
import functions
import DataWork
import calculation
import graphics as gp
import write_month_debits
import datetime



try:

    st.set_page_config(page_title='Finance Tracker', page_icon='💵', layout='wide')

    st.markdown(functions.load_css(), unsafe_allow_html=True) 
    


    if 'page' not in st.session_state:
        st.session_state.page = functions.PAGE_NAMES[0]
except Exception as e:
    functions.erro_logger(e, 'finance_ap.py/start')        




with st.sidebar:
    st.title('Sections')
    st.divider()

    for page_name in functions.PAGE_NAMES:
        is_active = st.session_state.page == page_name
            
        if st.button(
                    page_name,
                    width='stretch',
                    type="primary" if is_active else "secondary"
                    ):
                    
                    st.session_state.page = page_name
                    st.rerun()


page = st.session_state.page


if page == functions.PAGE_NAMES[0]:


    write_month_debits.write_returned_debits()


    BALANCE = calculation.calculate_current_balance()
    last_month_balance, delta_for_balance = calculation.calculate_last_month_balance_and_delta_for_balance()
    sum_this_month_income = calculation.calculate_sum_of_this_month_income()
    last_month_income, delta_for_income = calculation.calculate_last_month_income_and_delta()
    sum_this_month_expenses = calculation.calculate_sum_of_this_month_expense()
    last_month_expenses, delta_for_expenses = calculation.last_month_expenses_and_delta()
    df_debits, df_unpaid_debits, sum_of_unpaid_debits = calculation.df_debits_and_unpaid_debits()
    df_un_paid_salary, sum_of_salary = calculation.un_paid_working_hours()







    col1, col2, col3 = st.columns(3, gap='xxsmall')


    with col1:

        st.markdown(functions.generate_metric_card('Balance',
                                                    BALANCE,
                                                      delta_for_balance,
                                                      '%',
                                                      False),
                                                          unsafe_allow_html=True)

        
    with col2:

        st.markdown(functions.generate_metric_card('Income',
                                                    sum_this_month_income,
                                                      delta_for_income,
                                                        '%',
                                                        False), 
                                                        unsafe_allow_html=True)

    with col3:

        st.markdown(functions.generate_metric_card('Expenses',
                                                   sum_this_month_expenses,
                                                     delta_for_expenses,
                                                      '%',
                                                       True ),
                                                       unsafe_allow_html=True)

    st.divider()

    st.html("<h1 class='subtitle'> This Month Expenses Graphic</h1>")


    fig_expense = gp.generate_graphic_for_expenses_groupby_category()
    if fig_expense is not None:
        st.plotly_chart(fig_expense, width='stretch')
    else:
        st.error('Graphic could not be loaded')

    st.divider()


    st.html("<h1 class='subtitle'> Debits List</h1>")

    
    if df_unpaid_debits.empty:
        st.error('No Debits more')
    else:
        with st.container():
            header_for_debits = st.columns(4, gap='xxsmall')

            header_for_debits[0].html("<p class='df_headers'> The name </p>")
            header_for_debits[1].html("<p class='df_headers'> Amount € </p>")
            header_for_debits[2].html("<p class='df_headers'> Deadline </p>")
            header_for_debits[3].html("<p class='df_headers'> Paid?  </p>")

           

            @st.dialog('Kredits')

            def pay_dialog(line):
                st.markdown(f"**{line['name']}: total kredit - {line['amount']:.2f}")
                st.divider()

                paymet_method = st.radio('Paymet Method', ['Total', 'Partially'], horizontal=True)

                rest = 0.0

                if paymet_method == 'Partially':

                    paid_amout = st.number_input('Amount: ', min_value=0.1,
                                                max_value=float(line['amount']),
                                                step=0.5,
                                                value=float(line['amount']/ 3))
                    rest = round(line['amount'] - paid_amout, 2)
                    st.caption(f'Rest amount : {rest} ')

                else:
                    paid_amout = line['amount']    

                st.divider()

                col1, col2 = st.columns(2)

                if col1.button('Paid', type='primary', width='stretch'):
                    DataWork.write_expenses(line['name'],paid_amout,'Kreditor', f'Paid kreditor for {line['name']}')
                    DataWork.change_debit_status(line['id'])
                    if rest:
                        DataWork.write_debits(line['name'], rest, line['deadline'])

                    st.rerun()

                if col2.button('Out', type='secondary', width='stretch'):
                    st.rerun()


            for _ , row in df_unpaid_debits.iterrows():

                col1, col2, col3, col4 =st.columns(4, gap='xxsmall', )

                col1.html(f"<p class='element_of_df'> {row['name']} </p>")
                col2.html(f"<p class='element_of_df'> {row['amount']} €</p>")
                col3.html(f"<p class='element_of_df'> {row['deadline']} </p>")

                if col4.button('Payed', key=f"pay_{row['id']}"):
                        pay_dialog(row)

            st.html(functions.generate_total_cards(sum_of_unpaid_debits, False))


    st.divider()

    st.html("<h1 class='subtitle'> Working Hours List </h1>")


    if df_un_paid_salary.empty:
        st.info('No more unpaid working hours')
    else:

        header_for_salary = st.columns(4, gap='xxsmall')

        header_for_salary[0].html("<p class='df_headers'>Company</p>")
        header_for_salary[1].html("<p class='df_headers'>Worked Hours</p>")
        header_for_salary[2].html("<p class='df_headers'>Nominal</p>")
        header_for_salary[3].html("<p class='df_headers'>Salary</p>")

        for _, line in df_un_paid_salary.iterrows():

            cols = st.columns(4, gap='xxsmall')

            cols[0].html(f"<p class='element_of_df'>{line['company']}</p>")
            cols[1].html(f"<p class='element_of_df'>{line['hours']}</p>")
            cols[2].html(f"<p class='element_of_df'>{line['nominal']}</p>")
            cols[3].html(f"<p class='element_of_df'>{line['salary']}</p>")

        
        st.html(functions.generate_total_cards(sum_of_salary))
                

                 
                    





if page == functions.PAGE_NAMES[1]:

  

        

    st.subheader('Input Area')


    col1, col2, col3 =st.columns([5,5,5])

    with col1:
        with st.form('WriteExpense'):
            st.subheader('Write Expenses')
            name_of_expense = st.text_input('Expense name', placeholder='Weekly...', max_chars=50)
            category = st.selectbox('Category', functions.CATEGORY_FOR_EXPENSES )
            amount_of_expense = st.number_input('Amount ', min_value=0.0, max_value=100000.0, step=0.05, value=0.0)
            date_of_expense = st.date_input('Date: ', functions.DATE_OF_DAY)
            note_of_expense = st.text_input('Note : ', value='None')

            if st.form_submit_button('Write'):
                if not name_of_expense:
                    st.warning('Add the NAME pls')
                elif not amount_of_expense:
                    st.warning('add the AMOUNT pls')

                else:
                    DataWork.write_expenses(name_of_expense, amount_of_expense, category,date_of_expense, note_of_expense)
                    st.success(f'{amount_of_expense} - {name_of_expense} added to Expenses Table')

    with col2:

        with st.container(border=True):
            st.subheader('Write Income')
            name_of_income = st.selectbox('Soruce : ', options=functions.INCOME_SOURCE)

            if name_of_income == functions.INCOME_SOURCE[0]:
                with st.form(f'WriteIncome{functions.INCOME_SOURCE[0]}'):
                    company = st.selectbox('Company : ', functions.WORKED_COMPANIES)
                    from_when = st.date_input('From when : ', functions.DATE_OF_DAY )
                    to_when = st.date_input('To when : ', functions.DATE_OF_DAY )
                    date_of_pay = st.date_input('paid When: ', functions.DATE_OF_DAY)
                    if st.form_submit_button('Write'):
                        DataWork.payed_from_works(company, date_of_pay,from_when, to_when)

            elif  name_of_income == functions.INCOME_SOURCE[1]:
                with st.form(f'WriteIncome{functions.INCOME_SOURCE[1]}'):
                    donor = st.selectbox('Soruce :', functions.DONOR_SCHOLLERSHIPS)
                    amount_from_donor = st.number_input('Amount : ', min_value=0.0 , max_value=10000.0, step=1.0)
                    date_of_stipendium = st.date_input('Date: ', functions.DATE_OF_DAY)
                    if st.form_submit_button('Write'):
                        DataWork.write_income(donor, date_of_stipendium,amount_from_donor,functions.INCOME_SOURCE[1])
                        

            elif name_of_income == functions.INCOME_SOURCE[2]:
                with st.form(f'WriteIncome{functions.INCOME_SOURCE[2]}'):
                    work_place = st.selectbox('Where : ', functions.WORKED_COMPANIES)
                    amoun_of_tip = st.number_input('Amount : ', min_value=0.0, max_value=100000.0, step=1.0)
                    date_of_Tips_taken = st.date_input('Date: ', functions.DATE_OF_DAY)
                    if st.form_submit_button('Write'):
                        DataWork.write_income(work_place, amoun_of_tip, date_of_Tips_taken,functions.INCOME_SOURCE[2])
            elif name_of_income == functions.INCOME_SOURCE[3]:
                with st.form(f'WriteIncome{functions.INCOME_SOURCE[3]}'):
                    from_who = st.text_input('From : ', max_chars=50)
                    amoun_of_debit = st.number_input('Amount : ', max_value=10000.0, min_value=0.0, step=1.0)
                    date_of_taking = st.date_input('Date: ', functions.DATE_OF_DAY)
                    deadline = st.date_input('Deadline : ', functions.DATE_OF_DAY)
                    if st.form_submit_button('Write'):
                        DataWork.write_income(from_who, amoun_of_debit,date_of_taking, functions.INCOME_SOURCE[3])
                        DataWork.write_debits(from_who,amoun_of_debit,deadline,date_of_taking)
            elif name_of_income ==  functions.INCOME_SOURCE[4]:
                with st.form(f'WriteIncome{functions.INCOME_SOURCE[4]}'):
                    type_of_invest = st.selectbox('Which one: ', ['Cash','Coin', 'Crypto'])     
                    amount_from_invest = st.number_input('Amount: ', min_value=0.0, step=1.0)
                    date_of_invest_taken = st.date_input('Date: ', functions.DATE_OF_DAY)
                    if st.form_submit_button('Write'):
                        DataWork.write_income(type_of_invest,amount_from_invest,date_of_invest_taken, functions.INCOME_SOURCE[4])





    with col3:

        with st.form('WriteWorkHours'):
            st.subheader('Write Working Hours')

            company_name    = st.selectbox('Company', functions.WORKED_COMPANIES)
            date_of_work    = st.date_input('Date', value=datetime.date.today())

            col_t1, col_t2 = st.columns(2)
            with col_t1:
                start_time  = st.time_input('Start time', value=datetime.time(12, 0))
            with col_t2:
                end_time    = st.time_input('End time',   value=datetime.time(18, 0))

            salary_per_hour = st.number_input('Salary per hour (€)',
                                            value=13.0, min_value=0.0,
                                            max_value=1000.0, step=0.5)

            
            if start_time and end_time:
                from datetime import datetime as dt
                diff = round(
                    (dt.combine(datetime.date.today(), end_time) -
                    dt.combine(datetime.date.today(), start_time)
                    ).total_seconds() / 3600, 2
                )
                if diff > 0:
                    st.caption(f'Total: {diff}h × {salary_per_hour} € = {round(diff * salary_per_hour, 2)} €')
                else:
                    st.warning('End time must be after start time')

            if st.form_submit_button('Write'):
                if end_time <= start_time:
                    st.error('End time must be after start time')
                else:
                    DataWork.write_work_hours(
                        company_name, date_of_work,
                        start_time, end_time, salary_per_hour
                    )
                    st.success(f'{diff}h added for {company_name}')





