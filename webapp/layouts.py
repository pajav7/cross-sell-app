import dash_core_components as dcc
import dash_html_components as html

layoutrecc = html.Div([
    html.H3('Cross-Sell App'),
    dcc.Input(id='usernameInput', placeholder='Uživatelské jméno'),
    html.Button(id='loginButton', children='Přihlásit'),
    html.Div(id='currentUserSessionHistory', children=[], style={'display': 'none'}),
    html.Br(),
    html.Div(id='currentProductIDNumber', children='0'),
    html.Div(id='recommendationIDs', children=["1709503", "2401410", "848128007"] ),
    html.Img(id='currentProductImg', alt='0', style={'height':'500px', 'width':'500px'}),
    html.Div(id='productDescription', children='aaaa'),
    html.Br(),
    html.H4('Podobné produkty'),
    html.Div(id='reccBox1', children=[
        html.Img(id='reccImg1', alt = 'reccomendation 1', style={'height':'200px', 'width':'200px', 'margin':'10px'}),
        html.A(id='reccLink1', href='', children='link 1'),
        html.Div(id='reccDesc1', children='')]),
    html.Div(id='reccBox2', children=[
        html.Img(id='reccImg2', alt = 'reccomendation 2', style={'height':'200px', 'width':'200px', 'margin':'10px'}),
        html.A(id='reccLink2', href='', children='link 2'),
        html.Div(id='reccDesc2', children='')]),
    html.Div(id='reccBox3', children=[
        html.Img(id='reccImg3', alt='reccomendation 3', style={'height': '200px', 'width': '200px', 'margin': '10px'}),
        html.A(id='reccLink3', href='', children='link 3'),
        html.Div(id='reccDesc3', children='')]),
    html.Div(id='reccBox4', children=[
        html.Img(id='reccImg4', alt='reccomendation 4', style={'height': '200px', 'width': '200px', 'margin': '10px'}),
        html.A(id='reccLink4', href='', children='link 4'),
        html.Div(id='reccDesc4', children='')]),
    html.Div(id='reccBox5', children=[
        html.Img(id='reccImg5', alt='reccomendation 5', style={'height': '200px', 'width': '200px', 'margin': '10px'}),
        html.A(id='reccLink5', href='', children='link 5'),
        html.Div(id='reccDesc5', children='')]),

    html.Br(),
    html.Label(id='infoLabel', children='Info')
])

