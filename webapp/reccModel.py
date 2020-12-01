import pandas as pd
from gensim.models import Word2Vec

item_names_path = "../DATA/productID_name_category_NotNaN.csv"

pretrained_model = None
item_names = pd.DataFrame()

def load_model():
    # priprav predtrenovany model
    global pretrained_model
    pretrained_model = Word2Vec.load('../w2v.model')
    print("recommendation model loaded")


def load_names():
    # priprav tabulku se jmeny
    global item_names
    print("loading data from " + item_names_path)
    item_names = pd.read_csv(item_names_path)
    print(item_names.head(5))



def get_recc(productIDS):
    # doporuc neco k tomuto produktu (nebo seznamu produktu)
    global pretrained_model
    if isinstance(productIDS, list):
        reccsWithSimilarities = pretrained_model.wv.most_similar(positive=productIDS)
    else:
        reccsWithSimilarities = pretrained_model.wv.most_similar(positive=[productIDS])

    reccsClean = []

    # ocisti od ratingu
    for recc in reccsWithSimilarities:
        reccsClean.append(recc[0])

    return reccsClean


def get_product_description(productID):
    # vytahni z tabulky popis prave zobrazeneho produktu
    global item_names
    # samotny vnitrek vraci boolean masku, tu aplikujeme na item_names
    # a vyplivne to ten radek ve kterem se ID nachazi.
    # pak jeste indexujeme 0,0 - chceme jenom nazev
    product_description = item_names.loc[item_names['product_id'] == int(productID)].iloc[0,1]
    return product_description


def get_most_popular():
    global pretrained_model
