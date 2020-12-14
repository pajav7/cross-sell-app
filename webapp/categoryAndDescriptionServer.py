import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
from categoryBrowser import get_category_name

item_names_path = "../DATA/product_category_name_url_optimal_model_sorted.csv"
item_names = pd.DataFrame()


def load_names():
    # priprav tabulku se jmeny
    global item_names
    print("loading data from " + item_names_path)
    item_names = pd.read_csv(item_names_path)
    print(item_names.head(5))


def get_product_description(productID):
    # vytahni z tabulky popis prave zobrazeneho produktu
    global item_names
    try:
        productDescription = item_names.loc[item_names['product_id'] == int(productID)].iloc[0, 2]
        productImageURL = item_names.loc[item_names['product_id'] == int(productID)].iloc[0, 3]
    except (IndexError, TypeError) as e:
        productDescription = "K tomuto produktu neexistuje popis."
        productImageURL = ''
    return productDescription, productImageURL


def check_product_category(productIDs, categoryID):
    global item_names

    minidf = item_names[item_names['product_id'].isin(productIDs)]
    productsFromCategoryIDs = []
    categoryRecommendedSet = {str(categoryID)}
    for pID in productIDs:
        try:
            # zkontroluj jestli jsou doporucene produkty z teto kategorie
            foundCatID = minidf.loc[minidf['product_id'] == int(pID)].iloc[0, 1]
            if(int(foundCatID) == int(categoryID)):
                productsFromCategoryIDs.append(pID)
            else:
                #print("product {} is not from category {}".format(pID, categoryID))
                categoryRecommendedSet.add(str(foundCatID))
        except IndexError:
            print("indexerror: product {} is not from category {}".format(pID, categoryID))

    return productsFromCategoryIDs, categoryRecommendedSet


def generate_products_recommended(productIDs):
    # vraci Div s novymi produkty (cast "doporucene produkty")
    global item_names

    if(len(productIDs) == 0):
        return "K tomuto produktu/historii bohužel nemáme doporučení z této kategorie."

    productIDsDF = item_names[item_names['product_id'].isin(productIDs)]

    # priprav seznamy
    numberOfRecommendations = min(len(productIDs), 5)
    productURLs = []
    productDescriptions = []
    for i in range(numberOfRecommendations):
        productURLs.append("http://mall.cz/id/{}".format(productIDsDF.iloc[i, 0]))
        productDescriptions.append(productIDsDF.iloc[i, 2])

    # vygeneruj komponenty
    divchildren = []
    for i in range(numberOfRecommendations):
        divchildren.append(html.Img(
            id={'type': 'reccProdImg', 'productID': int(productIDsDF.iloc[i, 0])},
            alt='obrázek produktu {}'.format(productIDsDF.iloc[i, 0]),
            src=productIDsDF.iloc[i,3],
            style={'height': '200px', 'margin': '10px'}))
        divchildren.append(html.Div(children=[
            html.A(id='reccLink{}'.format(productIDsDF.iloc[i, 0]), href=productURLs[i], children=productIDsDF.iloc[i, 0]),
            html.Div(id='reccDesc{}', children=productDescriptions[i])
        ]))

    return divchildren


def generate_products_from_category(N_products, categoryID):
    # vraci Div s novymi produkty (cast "jine z teto kategorie")
    samples = item_names[item_names['cat_ID'] == int(categoryID)].sample(N_products)

    # priprav seznamy
    productURLs = []
    productDescriptions = []
    for i in range(N_products):
        productURLs.append("http://mall.cz/id/{}".format(samples.iloc[i, 0]))
        productDescriptions.append(samples.iloc[i, 2])

    # vygeneruj komponenty
    divchildren = []
    for i in range(N_products):
        divchildren.append(html.Img(
            id={'type':'dynamicProdImg', 'productID':int(samples.iloc[i, 0])},
            alt='obrázek produktu {}'.format(samples.iloc[i, 0]),
            src=samples.iloc[i, 3],
            style={'height': '200px', 'margin': '10px'}))
        divchildren.append(html.Div(children=[
            html.A(id='dynLink{}'.format(samples.iloc[i, 0]), href=productURLs[i], children=samples.iloc[i, 0]),
            html.Div(id='dynDesc{}', children=productDescriptions[i])
            ]))

    return divchildren


def generate_products_from_history(inputUsername, userHistoryList):
    # vraci Div s novymi produkty (cast "doporucene produkty")
    global item_names

    historyLength = len(userHistoryList)

    if inputUsername is None or not inputUsername.isalnum() or historyLength == 0:
        return "Tento uživatel nemá žádnou historii."

    # vytahni co bylo navstiveno, nejnovejsi prvni (proto reverse())
    productsVisited = list(map(lambda zaznam : zaznam[0], userHistoryList))
    categoriesVisited = list(map(lambda zaznam : zaznam[1], userHistoryList))
    productsVisited.reverse()
    categoriesVisited.reverse()

    # vyrez tabulky
    productIDsDF = item_names[item_names['product_id'].isin(productsVisited)]

    # priprav seznamy
    productURLs = []
    productDescriptions = []
    productImageURLs = []
    for i in range(historyLength):
        productURLs.append("http://mall.cz/id/{}".format(productsVisited[i]))
        productDescriptions.append("{}, kategorie: {} - {}".format(
            productIDsDF[productIDsDF['product_id']==int(productsVisited[i])].iloc[0, 2],
            categoriesVisited[i], get_category_name(categoriesVisited[i])))
        productImageURLs.append(
            productIDsDF[productIDsDF['product_id'] == int(productsVisited[i])].iloc[0, 3]
        )

    # vygeneruj komponenty
    divchildren = []
    for i in range(historyLength):
        divchildren.append(html.Img(
            id={'type': 'historyProdImg', 'productID': int(productsVisited[i])},
            alt='obrázek produktu {}'.format(productsVisited[i]),
            src=productImageURLs[i],
            style={'height': '200px', 'margin': '10px'}))
        divchildren.append(html.Div(children=[
            html.A(id='historyLink{}'.format(productsVisited[i]), href=productURLs[i], children=productsVisited[i]),
            html.Div(id='historyDesc{}', children=productDescriptions[i])
        ]))

    return divchildren
