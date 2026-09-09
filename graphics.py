import plotly.express as px
import plotly.graph_objects as go
import calculation
import functions



# barchar for expenses

if calculation.group_by_the_category_expenses_sum() is not None:
     

    for _, row in calculation.group_by_the_category_expenses_sum().iterrows():

            
        colours_for_category = [functions.get_category_colour(cat, amt) 
                                for cat, amt in zip(calculation.group_by_the_category_expenses_sum()['category'],
                                calculation.group_by_the_category_expenses_sum()['amount'])]

                
        hover_text_for_barchar = []


        limits = functions.CATEGORY_LIMITS_FOR_EXPENSES.get(row['category'],
                                                        {'low':200, 'limit':300})

        hover_text_for_barchar.append(
                f"<b>{row['category']}</b><br>"
                f"Amount: {row['amount']}<br>"
                f"Low: {limits['low']} €<br>"
                f"Limit: {limits['limit']} €"
            )





def generate_graphic_for_expenses_groupby_category():

    try:
            
        fig_for_expense_by_category = go.Figure( go.Bar(
                y=calculation.group_by_the_category_expenses_sum()['amount'],
                x=calculation.group_by_the_category_expenses_sum()['category'],
                marker_color = colours_for_category,
                text= [f'{amt:.2f}'  for amt in calculation.group_by_the_category_expenses_sum()['amount']],
                textposition='outside',
                hovertemplate="%{customdata}<extra></extra>",
                customdata=hover_text_for_barchar
            
            ))

        fig_for_expense_by_category.update_layout(
                xaxis_title='',
                yaxis_title='Amount €',
                

            
            )

        return fig_for_expense_by_category

    except Exception as e:
            functions.erro_logger(e, 'grapichs/generate_graphic_for_expenses_groupby_category') 
            return None   

