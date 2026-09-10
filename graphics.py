import plotly.express as px
import plotly.graph_objects as go
import calculation
import functions


# barchar for expenses

def generate_graphic_for_expenses_groupby_category():

    try:

        df_grouped = calculation.group_by_the_category_expenses_sum()

        if df_grouped is None:
            return None

        colours_for_category = [functions.get_category_colour(cat, amt)
                                for cat, amt in zip(df_grouped['category'],
                                                    df_grouped['amount'])]

        hover_text_for_barchar = []

        for _, row in df_grouped.iterrows():

            limits = functions.CATEGORY_LIMITS_FOR_EXPENSES.get(row['category'],
                                                                {'low': 200, 'limit': 300})

            hover_text_for_barchar.append(
                    f"<b>{row['category']}</b><br>"
                    f"Amount: {row['amount']}<br>"
                    f"Low: {limits['low']} €<br>"
                    f"Limit: {limits['limit']} €"
                )

        fig_for_expense_by_category = go.Figure( go.Bar(
                y=df_grouped['amount'],
                x=df_grouped['category'],
                marker_color = colours_for_category,
                text= [f'{amt:.2f}'  for amt in df_grouped['amount']],
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