from dash import register_page, html
import dash_bootstrap_components as dbc
from components import utils

register_page(
    __name__,
    path='/personal'
)

layout = dbc.Container([
   utils.app_header('КИР'),
   html.Div(utils.app_footer(4), className='mt-auto')
], fluid=True, style={'height': '100vh'}, class_name='d-flex flex-column')

