import pandas as pd
from gensim.models import Word2Vec

pretrained_model = None

def load_model():
    # priprav predtrenovany model
    global pretrained_model
    pretrained_model = Word2Vec.load('../w2v_optimal.model')
    print("recommendation model loaded")


def get_product_recc(productIDS, numberOfReccs=5):
    # doporuc neco k tomuto produktu (nebo seznamu produktu)
    global pretrained_model
    print(productIDS)
    try:
        if isinstance(productIDS, list):
            reccsWithSimilarities = pretrained_model.wv.most_similar(positive=productIDS, topn=numberOfReccs) #topn = 5?
        else:
            reccsWithSimilarities = pretrained_model.wv.most_similar(positive=[productIDS], topn=numberOfReccs)
    except KeyError:
        print("error: {} not in vocabulary".format(productIDS))
        reccsWithSimilarities = []

    reccsClean = []

    # ocisti od ratingu
    for recc in reccsWithSimilarities:
        reccsClean.append(recc[0])

    return reccsClean

def get_recc_products_all(productIDS):
    #doporuc top 5 produktu celkem
    global pretrained_model
    numberOfReccs = 5
    if len(productIDS) == 0:
        return []
    else:
        try:
            if isinstance(productIDS, list):
                reccsWithSimilarities = pretrained_model.wv.most_similar(positive=productIDS, topn=numberOfReccs) 
            else:
                reccsWithSimilarities = pretrained_model.wv.most_similar(positive=[productsIDS], topn=numberOfReccs)
        except KeyError:
            print("")
            reccsWithSimilarities = []
        reccsClean = []
        
        for recc in reccsWithSimilarities:
            reccsClean.append(recc[0])
        return reccsClean


