import dash

# test: pridej nejake to CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, title='Cross-Sell App', external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
server = app.server
