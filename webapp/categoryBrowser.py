import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

category_names_path = "../DATA/category/name_key.csv"
category_names = pd.DataFrame()
number_of_categories = 1

def load_categories():
    global category_names
    category_names = pd.read_csv(category_names_path)

def init_category_layout():
    global category_names, number_of_categories
    # vygeneruj vyber kategorii
    # pocet radku = pocet kategorii (72)
    number_of_categories = category_names.shape[0]
    # # vygeneruj mi odkazy na kategorie
    categoryLayout = []
    for index, rows in category_names.iterrows():
        [catID, catName] = [rows.cat_ID, rows.cat_name]
        categoryLayout.append(dcc.Link(children=catName, href="/products/{}".format(catID)))
        categoryLayout.append(html.Br())

    return html.Div(children=categoryLayout)