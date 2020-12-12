
import pandas as pd
import json

history = {}

historypath = 'historie.json'

def load_histories(path = historypath):
    # nacte soubor s historiemi
    global history
    print("loading history from " + path)
    try:
        with open(path) as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []
    print(history)


def get_user_history(username):
    global history
    # capni sloupec z tabulky a nacti jako list
    try:
        # pokud user existuje, nacti jeho sloupec
        userhistory = history[username]
        return userhistory
    except KeyError:
        return []


def save_history(username, historyList):
    # ulozi historii do souboru
    global history, historypath

    # TODO : predelat na JSON, ne DataFrame

    print(username)
    print(historyList)

    if username == None:
        print('no user logged in, no history saved')
        return

    if username not in history:
        # kdyz to je novy uzivatel tak to pripoj jako novy zaznam
        print('user {} doesn\'t exist, creating new column'.format(username))
        history[username] = historyList

    else:
        print('user {} found, appending to existing history'.format(username))
        history[username] = historyList

    #JSON:{data:{username:Jon, data:product1: "12233", product2: "4566", product3:"654"}, metadata:xXyz}

    with open(historypath, 'w') as f:
       json.dump(history,f)