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
    Output('currentProductImg', 'src'),
    [Input({'type': 'reccProdImg', 'productID': ALL}, 'n_clicks'),
     Input('IDSubmitButton', 'n_clicks'),
     Input({'type': 'dynamicProdImg', 'productID': ALL}, 'n_clicks'),
     Input('url','pathname')
    ],
    [State({'type': 'reccProdImg', 'productID': ALL}, 'id'),
     State('productIDInput', 'value'),
     State('currentProductIDNumber', 'children'),
     State({'type': 'dynamicProdImg', 'productID': ALL}, 'id')
    ]
)
def get_next_product_click(reccProdClicks, submitClicks, dynamicProdClicks, currentPageURL,\
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

    newDescription, newImageURL = get_product_description(newProductID)
    return msg, newProductID, newDescription, newImageURL


@app.callback(
    Output('currentUserSessionHistory', 'data'),
    Output('categoriesRecommended', 'data'),
    Output('reccProductsContent', 'children'),
    Output('historyLink', 'style'),
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
                                            currentURL):
    # zjisti na co se kliklo
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if currentURL != '/' and currentURL != '/history':
        currentCategoryID = re.findall(r'\d+', currentURL)[0]
    currentSessionRecommendedCategories = set(currentSessionRecommendedCategories)
    newReccProductsComponents = []
    IDSforRecommendation = []

    # vytahni posledni 3 navstivene produkty pro doporuceni
    if len(currentSessionHistory) != 0:
        for i in range(min(len(currentSessionHistory), 3)):
            IDSforRecommendation.append(currentSessionHistory[-i-1][0])
    else:
        IDSforRecommendation = selectedProductID

    if 'currentProductIDNumber' in changed_id:
        if selectedProductID != '0' and currentURL != '/' and currentURL != '/history':
            # dostan doporuceni k vybranemu produktu

            newRecommendedIDs, newRecommendedCategories = \
                check_product_category(get_product_recc(IDSforRecommendation, numberOfReccs=10), currentCategoryID)

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
        currentSessionRecommendedCategories = categoriesVisited
        if currentURL != '/' and currentURL != '/history':
            newRecommendedIDs, newRecommendedCategories = \
                check_product_category(get_product_recc(IDSforRecommendation, numberOfReccs=10), currentCategoryID)
            # nech tam ty stare komponenty
            newReccProductsComponents = generate_products_recommended(newRecommendedIDs)

    currentSessionRecommendedCategories = list(currentSessionRecommendedCategories)
    print("doporucene kategorie pro uzivatele {} : {}".format(inputUsername,currentSessionRecommendedCategories))

    # zobraz link na historii?
    if inputUsername is not None and inputUsername.isalnum():
        print("user {} logged in, display link to history".format(inputUsername))
        historyLinkStyle = {'display': 'flex'}
    else:
        historyLinkStyle = {'display': 'none'}

    return currentSessionHistory, \
           currentSessionRecommendedCategories, newReccProductsComponents, \
           historyLinkStyle


@app.callback(
    Output('categoryHeading', 'children'),
    Output('layoutCategories', 'style'),
    Output('layoutRecc', 'style'),
    Output('layoutHistory', 'style'),
    Output('reccCategoryList', 'children'),
    Output('historyDisplay', 'children'),
    Output('layoutProductsAll', 'style'),
    Output('productsRecAll', 'children'),
    [Input('url', 'pathname'),
     Input('categoriesRecommended', 'data')
     ],
    [State('categoriesRecommended', 'data'),
     State('usernameInput', 'value'),
     State('currentUserSessionHistory', 'data')]
)
def switch_page(pathname, categoriesRecommendedListAsInput, categoriesRecommendedListAsState, inputUsername, userHistoryList):
    global RE_catID
    if pathname == '/':
        recommendToIDS = [x[0] for x in userHistoryList]
        return '', {'display': 'block'}, {'display': 'none'}, {'display': 'none'}, get_recc_category_links(categoriesRecommendedListAsState), '',{'display': 'block'}, generate_products_recommended_All(get_recc_products_all(recommendToIDS))
    elif pathname == '/history':
        return '', {'display': 'none'}, {'display': 'none'}, {'display': 'block'}, '', generate_products_from_history(inputUsername, userHistoryList), {'display': 'none'}, ''
    elif bool(re.search(RE_catID, pathname)):
        return get_category_name(re.findall(r'\d+', pathname)[0]), {'display': 'none'}, {'display': 'block'}, {'display': 'none'}, '', '', {'display': 'none'}, ''
    else:
        return 'Čtyřistačtyři', {'display': 'none'}, {'display': 'none'}, {'display': 'block'}, '', layout404, {'display': 'none'}, ''


@app.callback(
    Output('moreProductsContent', 'children'),
    [Input('loadMoreButton', 'n_clicks'),
     Input('url','pathname')
    ],
    [State('moreProductsContent', 'children'),
     State('url', 'pathname')]
)
def load_more_products(clicks, currentPageURLAsInput, oldchildren, currentPageURLAsState):
    if (currentPageURLAsState != '/' and currentPageURLAsState != '/history'):
        return oldchildren + generate_products_from_category(5, re.findall(r'\d+', currentPageURLAsState)[0])
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

