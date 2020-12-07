import pandas as pd
from gensim.models import Word2Vec

pretrained_model = None


def load_model():
    # priprav predtrenovany model
    global pretrained_model
    pretrained_model = Word2Vec.load('../w2vAllMin5.model')
    print("recommendation model loaded")


def get_product_recc(productIDS, numberOfReccs=5):
    # doporuc neco k tomuto produktu (nebo seznamu produktu)
    global pretrained_model
    if isinstance(productIDS, list):
        reccsWithSimilarities = pretrained_model.wv.most_similar(positive=productIDS, topn=numberOfReccs) #topn = 5?
    else:
        reccsWithSimilarities = pretrained_model.wv.most_similar(positive=[productIDS], topn=numberOfReccs)

    reccsClean = []

    # ocisti od ratingu
    for recc in reccsWithSimilarities:
        reccsClean.append(recc[0])

    return reccsClean


def get_category_recc(productIDS):

    return



