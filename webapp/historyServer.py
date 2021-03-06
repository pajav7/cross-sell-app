
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
        history = {}
    print(history)


def get_user_history(username):
    global history
    # capni sloupec z JSONu a nacti jako list
    try:
        # pokud user existuje, nacti jeho historii
        userhistory = history[username]
        return userhistory
    except KeyError:
        # pokud neexistuje, zaloz novy seznam
        return []


def save_history(username, historyList):
    # ulozi historii do souboru
    global history, historypath

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

    # JSON structure:
    # { username1: [ [pID1, catID1], [pID2, catID2], ... ],
    # username2: [ [pID1, catID1], ... ],
    # ... }

    # TODO otestovat jestli to neustale otevirani souboru nezpomaluje (ugly hack)
    with open(historypath, 'w') as f:
       json.dump(history,f)