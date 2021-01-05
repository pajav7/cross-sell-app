#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re  # For preprocessing
from time import time  # To time our operations
from collections import defaultdict  # For word frequency
import pandas as pd
import os
#os.listdir()
#print(os.listdir("Data/"))#Contents of the Data folder

import logging  # Setting up the loggings to monitor gensim
logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt= '%H:%M:%S', level=logging.INFO)


# In[2]:


#dataFile = "Data/product_views_unified.csv"
# helios path to file
dataFile = "../../../DAS/product_views_unified.csv"

number_rows = 30000000
data_2020 = pd.read_csv(dataFile,nrows=number_rows)
print(data_2020)


# In[3]:


data_2020['product_id'] = data_2020.loc[:,'product_id'].map(str)
print(data_2020)


# In[4]:


sentences = data_2020.groupby('user_id_anon')['product_id'].apply(list)
print(sentences)


# In[36]:


# most_viewed_element = data_2020["product_id"].value_counts().idxmax()
# print(most_viewed_element)


# In[5]:


import multiprocessing

from gensim.models import Word2Vec
import numpy as np

cores = multiprocessing.cpu_count() # Count the number of cores in a computer

# w2v_model = Word2Vec(min_count=10,
#                      window=2,
#                      size=300,
#                      sample=6e-5, 
#                      alpha=0.05, 
#                      min_alpha=0.001, 
#                      negative=20,
#                      workers=cores-1)


# In[24]:


#dataFile = "Data/product_views_unified.csv"
test_rows = 31502086 - number_rows
test_data = pd.read_csv(dataFile,names=["user_id_anon","product_id"],skiprows=number_rows,nrows=test_rows)
test_data['product_id'] = test_data.loc[:,'product_id'].map(str)
test_set = test_data.groupby('user_id_anon')['product_id'].apply(list)
print(test_set)


# In[32]:


import itertools

parm_dict = {'size':(200,250,300),'window':(2,4,5),'alpha':(0.35,0.03,0.025,0.02)}

import ray


def cust_param_search(parm_dict,sentences,test_set):
    score_best, parm_best = 0,()
   
    size, window, alpha = [tup for k,tup in parm_dict.items()] # Individual parm tuples

    parm_combo = list(itertools.product(size, window, alpha)) # Create all combinations
    score = []
    firstIteration = 1
    test_set_in_vocab = []
    num_history = 5
    num_recommend = 20
    
    ray.init(num_cpus=16)
    for parms in parm_combo:
        s, w, a = parms
        print("Trying parameters:")
        print (parms)
        model = Word2Vec(min_count=20,
                         window=w,
                         size=s,
                         alpha=a,
                         workers=cores-1)
        model.build_vocab(sentences, progress_per=5000)
        model.train(sentences, total_examples=model.corpus_count, epochs=30, report_delay=1)
        model.init_sims(replace=True)
        
        precision = []
        if firstIteration == 1: #upraveni test setu (neobsahuje slova co nejsou ve slovníku + jsou dlouhý alespoň num_history+1)
            print("It is first iteration")
#             print(len(test_set))
            firstIteration = 0
            for i in test_set:
                test = i
                k=0
                while k < len(test):
                        if test[k] not in model.wv.vocab or (test[k] in test[:k]):
                            test.pop(k)
                        else:
                            k=k+1
                if (len(test) > num_history + num_recommend):
                    test_set_in_vocab.append(test[:num_history+num_recommend])
            print("Length of test set:")
            print(len(test_set_in_vocab))
        
        for t in test_set_in_vocab: #SCORE FUNCTION pro nejvíce viděný produkt oproti všem ostatním      
            vector = model.wv.most_similar(positive=t[:num_history],topn=num_recommend)
            vector = [l for (l,n) in vector]
            num = 0
            prec = 0
            for l in range(num_recommend):
                if t[l+num_history] in vector:
                    num = num + 1
                    prec = prec + num / (l+1)
#                         print("true positive")
            precision.append(prec / num_recommend)
        
        score.append(sum(precision)/len(precision)) #MEAN AVERAGE PRECISION scoring function
        print(parms)
        print(score[len(score)-1])

        if score[len(score)-1] > score_best:
            score_best = score[len(score)-1]
            parm_best = parms   
            print("This is best score so far.")
            model.save("w2v_optimal.model")
            
    print("Best score -",score_best, "Best parms - ",parm_best)
    print(score)
    ray.shutdown()


# In[33]:


cust_param_search(parm_dict,sentences,test_set)


# In[39]:


#S JINOU SCORING FUNKCI

# import itertools

# parm_dict = {'size':(100,200,300),'window':(2,5),'min_count':(5,10),'alpha':(0.03,0.02,0.01)}

# def cust_param_search(parm_dict,sentences,test_set,most_viewed_element):
#     score_best, parm_best = 0,()
   
#     size,window, min_count, alpha = [tup for k,tup in parm_dict.items()] # Individual parm tuples

#     parm_combo = list(itertools.product(size,window, min_count, alpha)) # Create all combinations

#     for parms in parm_combo:
#         s, w, m, a = parms
#         print (parms)
#         model = Word2Vec(min_count=m,
#                          window=w,
#                          size=s,
#                          alpha=a,
#                          workers=cores-1)
#         model.build_vocab(sentences, progress_per=5000)
#         model.train(sentences, total_examples=model.corpus_count, epochs=10, report_delay=1)

#         model.init_sims(replace=True)
#         similarity = []
#         for i in test_set: #SCORE FUNCTION pro nejvíce viděný produkt oproti všem ostatním
#             simil = []
#             for j in i:
#                 if j in model.wv.vocab and j != most_viewed_element:
# #                     print(model.wv.similarity(most_viewed_element,j))
#                     simil.append(model.wv.similarity(most_viewed_element,j))
#             if len(simil)>0:
#                 similarity.append(sum(simil)/len(simil))
        
#         score = sum(similarity)/len(similarity)
#         print(score)

#         if score > score_best:
#             score_best = score
#             parm_best = parms          
#     print("Best score -",score_best, "Best parms - ",parm_best)


# In[16]:


# model = Word2Vec(min_count=5,
#                  window=5,
#                  size=200,
#                  alpha=0.025,
#                  workers=cores-1)
# model.build_vocab(sentences, progress_per=5000)
# model.train(sentences, total_examples=model.corpus_count, epochs=20, report_delay=1)

# model.init_sims(replace=True)
# precision = []
# for i in test_set: #SCORE FUNCTION pro nejvíce viděný produkt oproti všem ostatním
#     test = i
#     k=0
#     num_history = 5
#     while k < len(test):
#             if test[k] not in model.wv.vocab:
#                 test.pop(k)
#             else:
#                 k=k+1
#     if len(test) > num_history:        
#         vector = model.wv.most_similar(positive=test[:num_history],topn=len(test)-num_history)
#         vector = [l for (l,n) in vector]
#         num = 0
#         for l in range(len(vector)):
#             if vector[l] in test[num_history:]:
#                 num = num + 1
#                 print("true positive")
#                 print("position " + str(l) + " of " + str(len(vector)) + " positions")
#         precision.append(num / (len(test)-num_history))
# #         print(precision)

# score = sum(precision)/len(precision)
# print(score)


# In[26]:


# cust_param_search(parm_dict,sentences,test_set,most_viewed_element)


# In[ ]:




