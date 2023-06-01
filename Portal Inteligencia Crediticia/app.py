import flask
import dash
import dash_bootstrap_components as dbc

#server = flask.Flask(__name__)
##dashboard.bind(server)
#app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True)

#app=dash.Dash(__name__, suppress_callback_exceptions=True)
#server=app.server


app = dash.Dash(__name__)
server = app.server
app.config.suppress_callback_exceptions = True