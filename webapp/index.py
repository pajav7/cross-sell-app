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
        msg = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        newProductID = currentProductID

    return msg, newProductID


@app.callback(
    Output('recommendationIDs', 'children'),
    Output('productDescription', 'children'),
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

    # dostan doporuceni k vybranemu produktu
    currentCategoryID = re.findall(r'\d+', currentCategoryURL)[0]
    newRecommendedIDs, newRecommendedCategories = \
        check_product_category(get_product_recc(selectedProductID, numberOfReccs=10), currentCategoryID)
    newDescription = get_product_description(selectedProductID)

    if 'currentProductIDNumber' in changed_id:
        if selectedProductID != '0':
            # ugly hack
            # v momente kdy vlezu do kategorie se tento callback spusti
            # (zrejme kvuli tomu ze se znovu generuji vsechny ty komponenty)
            # zmeni se tedy vzdy n_clicks, i kdyz uzivatel na nic nekliknul a nic noveho jeste nevidel
            # (protoze se nam jeste nenacetla nova kategorie)
            # proto pri defaultni hodnote z layoutu nic nedelej
            currentSessionHistory.append([str(selectedProductID),str(currentCategoryID)])
            # uloz historii
            save_history(inputUsername, currentSessionHistory)
    elif 'loginButton' in changed_id:
        # vymaz historii soucasne session v momente kdy se novy uzivatel prihlasi
        currentSessionHistory = get_user_history(inputUsername)

    # pridej nove doporucene kategorie
    currentSessionRecommendedCategories = set(currentSessionRecommendedCategories)
    currentSessionRecommendedCategories.update(newRecommendedCategories)
    currentSessionRecommendedCategories = list(currentSessionRecommendedCategories)

    return newRecommendedIDs, newDescription, currentSessionHistory, \
           currentSessionRecommendedCategories, generate_products_recommended(newRecommendedIDs)


@app.callback(
    Output('pageContent', 'children'),
    Output('categoryHeading', 'children'),
    Input('url', 'pathname'),
    State('categoriesRecommended', 'data')
)
def switch_page(pathname, categoriesRecommendedList):
    global RE_catID
    if pathname == '/':
        layoutcategories.children[1] = get_recc_category_links(categoriesRecommendedList)
        return layoutcategories, ''
    elif bool(re.search(RE_catID, pathname)):
        return layoutrecc, get_category_name(re.findall(r'\d+', pathname)[0])
    else:
        return layout404, 'Čtyřistačtyři'


@app.callback(
    Output('moreProductsContent', 'children'),
    Input('loadMoreButton', 'n_clicks'),
    [State('moreProductsContent', 'children'),
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

