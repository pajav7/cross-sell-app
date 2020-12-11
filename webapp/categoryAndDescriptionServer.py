import pandas as pd
import dash_html_components as html
import dash_core_components as dcc

item_names_path = "../DATA/product_category_name_sorted.csv"
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
    # samotny vnitrek vraci boolean masku, tu aplikujeme na item_names
    # a vyplivne to ten radek ve kterem se ID nachazi.
    # pak jeste indexujeme 0,0 - chceme jenom nazev
    product_description = item_names.loc[item_names['product_id'] == int(productID)].iloc[0, 2]
    return product_description


def check_product_category(productIDs, categoryID):
    global item_names

    minidf = item_names[item_names['product_id'].isin(productIDs)]
    productsFromCategoryIDs = []
    try:
        for pID in productIDs:
            # zkontroluj jestli jsou doporucene produkty z teto kategorie
            foundCatID = minidf.loc[minidf['product_id'] == pID].iloc[0, 1]
            if(foundCatID == categoryID):
                productsFromCategoryIDs.append(pID)
            else:
                continue
    except IndexError:
        print("no products in {} are from category {}".format(productIDs, categoryID))
        print("returning {}".format(productsFromCategoryIDs))

    return productsFromCategoryIDs


def generate_products_from_category(N_products, categoryID):
    # vraci Div s novymi produkty a knofliky
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
            id={'type':'dynamicProdImg', 'productID':int(samples.iloc[i, 0])}, alt='obrázek produktu {}'.format(samples.iloc[i, 0]),
                 style={'height': '200px', 'width': '200px', 'margin': '10px'}))
        divchildren.append(html.Div(children=[
            html.A(id='reccLink{}'.format(samples.iloc[i, 0]), href=productURLs[i], children=samples.iloc[i, 0]),
            html.Div(id='reccDesc{}', children=productDescriptions[i])
            ]))

    return divchildren
