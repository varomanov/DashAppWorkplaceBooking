from dash import Dash, page_container, dcc, html
import dash_bootstrap_components as dbc

app = Dash(
    __name__, 
    use_pages=True, 
    prevent_initial_callbacks=True, 
    external_stylesheets=[dbc.themes.JOURNAL, dbc.icons.BOOTSTRAP]
)

app.layout = dbc.Container([
    dcc.Store(id='common-store-user_name', data={'username': '_'}),
    page_container
], fluid=True, class_name='d-flex flex-column col-md-5 px-0', style={'height': '100dvh', 'backgroundColor': '#fff'})

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(port=8050, host='0.0.0.0')