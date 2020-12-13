import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

category_names_path = "../DATA/category/name_key.csv"
category_translations_path = "../DATA/category/reduced_category_key.csv"

category_names = pd.DataFrame()
category_translations = pd.DataFrame()
number_of_categories = 1


def load_categories():
    global category_names, category_translations
    category_names = pd.read_csv(category_names_path)
    category_translations = pd.read_csv(category_translations_path)


def init_all_category_layout():
    global category_names, number_of_categories
    # vygeneruj vyber kategorii
    # pocet radku = pocet kategorii (je jich 72)
    number_of_categories = category_names.shape[0]
    # # vygeneruj mi odkazy na kategorie
    categoryLayout = []
    for index, rows in category_names.iterrows():
        [catID, catName] = [rows.cat_ID, rows.cat_name]
        categoryLayout.append(dcc.Link(id="linkCat_{}".format(catID), children=catName, href="/products/{}".format(catID)))
        categoryLayout.append(html.Br())

    return html.Div(children=categoryLayout)


def get_recc_category_links(reccCategoryIDs):
    # vygeneruj odkazy na doporucene kategorie
    global category_names
    reccCategoryLayoutChildren = []
    #reccCategoryNames = category_names[category_names["cat_ID"].isin(reccCategoryIDs)]["cat_name"]
    for i in range(len(reccCategoryIDs)):
        reccCategoryLayoutChildren.append(
            dcc.Link(id="linkCat_{}".format(reccCategoryIDs[i]),
                     children=category_names[category_names['cat_ID'] == int(reccCategoryIDs[i])].iloc[0, 1],
                     href="/products/{}".format(reccCategoryIDs[i])))
        reccCategoryLayoutChildren.append(html.Br())

    return html.Div(children=reccCategoryLayoutChildren)


def translate_categories(oldCategoryIDsList):
    # prelozi stare ID na nove
    newCatIDs = category_translations[category_translations["categories"].isin(oldCategoryIDsList)]["cat_ID"].tolist()
    newCatIDs = list(map(int, newCatIDs))
    return newCatIDs


def get_category_name(catID):
    return category_names[category_names['cat_ID'] == int(catID)].iloc[0, 1]
