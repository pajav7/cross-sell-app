# Cross-sell application

This application was created as a university project which aims to simulate a real life business assignement concerning on-line shops.

## General info
Our application is an on-line shop, which in addition recommends various categories and new products for each user based on his/hers particular history. 

Most of the text in the application is in CZECH.

## How does it work

The application returns recommendations based on history of views using Word2vec recommendation engine. 
The web application uses Dash in Python.

## How to use it

In order to obtain your own history of views you need to sign in with your original name.

Then you can view any category and any product you want. When you have selected a category, only products from this particular category will be displayed and recommended. 

After you have gone back to the main page new categories and 5 new products from the whole e-shop will be recommended based on the products and categories you have already visited.

## How can YOU try it?

Unfortunately his application does not run on a webside since the trained recommendation model and the data required for the application are too big. 
This repository does not contain a trained recommendation model either since the files are bigger than 100MB.

However you can see few pictures of the application in the folder: `pictures`.

If you want to run this application withou recommendation model, the required packages in Python 3 are listed in the file requirements.txt
You can use the following commands in Windows using pip:

`$ pip3 install -r requirements.txt`

and then run the application in the folder `webapp` using command:

`$ py index.py`
