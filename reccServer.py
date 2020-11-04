
import pandas as pd

#data_path = "produkty.csv"

data = pd.DataFrame()

def load_reccs(path):
    global data
    print("loading data from " + path)
    data = pd.read_csv(path)
    print(data.head(5))

def get_recc(product_ID):
    # vytahni radek doporuceni z tabulky
    global data
    print("getting recommendation for product {}".format(product_ID))
    recc = data.loc[data["ID"]==int(product_ID)].stack().tolist()[1:4]
    print("recommendation: {}".format( recc))
    return recc

def get_name(product_ID):
    # vytahni jmeno prave zobrazeneho produktu
    global data
    name = data.loc[data["ID"]==int(product_ID)]['Název']
    print("product: {}, name: {}".format(product_ID, name))
    return name


