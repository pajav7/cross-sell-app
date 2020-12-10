import dash_core_components as dcc
import dash_html_components as html

layoutvse = html.Div([
    dcc.Location(id='url', refresh=False),
    html.H2('Cross-Sell App'),
    html.Div([
        dcc.Input(id='usernameInput', placeholder='Uživatelské jméno'),
        html.Button(id='loginButton', children='Přihlásit'),
    ]),
    html.Div(id='pageContent')
])


layoutcategories = html.Div([
    html.H3('Doporučené kategorie'),
    html.Div(id='reccCategoryList'),
    html.H3('Všechny kategorie'),
    html.Div(id='allCategoryList')
])


layoutrecc = html.Div([
    html.H3('Cross-Sell App'),
    dcc.Link('Zpět na všechny kategorie', href='/'),
    html.Div([
        dcc.Input(id='productIDInput', placeholder='Zadejte ID produktu'),
        html.Button(id='IDSubmitButton', children='OK'),
    ]),
    html.Div(id='currentUserSessionHistory', children=[], style={'display': 'none'}),
    html.Br(),
    html.Div(id='currentProductIDNumber', children='0'),
    html.Div(id='recommendationIDs', children=[],  style={'display': 'none'}),
    html.Img(id='currentProductImg', alt='obrazek vybraneho produktu', style={'height':'500px', 'width':'500px'}),
    html.Div(id='productDescription', children='aaaa'),
    html.Br(),
    html.H4('Podobné produkty'),
    html.Div(id='reccBox1', children=[
        html.Img(id='reccImg1', alt = 'obrazek doporuceni 1', style={'height':'200px', 'width':'200px', 'margin':'10px'}),
        html.Div(children=[
            html.A(id='reccLink1', href='', children='link 1'),
            html.Div(id='reccDesc1', children=''),
        ]),
    ]),
    html.Br(),
    html.Div(id='reccBox2', children=[
        html.Img(id='reccImg2', alt = 'obrazek doporuceni  2', style={'height':'200px', 'width':'200px', 'margin':'10px'}),
        html.Div(children=[
            html.A(id='reccLink2', href='', children='link 2'),
            html.Div(id='reccDesc2', children=''),
        ]),
    ]),
    html.Br(),
    html.Div(id='reccBox3', children=[
        html.Img(id='reccImg3', alt='obrazek doporuceni 3', style={'height': '200px', 'width': '200px', 'margin': '10px'}),
        html.Div(children=[
            html.A(id='reccLink3', href='', children='link 3'),
            html.Div(id='reccDesc3', children=''),
        ]),
    ]),
    html.Br(),
    html.Div(id='reccBox4', children=[
        html.Img(id='reccImg4', alt='obrazek doporuceni 4', style={'height': '200px', 'width': '200px', 'margin': '10px'}),
        html.Div(children=[
            html.A(id='reccLink4', href='', children='link 4'),
            html.Div(id='reccDesc4', children='')
        ]),
    ]),
    html.Br(),
    html.Div(id='reccBox5', children=[
        html.Img(id='reccImg5', alt='obrazek doporuceni 5', style={'height': '200px', 'width': '200px', 'margin': '10px'}),
        html.Div(children=[
            html.A(id='reccLink5', href='', children='link 5'),
            html.Div(id='reccDesc5', children='')
        ]),
    ]),
    html.Br(),
    html.Label(id='infoLabel', children='Info')
])

