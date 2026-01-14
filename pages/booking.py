from dash import register_page, html, callback, Input, Output, State, no_update
import dash_bootstrap_components as dbc
from components import utils
from models.models import get_dates, get_places, book_place

register_page(
    __name__,
    path='/booking'
)

layout = dbc.Container([
   utils.app_header('Бронирование'),
   html.Div([
        html.P('📅 Дата бронирования', className='mt-5 mb-2 ms-1'),
        dbc.Select(
            id='booking-select-date',
            options=[{'label': '✔️'.join(['', x.strftime('%Y-%m-%d')]), 'value': x} for x in get_dates()]
        ),
        html.P('🪧 Место', className='mt-5 mb-2 ms-1'),
        dbc.Select(
            id='booking-select-place',
            options=[{'label': ' '.join(['✔️', x['name']]), 'value': x['id']} for x in get_places()]
        ),
        html.Br(),
        html.Br(),
        html.Hr(),
        html.Div(dbc.Button('Забронировать', id='booking-button-book', disabled=True, color='secondary'), className='text-center mt-5'),
        html.Div(id='boking-alert')
   ]),
   html.Div(utils.app_footer(1), className='mt-auto')
], fluid=True, style={'height': '100dvh'}, class_name='d-flex flex-column')

@callback(
    Output('booking-button-book', 'color'),
    Output('booking-button-book', 'disabled'),
    Input('booking-select-date', 'value'),
    Input('booking-select-place', 'value'),
    prevent_initial_call=True
)
def booking_button_update(date, place):
    if date is None or place is None:
        return [no_update] * 2
         
    return 'primary', False


@callback(
    Output('boking-alert', 'children'),
    Input('booking-button-book', 'n_clicks'),
    Input('booking-select-date', 'value'),
    State('booking-select-place', 'value'),
    State('common-store-user_name', 'data'),
    prevent_initial_call=True    
)
def booking_make_book(clicks, date, place, data):
    if clicks:
        if book_place(date=date, user_id=data['username'], place_id=place):
            return dbc.Alert('Место забронировано успешно!', duration=2000)
    else:
        return no_update
