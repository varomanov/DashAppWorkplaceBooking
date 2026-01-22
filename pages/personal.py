from dash import register_page, html, callback, dcc, Output, Input
import dash_bootstrap_components as dbc
from components import utils
import plotly.express as px
from models.models import engine
import pandas as pd

register_page(
    __name__,
    path='/personal'
)

layout = dbc.Container([
   utils.app_header('График'),
   html.Div(id='chart_container', className='mt-5'),
   html.Div(utils.app_footer(4), className='mt-auto')
], fluid=True, style={'height': '100dvh'}, class_name='d-flex flex-column')

@callback(
    Output('chart_container', 'children'),
    Input('common-store-user_name', 'data')
)
def update_chart(data):
    df = pd.read_sql(
        '''select booked_at, count(*) as 'value'
        from bookings 
        where person_id > 0 
        group by booked_at''', 
    engine)
    fig = px.bar(data_frame=df, x='booked_at', y='value', color='booked_at', height=600)
    fig.update_layout(title='Динамика бронирования по дням', xaxis_title='Дни', yaxis_title='Кол-во сотрудников')
    return dcc.Graph(figure=fig)