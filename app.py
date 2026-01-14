from dash import Dash, page_container, dcc, html
import dash_bootstrap_components as dbc
from flask import jsonify

app = Dash(
    __name__, 
    use_pages=True, 
    prevent_initial_callbacks=True, 
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.COSMO, dbc.icons.BOOTSTRAP]
)

# Добавьте healthcheck endpoint
@app.server.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200


app.layout = dbc.Container([
    dcc.Store(id='common-store-user_name', data={'username': 0}),
    page_container
], fluid=True, class_name='d-flex flex-column col-md-5 px-0', style={'height': '100dvh', 'backgroundColor': '#fff'})

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(port=8050, host='0.0.0.0')