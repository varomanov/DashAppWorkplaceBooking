from dash import register_page, html, callback, Input, Output, no_update
import dash_bootstrap_components as dbc
from models.models import get_persons

register_page(
    __name__,
    path='/'
)

layout = dbc.Container([
    html.Div(html.Img(src='assets/logo.png', alt='logo', width=250), className='text-center mb-5'),
    dbc.Select(
        id='login-input-username', 
        options=[{'label': ' '.join(['🔒', x['name']]), 'value': x['id']} for x in get_persons()], 
        style={'width': '100%'}, 
        class_name='mb-5',
        placeholder='Ваше имя'
    ),
    dbc.Button('Войти', id='login-btn-enter', disabled=True, color='secondary', href='/booking')
], fluid=True, class_name='d-flex flex-column justify-content-center align-items-center', style={'height': '100vh'})

@callback(
    Output('common-store-user_name', 'data'),
    Output('login-btn-enter', 'color'),
    Output('login-btn-enter', 'disabled'),
    Input('login-input-username', 'value'),
    prevent_initial_call=True
)
def login_button_update(value):
    if value is None:
        return [no_update] * 3
    return {'username': value}, 'primary', False