
import pandas as pd

history = pd.DataFrame()

historypath = 'historie.csv'

def load_histories(path = historypath):
    # nacte soubor s historiemi
    global history
    print("loading history from " + path)
    history = pd.read_csv(path)
    print(history.head(5))

def save_history(username, historyList):
    # ulozi historii do souboru
    global history, historypath

    if username == None:
        print('no user logged in, no history saved')
        return

    if username not in history:
        # kdyz to je novy uzivatel tak to pripoj jako novy sloupec
        print('user {} doesn\'t exist, creating new column'.format(username))
        history = history.append(pd.DataFrame({username: historyList}, columns=[username]), ignore_index=True)
    else:
        print('user {} found, appending to existing history'.format(username))
        history = history.append(pd.DataFrame({username: historyList}, columns=[username]), ignore_index=True)

    history.to_csv(historypath)