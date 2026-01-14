from dash import register_page, html, dcc, callback, Input, Output, no_update, ALL, ctx, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from components import utils
from models.models import get_user_places, get_all_booked_places, remove_place

register_page(
    __name__,
    path='/journal'
)

layout = dbc.Container([
   utils.app_header('Журнал'),
   html.Div(id='dummy'),
   dbc.Tabs([
       dbc.Tab(html.Div(id='journal-places-my'), label='Мои'),
       dbc.Tab(html.Div(id='journal-places-all'), label='Всего отдела'),
   ], class_name='mt-3 fw-bold'),
   html.Div(utils.app_footer(2), className='mt-auto')
], fluid=True, style={'height': '100dvh'}, class_name='d-flex flex-column')

@callback(
    Output('journal-places-my', 'children'),
    Input('common-store-user_name', 'data'),
)
def journal_update_history(data):
    if not data:
        raise PreventUpdate
    
    result = get_user_places(data['username'])
    if result:
        return [
            html.Div([
                html.Div(html.I(className='bi bi-person-circle display-1 text-primary')),
                html.Div([
                    html.H2(x['place'], className='mb-1 mt-3 fw-bold'),
                    html.P(x['name'], className='mb-1'),
                    html.P(x['dt'], className='mb-3 text-secondary fst-italic'),
                ]),
                html.I(
                    className='bi bi-trash-fill fs-3', 
                    style={'color': 'red', 'cursor': 'pointer'}, 
                    id={'type': 'journal-rmbtn', 'index': x['row_id']}
                )
            ], className='d-flex justify-content-around align-items-center border-bottom border-2') for x in result
        ]
    return []


@callback(
    Output('journal-places-all', 'children'),
    Input('common-store-user_name', 'data'),
)
def journal_update_history_all(data):
    # Этот callback может оставаться как есть или тоже добавить PreventUpdate
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
    return []
    

@callback(
    Output('journal-places-my', 'children', allow_duplicate=True),
    Output('dummy', 'children'),
    Input({'type': 'journal-rmbtn', 'index': ALL}, 'n_clicks'),
    State('common-store-user_name', 'data'),
    prevent_initial_call=True
)
def remove_book(clicks, data):
    if not clicks or not data:
        raise PreventUpdate
    
    # Проверяем, была ли нажата какая-либо кнопка удаления
    if any(clicks):
        # Определяем, какая именно кнопка была нажата
        button_id = ctx.triggered_id
        if button_id:
            row_id = button_id['index']
            remove_place(row_id=row_id)
            result = get_user_places(data['username'])
            if result:
                return [
                    html.Div([
                        html.Div(html.I(className='bi bi-person-circle display-1 text-primary')),
                        html.Div([
                            html.H2(x['place'], className='mb-1 mt-3 fw-bold'),
                            html.P(x['name'], className='mb-1'),
                            html.P(x['dt'], className='mb-3 text-secondary fst-italic'),
                        ]),
                        html.I(
                            className='bi bi-trash-fill fs-3', 
                            style={'color': 'red', 'cursor': 'pointer'}, 
                            id={'type': 'journal-rmbtn', 'index': x['row_id']}
                        )
                    ], className='d-flex justify-content-around align-items-center border-bottom border-2') for x in result
                ],dbc.Alert('Запись удалена', duration=2000)
    return no_update, no_update