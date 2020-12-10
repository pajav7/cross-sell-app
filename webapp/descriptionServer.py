import pandas as pd

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
