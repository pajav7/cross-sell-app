import dash_core_components as dcc
import dash_html_components as html

layoutcategories = html.Div(id='layoutCategories', children=[
    html.H3('Doporučené kategorie'),
    html.Div(id='reccCategoryList'),
    html.H3('Všechny kategorie'),
    html.Div(id='allCategoryList')
])

layoutrecc = html.Div(id='layoutRecc', children=[
    dcc.Link('Zpět na všechny kategorie', href='/'),
    html.Br(),
    html.Img(id='currentProductImg', alt='obrazek vybraneho produktu', style={'height':'400px'}),
    html.Div(id='productDescription', children='aaaa'),
    html.Br(),
    html.H4('Doporučené produkty'),
    html.Div(id='reccProductsContent', children=[]),
    html.Br(),
    html.Label(id='infoLabel', children='Info'),
    html.H5('Jiné produkty z této kategorie'),
    html.Div(id='moreProductsContent', children=[]),
    html.Button(id='loadMoreButton', children='Načíst další produkty'),
    html.Br(),
    html.Br(),
    html.Label(children='Manuální zadávání ID produktu'),
    html.Div([
        dcc.Input(id='productIDInput', placeholder='Zadejte ID produktu'),
        html.Button(id='IDSubmitButton', children='OK'),
    ])
])

layout404 = html.Div([
    html.Label(children='Omlouváme se, zde nejsou žádné produkty.'),
    dcc.Link('Zpět na všechny kategorie', href='/')
])

layoutvse = html.Div([
    dcc.Location(id='url', refresh=False),
    html.H2('Cross-Sell App'),
    dcc.Store(id='currentUserSessionHistory', storage_type='memory', data=[]),
    dcc.Store(id='categoriesRecommended', storage_type='memory', data=[]),
    html.Div([
        dcc.Input(id='usernameInput', placeholder='Uživatelské jméno'),
        html.Button(id='loginButton', children='Přihlásit'),
    ]),
    layoutcategories,
    html.Div(id='currentProductIDNumber', children='0', style={'display': 'none'}),
    html.H3(id='categoryHeading', children='Cross-Sell App'),
    layoutrecc
])
