import pandas as pd
from gensim.models import Word2Vec

item_names_path = "../DATA/item_list.csv"

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
    # hledej v tom jako ve stringu (mozna bude pomale)
    # jediny zpusob jak najit cislo produktu v arrayich ktere jsou v druhem sloupci tabulky item_list.csv
    # samotny vnitrek vraci boolean masku, tu aplikujeme na item_names
    # a vyplivne to ten radek ve kterem se ID nachazi.
    # pak jeste indexujeme 0,0 - chceme jenom nazev
    product_description = item_names[item_names['list_id'].str.contains(productID)].iloc[0, 0]
    # print("description of product {} : \n {}".format(productID, product_description))
    return product_description


def get_most_popular():
    global pretrained_model
