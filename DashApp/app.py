
import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, suppress_callback_exceptions=True, title='CEA Dashboard', external_stylesheets=[dbc.themes.BOOTSTRAP]) #

server = app.server

app.config.suppress_callback_exceptions = True

caminho = '/'