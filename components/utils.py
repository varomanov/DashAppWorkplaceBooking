from dash import html, dcc
import dash_bootstrap_components as dbc

def app_header(name):
    return dbc.Row([
        dbc.Col(html.I(className='bi bi-person-circle fs-1'), width='auto', align='center'),
        dbc.Col(html.P(name, className='fs-4 fw-bold mb-0 py-2')),
        dbc.Col(dcc.Link(html.I(className='bi bi-box-arrow-right text-light fw-bold fs-3 ms-auto'), href='/'), align='center', width='auto')
    ], class_name='bg-primary text-light')


def app_footer(id=1):
    return dbc.Row([
        dbc.Col(dcc.Link(['Бронь', html.Br(), html.I(className='bi bi-house-fill fs-2')], href='/booking', className=f'{"text-primary" if id==1 else "text-secondary"}'), width='auto', class_name='text-center'),
        dbc.Col(dcc.Link(['Журнал', html.Br(), html.I(className='bi bi-book-fill fs-2')], href='/journal', className=f'{"text-primary" if id==2 else "text-secondary"}'), width='auto', class_name='text-center'),
        dbc.Col(dcc.Link(['Этажи', html.Br(), html.I(className='bi bi-stack fs-2')], href='/floor', className=f'{"text-primary" if id==3 else "text-secondary"}'), width='auto', class_name='text-center'),
        dbc.Col(dcc.Link(['График', html.Br(), html.I(className='bi bi-person-workspace fs-2')], href='/personal', className=f'{"text-primary" if id==4 else "text-secondary"}'), width='auto', class_name='text-center'),
    ], justify='between', align='center', className='footer_div pt-2', style={'borderTop': '2px solid orangered'})