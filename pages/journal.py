from dash import register_page, html, callback, Input, Output, no_update
import dash_bootstrap_components as dbc
from components import utils
from models.models import get_user_places, get_all_booked_places

register_page(
    __name__,
    path='/journal'
)

layout = dbc.Container([
   utils.app_header('Журнал'),
   dbc.Tabs([
       dbc.Tab(html.Div(id='journal-places-my'), label='Мои'),
       dbc.Tab(html.Div(id='journal-places-all'), label='Всего отдела'),
   ], class_name='mt-3 fw-bold'),
   html.Div(utils.app_footer(2), className='mt-auto')
], fluid=True, style={'height': '100vh'}, class_name='d-flex flex-column')

@callback(
    Output('journal-places-my', 'children'),
    Input('common-store-user_name', 'data')
)
def journal_update_history(data):
    result = get_user_places(4)
    # result = get_user_places(data['username'])
    if result:
        return [
            html.Div([
                html.Div(html.I(className='bi bi-person-circle display-1 text-primary')),
                html.Div([
                    html.H2(x['place'], className='mb-1 mt-3 fw-bold'),
                    html.P(x['name'], className='mb-1'),
                    html.P(x['dt'], className='mb-3 text-secondary fst-italic'),
                ]),
                html.I(className='bi bi-trash-fill fs-3', style={'color': 'red'}, id={'type': 'journal-rmbtn', 'index': x['row_id']})
            ], className='d-flex justify-content-around align-items-center border-bottom border-2') for x in result
        ]


@callback(
    Output('journal-places-all', 'children'),
    Input('common-store-user_name', 'data')
)
def journal_update_history_all(data):
    result = get_all_booked_places()
    if result:
        return [
            html.Div([
                html.Div(html.I(className='bi bi-person-circle display-1 text-primary')),
                html.Div([
                    html.H2(x['place'], className='mb-1 mt-3 fw-bold'),
                    html.P(x['name'], className='mb-1'),
                    html.P(x['dt'], className='mb-3 text-secondary fst-italic'),
                ]),
                html.I(className='bi bi-info-square fs-3', style={'color': 'blue'}),
            ], className='d-flex justify-content-around align-items-center border-bottom border-2') for x in result
        ]