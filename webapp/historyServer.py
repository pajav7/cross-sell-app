
import pandas as pd

history = pd.DataFrame()

historypath = 'historie.csv'

def load_histories(path = historypath):
    # nacte soubor s historiemi
    global history
    print("loading history from " + path)
    try:
        history = pd.read_csv(path)
    except FileNotFoundError:
        history = pd.DataFrame()
    print(history.head(5))


def get_user_history(username):
    global history
    try:
        # pokud user existuje, nacti jeho sloupec
        userhistory = history[username]
        userhistory = userhistory.dropna()
        return userhistory
    except KeyError:
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
        # kdyz to je novy uzivatel tak to pripoj jako novy sloupec
        print('user {} doesn\'t exist, creating new column'.format(username))
        userhistorydf = pd.DataFrame({username: historyList})
        history = pd.concat([history, userhistorydf], axis=1)
    else:
        print('user {} found, appending to existing history'.format(username))
        userhistorydf = pd.DataFrame({username: historyList})
        history[username] = userhistorydf

    history.to_csv(historypath)