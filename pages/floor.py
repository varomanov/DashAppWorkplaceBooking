from dash import register_page, html
import dash_bootstrap_components as dbc
from components import utils

register_page(
    __name__,
    path='/floor'
)

layout = dbc.Container([
   utils.app_header('Этажи'),
   dbc.Accordion([
       dbc.AccordionItem(
            html.Img(src='assets/floor.jpg', style={'width': '100%'}),
            title='План 8 этажа'
       ),
       dbc.AccordionItem(
            html.Img(src='assets/floor2.jpg', style={'width': '100%'}),
            title='План 9 этажа'
       )
   ], class_name='mt-3', always_open=True),
   html.Div(utils.app_footer(3), className='mt-auto')
], fluid=True, style={'height': '100dvh'}, class_name='d-flex flex-column')

