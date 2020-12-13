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
    Output('productDescription', 'children'),
    [Input({'type': 'reccProdImg', 'productID': ALL}, 'n_clicks'),
     Input('IDSubmitButton', 'n_clicks'),
     Input({'type': 'dynamicProdImg', 'productID': ALL}, 'n_clicks')
    ],
    [State({'type': 'reccProdImg', 'productID': ALL}, 'id'),
     State('productIDInput', 'value'),
     State('currentProductIDNumber', 'children'),
     State({'type': 'dynamicProdImg', 'productID': ALL}, 'id')
    ]
)
def get_next_product_click(reccProdClicks, submitClicks, dynamicProdClicks,\
                           reccProdIDs, productIDfromInput, currentProductID, dynamicProdIDs):
    # zjisti na ktery obrazek se kliklo a posli to dal, posli ID produktu co se ma ted zobrazit
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'reccProdImg' in changed_id:
        newProductID = re.findall(r'\d+', changed_id)[0]
        msg = 'Recommended product clicked. ID: {}'.format(newProductID)
    elif 'IDSubmitButton' in changed_id:
        newProductID = productIDfromInput
        msg = 'Submit button clicked. Custom product ID: {}'.format(newProductID)
    elif 'dynamicProdImg' in changed_id:
        newProductID = re.findall(r'\d+', changed_id)[0]
        msg = 'Dynamic product clicked. ID: {}'.format(newProductID)
    else:
        msg = ""
        newProductID = currentProductID

    newDescription = get_product_description(newProductID)
    return msg, newProductID, newDescription


@app.callback(
    Output('currentUserSessionHistory', 'data'),
    Output('categoriesRecommended', 'data'),
    Output('reccProductsContent', 'children'),
    [Input('currentProductIDNumber', 'children'),
     Input('loginButton', 'n_clicks'),
    ],
    [State('usernameInput', 'value'),
     State('currentUserSessionHistory', 'data'),
     State('categoriesRecommended', 'data'),
     State('url', 'pathname')]
)
def populate_recommended_and_update_history(selectedProductID, loginClicks, inputUsername,
                                            currentSessionHistory, currentSessionRecommendedCategories,
                                            currentCategoryURL):
    # zjisti na co se kliklo
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if currentCategoryURL != '/':
        currentCategoryID = re.findall(r'\d+', currentCategoryURL)[0]
    currentSessionRecommendedCategories = set(currentSessionRecommendedCategories)
    newReccProductsComponents = []

    if 'currentProductIDNumber' in changed_id:
        # ugly hack
        # v momente kdy vlezu do kategorie se tento callback spusti
        # (zrejme kvuli tomu ze se znovu generuji vsechny ty komponenty)
        # zmeni se tedy vzdy n_clicks, i kdyz uzivatel na nic nekliknul a nic noveho jeste nevidel
        # (protoze se nam jeste nenacetla nova kategorie)
        # proto pri defaultni hodnote z layoutu nic nedelej
        if selectedProductID != '0':
            # dostan doporuceni k vybranemu produktu

            newRecommendedIDs, newRecommendedCategories = \
                check_product_category(get_product_recc(selectedProductID, numberOfReccs=10), currentCategoryID)

            currentSessionHistory.append([str(selectedProductID), str(currentCategoryID)])
            save_history(inputUsername, currentSessionHistory)
            # pridej nove doporucene kategorie
            currentSessionRecommendedCategories.update(newRecommendedCategories)
            # vygeneruj nam nove komponenty
            newReccProductsComponents = generate_products_recommended(newRecommendedIDs)

    elif 'loginButton' in changed_id:
        # vymaz historii soucasne session v momente kdy se novy uzivatel prihlasi
        currentSessionHistory = get_user_history(inputUsername)
        # vytahni vsechny navstivnene kategorie z historie
        categoriesVisited = set(map(lambda zaznam: zaznam[1], currentSessionHistory))
        currentSessionRecommendedCategories.update(categoriesVisited)
        if currentCategoryURL != '/':
            newRecommendedIDs, newRecommendedCategories = \
                check_product_category(get_product_recc(selectedProductID, numberOfReccs=10), currentCategoryID)
            # nech tam ty stare komponenty
            newReccProductsComponents = generate_products_recommended(newRecommendedIDs)

    currentSessionRecommendedCategories = list(currentSessionRecommendedCategories)
    print("doporucene kategorie pro uzivatele {} : {}".format(inputUsername,currentSessionRecommendedCategories))

    return currentSessionHistory, \
           currentSessionRecommendedCategories, newReccProductsComponents


@app.callback(
    Output('categoryHeading', 'children'),
    Output('layoutCategories', 'style'),
    Output('layoutRecc', 'style'),
    Output('reccCategoryList', 'children'),
    [Input('url', 'pathname'),
     Input('categoriesRecommended', 'data')
     ],
    State('categoriesRecommended', 'data')
)
def switch_page(pathname, categoriesRecommendedListAsInput, categoriesRecommendedListAsState):
    global RE_catID
    if pathname == '/':
        return '', {'display': 'block'}, {'display': 'none'}, get_recc_category_links(categoriesRecommendedListAsState)
    elif bool(re.search(RE_catID, pathname)):
        return get_category_name(re.findall(r'\d+', pathname)[0]), {'display': 'none'}, {'display': 'block'}, ''
    else:
        return 'Čtyřistačtyři', {'display': 'none'}, {'display': 'none'}, layout404


@app.callback(
    Output('moreProductsContent', 'children'),
    Input('loadMoreButton', 'n_clicks'),
    [State('moreProductsContent', 'children'),
     State('url', 'pathname')]
)
def load_more_products(clicks, oldchildren, currentCategoryURL):
    if (currentCategoryURL != '/'):
        return oldchildren + generate_products_from_category(5, re.findall(r'\d+', currentCategoryURL)[0])
    else:
        return []


# nacti vsechno
load_model()
load_names()
load_histories()
load_categories()

RE_catID = re.compile(r'products/\d+')

# priprav uvodni stranku

layoutcategories.children[3] = init_all_category_layout()

# nastav rozvrzeni stranky a pridej CSS
app.layout = layoutvse

# spust webovku
if __name__ == '__main__':
    app.run_server(debug=True)

