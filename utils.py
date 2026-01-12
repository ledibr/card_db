import pandas as pd
import unicodedata


def format_pandas():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.width', 200)


def normalize(text):
    text = unicodedata.normalize('NFD', text)
    result = []
    for i in range(len(text)):
        if text[i].isalpha() or text[i].isspace():
            result.append(text[i])
    result = unicodedata.normalize('NFC', ''.join(result))
    return result