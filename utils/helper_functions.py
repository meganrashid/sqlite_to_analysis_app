import pandas as pd
from bs4 import BeautifulSoup
from collections import Counter
from nltk.tokenize import word_tokenize

# Print to verify that the module is being executed
print("helper_functions.py has been loaded")

def word_count(text):
    """
    # of words in a text
    """
    return len(str(text).split(' '))

def word_freq(clean_text_list, top_n):
    """
    Word Frequency Counter
    """
    flat = [item for sublist in clean_text_list for item in sublist]
    with_counts = Counter(flat)
    top = with_counts.most_common(top_n)
    word = [each[0] for each in top]
    num = [each[1] for each in top]
    return pd.DataFrame([word, num]).T

