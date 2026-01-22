from dash import register_page, html, callback, dcc, Output, Input
import dash_bootstrap_components as dbc
from components import utils
import plotly.express as px
from models.models import engine
import pandas as pd
from pyecharts.charts import Bar
from pyecharts import options as opts
import dash_echarts as echarts


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
        '''select booked_at, count(*) as value
           from bookings 
           where person_id > 0 
           group by booked_at''',
        engine
    )

    option = {
        "title": {"text": "Динамика бронирования по дням"},
        "tooltip": {},
        "legend": {"bottom": 0},
        "grid": {"left": 30},

        # 🔥 ПАЛИТРА ЦВЕТОВ
        "color": [
            "#5470C6", "#91CC75", "#FAC858", "#EE6666",
            "#73C0DE", "#3BA272", "#FC8452", "#9A60B4",
            "#EA7CCC", "#FF9F7F", "#8378EA", "#96BFFF"
        ],

        "xAxis": {
            "type": "category",
            "name": "Дни",
            "data": df["booked_at"].astype(str).tolist()
        },
        "yAxis": {
            "type": "value",
            "name": "Кол-во сотрудников",
            "nameLocation": "middle",
            "nameGap": 50
        },
        "series": [
            {
                "name": "Дата бронирования",
                "type": "bar",
                "color": 'darkblue',
                "data": df["value"].tolist()
            }
        ]
    }



    return echarts.DashECharts(
        option=option,
        style={"height": "400px", "width": "100%"}
    )