import re
import dash
from dash.dependencies import Input, Output, State, ALL, MATCH

from app import app
from categoryBrowser import *
from categoryAndDescriptionServer import *
from historyServer import *
from layouts import *
from reccModel import *


@app.callback(
    Output('infoLabel', 'children'),
    Output('currentProductIDNumber', 'children'),
    [Input({'type': 'reccProdImg', 'productID': ALL}, 'n_clicks'),
     Input('IDSubmitButton', 'n_clicks'),
     Input({'type': 'dynamicProdImg', 'productID': ALL}, 'n_clicks')
    ],
    [State({'type': 'reccProdImg', 'productID': ALL}, 'id'),
     State('productIDInput', 'value'),
     State({'type': 'dynamicProdImg', 'productID': ALL}, 'id')
    ]
)
def get_next_product_click(reccProdClicks, submitClicks, dynamicProdClicks,\
                           reccProdIDs, productIDfromInput, dynamicProdIDs):
    # zjisti na ktery obrazek se kliklo a posli to dal, posli ID produktu co se ma ted zobrazit
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'reccProdImg' in changed_id:
        newproductID = re.findall(r'\d+', changed_id)[0]
        msg = 'Recommended product clicked. ID: {}'.format(newproductID)
    elif 'IDSubmitButton' in changed_id:
        newproductID = productIDfromInput
        msg = 'Submit button clicked. Custom product ID: {}'.format(newproductID)
    elif 'dynamicProdImg' in changed_id:
        newproductID = re.findall(r'\d+', changed_id)[0]
        msg = 'Dynamic product clicked. ID: {}'.format(newproductID)
    else:
        msg = 'None of the images have been clicked yet'
        newproductID = '848128007'
    return msg, newproductID


@app.callback(
    Output('recommendationIDs', 'children'),
    Output('productDescription', 'children'),
    Output('currentUserSessionHistory', 'children'),
    Output('reccProductsContent', 'children'),
    [Input('currentProductIDNumber', 'children'),
     Input('loginButton', 'n_clicks'),
    ],
    [ State('usernameInput', 'value'),
      State('currentUserSessionHistory', 'children'),
      State('url', 'pathname')]
)
def populate_recommended(selectedProductID, clicks, inputUsername, currentSessionHistory, currentCategoryURL):
    # zjisti na co se kliklo
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    # dostan doporuceni k vybranemu produktu
    currentCategoryID = re.findall(r'\d+', currentCategoryURL)[0]
    unfilteredReccs = get_product_recc(selectedProductID, numberOfReccs=10)
    print("unfiltered Reccs: {}".format(unfilteredReccs))
    newRecommendedIDs = check_product_category(unfilteredReccs, currentCategoryID)
    newDescription = get_product_description(selectedProductID)

    if 'currentProductIDNumber' in changed_id:
        currentSessionHistory.append(str(selectedProductID))
        # uloz historii
        save_history(inputUsername, currentSessionHistory)
    elif 'loginButton' in changed_id:
        # vymaz historii soucasne session v momente kdy se novy uzivatel prihlasi
        currentSessionHistory = get_user_history(inputUsername)

    return newRecommendedIDs, newDescription, currentSessionHistory, generate_products_recommended(newRecommendedIDs)


# prevzato z https://dash.plotly.com/urls
@app.callback(Output('pageContent', 'children'),
              Output('categoryHeading', 'children'),
              Input('url', 'pathname'))
def switch_page(pathname):
    global RE_catID
    if pathname == '/':
        return layoutcategories, ''
    elif bool(re.search(RE_catID, pathname)):
        return layoutrecc, get_category_name(re.findall(r'\d+', pathname)[0])
    else:
        return layout404, 'Čtyřistačtyři'


@app.callback(
    Output('moreProductsContent', 'children'),
    Input('loadMoreButton', 'n_clicks'),
    [ State('moreProductsContent', 'children'),
    State('url', 'pathname')]
)
def load_more_products(clicks, oldchildren, currentCategoryURL):
    return oldchildren + generate_products_from_category(5, re.findall(r'\d+', currentCategoryURL)[0])


# nacti vsechno
load_model()
load_names()
load_histories()
load_categories()

RE_catID = re.compile(r'products/\d+')

# priprav uvodni stranku
layoutcategories.children[1] = get_recc_category_links(["1","2","23","45"] + translate_categories(["237","118"]))
                                # prelozi se na 237->3, 118->5
layoutcategories.children[3] = init_all_category_layout()

# nastav rozvrzeni stranky a pridej CSS
app.layout = layoutvse

# spust webovku
if __name__ == '__main__':
    app.run_server(debug=True)

