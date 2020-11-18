import dash_core_components as dcc
import dash_html_components as html
import dash
import flask
import os
from dash.dependencies import Input, Output, State

from reccServer import *
from historyServer import *
from app import app
from layouts import layoutrecc

image_directory = 'productImages'
valid_formats = [".jpg"]
# sestav seznam obrazku
list_of_images = []
for f in os.listdir(image_directory):
    ext = os.path.splitext(f)[1]
    if ext.lower() not in valid_formats:
        continue
    list_of_images.append(f)

print('loaded images {}'.format(list_of_images[0:5]))

static_image_route = '/static/'
data_path = "produkty.csv"

load_reccs(data_path)
load_histories()


@app.callback(
    Output('infoLabel', 'children'),
    Output('currentProductIDNumber', 'children'),
    [Input('reccImg1', 'n_clicks'),
    Input('reccImg2', 'n_clicks'),
    Input('reccImg3', 'n_clicks')
    ],
    [State('recommendationIDs', 'children') # jenom precti, nereaguj na jejich zmenu
    ]
)
def get_next_product_click(clicks1, clicks2, clicks3, currentRecommendedIDs):
    # zjisti na ktery obrazek se kliklo a posli to dal, posli ID produktu co se ma ted zobrazit
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'reccImg1' in changed_id:
        newproductID = currentRecommendedIDs[0]
        msg = 'Image 1 was most recently clicked, ID: {}'.format(newproductID)
    elif 'reccImg2' in changed_id:
        newproductID = currentRecommendedIDs[1]
        msg = 'Image 2 was most recently clicked, ID: {}'.format(newproductID)
    elif 'reccImg3' in changed_id:
        newproductID = currentRecommendedIDs[2]
        msg = 'Image 3 was most recently clicked, ID: {}'.format(newproductID)
    else:
        msg = 'None of the images have been clicked yet'
        newproductID = '40001'
    return msg, newproductID


@app.callback(
    Output('recommendationIDs', 'children'),
    Output('productDescription', 'children'),
    Output('currentProductImg', 'src'),
    Output('reccImg1', 'src'),
    Output('reccImg2', 'src'),
    Output('reccImg3', 'src'),
    Output('currentUserSessionHistory', 'children'),
    [Input('currentProductIDNumber', 'children'),
     Input('loginButton', 'n_clicks'),
    ],
    [ State('usernameInput', 'value'),
      State('currentUserSessionHistory', 'children')]
)
def load_next_product(selectedProductID, clicks, oldUsername,  currentSessionHistory):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    # dostan doporuceni k vybranemu produktu, zanes ho do historie a prehazej obrazky
    newRecommendedIDs = get_recc(selectedProductID)
    newDescription = get_name(selectedProductID)
    # zmen podle toho obrazky
    currentImgPath = static_image_route + str(selectedProductID)
    reccImg1Path = static_image_route + str(newRecommendedIDs[0])
    reccImg2Path = static_image_route + str(newRecommendedIDs[1])
    reccImg3Path = static_image_route + str(newRecommendedIDs[2])

    if 'currentProductIDNumber' in changed_id:
        currentSessionHistory.append(str(selectedProductID))
        # uloz historii
        save_history(oldUsername, currentSessionHistory)
    elif 'loginButton' in changed_id:
        # vymaz historii soucasne session v momente kdy se novy uzivatel prihlasi
        currentSessionHistory = []

    return newRecommendedIDs, newDescription, currentImgPath, reccImg1Path, reccImg2Path, reccImg3Path, currentSessionHistory


@app.server.route('{}<image_path>'.format(static_image_route))
def serve_image(image_path):
    # nacteni obrazku z disku
    image_name = '{}.jpg'.format(image_path)
    print('looking up image {}'.format(image_name))
    if image_name not in list_of_images:
        raise Exception('"{}" is excluded from the allowed static files'.format(image_path))
    return flask.send_from_directory(image_directory, image_name)

# nastav rozvrzeni stranky a pridej CSS
app.layout = layoutrecc

if __name__ == '__main__':
    app.run_server(debug=True)