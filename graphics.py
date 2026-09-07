import plotly.express as px
import calculation
import functions

def generate_graphic_for_expenses_groupby_category():
    try:
        
        fig_for_expense_by_category = px.bar(
            calculation.group_by_the_category_expenses_sum(),
            x='category',
            y='amount',
            title='Graphic of expenses by category',
            color='amount',
            color_continuous_scale='Greens',
            labels={'category':'Category', 'amount':'Amount  €'},
            text='amount'
        )

        return fig_for_expense_by_category

    except Exception as e:
        functions.erro_logger(e, 'grapichs/generate_graphic_for_expenses_groupby_category')    

