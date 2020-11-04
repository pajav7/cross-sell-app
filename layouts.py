import dash_core_components as dcc
import dash_html_components as html

layoutrecc = html.Div([
    html.H3('Cross-Sell App'),
    dcc.Input(id='usernameInput', placeholder='uživatelské jméno'),
    html.Button(id='loginButton', children='Přihlásit'),
    html.Div(id='currentUserSessionHistory', children=[], style={'display': 'none'}),
    html.Br(),
    html.Div(id='currentProductIDNumber', children='0', style={'display': 'none'}),
    html.Div(id='recommendationIDs', children=['400002', '400006', '400003'] , style={'display': 'none'}),
    html.Img(id='currentProductImg', alt='0', style={'height':'500px', 'width':'500px'}),
    html.Div(id='productDescription', children='aaaa'),
    html.Br(),
    html.H4('Podobné produkty'),
    html.Img(id='reccImg1', alt = 'reccomendation 1', style={'height':'200px', 'width':'200px', 'margin':'10px'}),
    html.Img(id='reccImg2', alt = 'reccomendation 2', style={'height':'200px', 'width':'200px', 'margin':'10px'}),
    html.Img(id='reccImg3', alt = 'reccomendation 3', style={'height':'200px', 'width':'200px', 'margin':'10px'}),
    html.Br(),
    html.Label(id='infoLabel', children='Info')
])

