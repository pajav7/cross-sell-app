import re
import dash
from dash.dependencies import Input, Output, State

from app import app
from categoryBrowser import *
from categoryAndDescriptionServer import *
from historyServer import *
from layouts import *
from reccModel import *


@app.callback(
    Output('infoLabel', 'children'),
    Output('currentProductIDNumber', 'children'),
    [Input('reccImg1', 'n_clicks'),
    Input('reccImg2', 'n_clicks'),
    Input('reccImg3', 'n_clicks'),
    Input('reccImg4', 'n_clicks'),
    Input('reccImg5', 'n_clicks'),
    Input('IDSubmitButton', 'n_clicks')
    ],
    [State('recommendationIDs', 'children'),
     State('productIDInput', 'value')# jenom precti, nereaguj na jejich zmenu
    ]
)
def get_next_product_click(clicks1, clicks2, clicks3, clicks4, clicks5, submitClicks, currentRecommendedIDs, productIDfromInput):
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
    elif 'reccImg4' in changed_id:
        newproductID = currentRecommendedIDs[3]
        msg = 'Image 4 was most recently clicked, ID: {}'.format(newproductID)
    elif 'reccImg5' in changed_id:
        newproductID = currentRecommendedIDs[4]
        msg = 'Image 5 was most recently clicked, ID: {}'.format(newproductID)
    elif 'IDSubmitButton' in changed_id:
        newproductID = productIDfromInput
        msg = 'Submit button clicked. Custom product ID: {}'.format(newproductID)
    else:
        msg = 'None of the images have been clicked yet'
        newproductID = '848128007'
    return msg, newproductID


@app.callback(
    Output('recommendationIDs', 'children'),
    Output('productDescription', 'children'),
    Output('currentUserSessionHistory', 'children'),
    Output('reccLink1', 'href'),
    Output('reccLink2', 'href'),
    Output('reccLink3', 'href'),
    Output('reccLink4', 'href'),
    Output('reccLink5', 'href'),
    Output('reccLink1', 'children'),
    Output('reccLink2', 'children'),
    Output('reccLink3', 'children'),
    Output('reccLink4', 'children'),
    Output('reccLink5', 'children'),
    Output('reccDesc1', 'children'),
    Output('reccDesc2', 'children'),
    Output('reccDesc3', 'children'),
    Output('reccDesc4', 'children'),
    Output('reccDesc5', 'children'),
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
    newRecommendedIDs = check_product_category(get_product_recc(selectedProductID, numberOfReccs=10), currentCategoryID)
    newDescription = get_product_description(selectedProductID)

    # priprav seznamy
    reccURLs = []
    reccDescriptions = []
    for i in range(min(len(newRecommendedIDs), 5)):
        reccURLs.append("http://mall.cz/id/{}".format(newRecommendedIDs[i]))
        reccDescriptions.append(get_product_description(newRecommendedIDs[i]))

    # dopln mista kde jsme nemeli doporuceni
    if(len(newRecommendedIDs) < 5):
        if(len(newRecommendedIDs) == 0):
            newRecommendedIDs.append("")
            reccURLs.append("")
            reccDescriptions.append("K tomuto produktu nemáme vhodná doporučení.")
        for i in range(len(newRecommendedIDs), 5):
            newRecommendedIDs.append("")
            reccURLs.append("")
            reccDescriptions.append("")

    if 'currentProductIDNumber' in changed_id:
        currentSessionHistory.append(str(selectedProductID))
        # uloz historii
        save_history(inputUsername, currentSessionHistory)
    elif 'loginButton' in changed_id:
        # vymaz historii soucasne session v momente kdy se novy uzivatel prihlasi
        currentSessionHistory = get_user_history(inputUsername)

    return newRecommendedIDs, newDescription, currentSessionHistory, \
        reccURLs[0], reccURLs[1], reccURLs[2], reccURLs[3], reccURLs[4], \
        newRecommendedIDs[0], newRecommendedIDs[1], newRecommendedIDs[2], newRecommendedIDs[3], newRecommendedIDs[4], \
        reccDescriptions[0], reccDescriptions[1], reccDescriptions[2], reccDescriptions[3], reccDescriptions[4]


# prevzato z https://dash.plotly.com/urls
@app.callback(Output('pageContent', 'children'),
              Input('url', 'pathname'))
def switch_page(pathname):
    global RE_catID
    if pathname == '/':
         return layoutcategories
    elif bool(re.search(RE_catID, pathname)):
         return layoutrecc
    else:
        return '404'

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

layoutcategories.children[1] = get_recc_category_links(["1","2","23","45"] + translate_categories(["237","118"]))
                                # prelozi se na 237->3, 118->5
layoutcategories.children[3] = init_all_category_layout()

# nastav rozvrzeni stranky a pridej CSS
app.layout = layoutvse

# spust webovku
if __name__ == '__main__':
    app.run_server(debug=True)

