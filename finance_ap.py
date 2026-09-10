import streamlit as st
import pandas as pd
import functions
import DataWork
import calculation
import graphics as gp



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
                    use_container_width=True,
                    type="primary" if is_active else "secondary"
                    ):
                    
                    st.session_state.page = page_name
                    st.rerun()


page = st.session_state.page


if page == functions.PAGE_NAMES[0]:
    col1, col2, col3 = st.columns(3, gap='xxsmall')


    with col1:

        st.markdown(functions.generate_metric_card('Balance',
                                                    calculation.BALANCE,
                                                      calculation.delta_for_balance,
                                                      '%',
                                                      False),
                                                          unsafe_allow_html=True)

        
    with col2:

        st.markdown(functions.generate_metric_card('Income',
                                                    calculation.sum_this_month_income,
                                                      calculation.delta_for_income,
                                                        '%',
                                                        False), 
                                                        unsafe_allow_html=True)

    with col3:

        st.markdown(functions.generate_metric_card('Expenses',
                                                   calculation.sum_this_month_expenses,
                                                     calculation.delta_for_expenses,
                                                      '%',
                                                       True ),
                                                       unsafe_allow_html=True)

    st.divider()

    fig_expense = gp.generate_graphic_for_expenses_groupby_category()
    if fig_expense:
        st.plotly_chart(gp.generate_graphic_for_expenses_groupby_category(),  width='stretch')
    else:
        st.error('Graphic couldnt enroaled') 

    st.divider()


    df_debits = calculation.df_debits_un_paid

    
    if df_debits.empty:
        st.error('No Debits more')
    else:
        with st.container():
            header = st.columns(4, gap='xxsmall')

            header[0].html("<p class='title_for_db_df'> The name </p>")
            header[1].html("<p class='title_for_db_df'> Amount € </p>")
            header[2].html("<p class='title_for_db_df'> Deadline </p>")
            header[3].html("<p class='title_for_db_df'> Paid?  </p>")

           

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

                if col1.button('Paid', type='primary', use_container_width=True):
                    DataWork.write_expenses(line['name'],paid_amout,'Kreditor', f'Paid kreditor for {line['name']}')
                    DataWork.change_debit_status(line['id'])
                    if rest:
                        DataWork.write_debits(line['name'], rest, line['deadline'])

                    st.rerun()

                if col2.button('Out', type='secondary', use_container_width=True):
                    st.rerun()







            for _ , row in df_debits.iterrows():

                col1, col2, col3, col4 =st.columns(4, gap='xxsmall', )

                col1.html(f"<p class='element_for_db_df'> {row['name']} </p>")
                col2.html(f"<p class='element_for_db_df'> {row['amount']} €</p>")
                col3.html(f"<p class='element_for_db_df'> {row['deadline']} </p>")

                if col4.button('Payed', key=f"pay_{row['id']}"):
                        pay_dialog(row)

                    

                 
                    





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

            company_name = st.selectbox('Company : ', functions.WORKED_COMPANIES)
            date_of_working_day = st.date_input('Date', value=functions.DATE_OF_DAY)
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







