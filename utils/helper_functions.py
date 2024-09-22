import pandas as pd
from bs4 import BeautifulSoup
from collections import Counter

from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

import itertools, string, re, unicodedata, nltk



# Print to verify that the module is being executed
print("helper_functions.py has been loaded")

########################################## contraction dictionary ###################################################
#Contraction map
c_dict = {
  "ain't": "am not",
  "aren't": "are not",
  "can't": "cannot",
  "can't've": "cannot have",
  "'cause": "because",
  "could've": "could have",
  "couldn't": "could not",
  "couldn't've": "could not have",
  "didn't": "did not",
  "doesn't": "does not",
  "don't": "do not",
  "hadn't": "had not",
  "hadn't've": "had not have",
  "hasn't": "has not",
  "haven't": "have not",
  "he'd": "he would",
  "he'd've": "he would have",
  "he'll": "he will",
  "he'll've": "he will have",
  "he's": "he is",
  "how'd": "how did",
  "how'd'y": "how do you",
  "how'll": "how will",
  "how's": "how is",
  "i'd": "I would",
  "i'd've": "I would have",
  "i'll": "I will",
  "i'll've": "I will have",
  "i'm": "I am",
  "i've": "I have",
  "isn't": "is not",
  "it'd": "it had",
  "it'd've": "it would have",
  "it'll": "it will",
  "it'll've": "it will have",
  "it's": "it is",
  "let's": "let us",
  "ma'am": "madam",
  "mayn't": "may not",
  "might've": "might have",
  "mightn't": "might not",
  "mightn't've": "might not have",
  "must've": "must have",
  "mustn't": "must not",
  "mustn't've": "must not have",
  "needn't": "need not",
  "needn't've": "need not have",
  "o'clock": "of the clock",
  "oughtn't": "ought not",
  "oughtn't've": "ought not have",
  "shan't": "shall not",
  "sha'n't": "shall not",
  "shan't've": "shall not have",
  "she'd": "she would",
  "she'd've": "she would have",
  "she'll": "she will",
  "she'll've": "she will have",
  "she's": "she is",
  "should've": "should have",
  "shouldn't": "should not",
  "shouldn't've": "should not have",
  "so've": "so have",
  "so's": "so is",
  "that'd": "that would",
  "that'd've": "that would have",
  "that's": "that is",
  "there'd": "there had",
  "there'd've": "there would have",
  "there's": "there is",
  "they'd": "they would",
  "they'd've": "they would have",
  "they'll": "they will",
  "they'll've": "they will have",
  "they're": "they are",
  "they've": "they have",
  "to've": "to have",
  "wasn't": "was not",
  "we'd": "we had",
  "we'd've": "we would have",
  "we'll": "we will",
  "we'll've": "we will have",
  "we're": "we are",
  "we've": "we have",
  "weren't": "were not",
  "what'll": "what will",
  "what'll've": "what will have",
  "what're": "what are",
  "what's": "what is",
  "what've": "what have",
  "when's": "when is",
  "when've": "when have",
  "where'd": "where did",
  "where's": "where is",
  "where've": "where have",
  "who'll": "who will",
  "who'll've": "who will have",
  "who's": "who is",
  "who've": "who have",
  "why's": "why is",
  "why've": "why have",
  "will've": "will have",
  "won't": "will not",
  "won't've": "will not have",
  "would've": "would have",
  "wouldn't": "would not",
  "wouldn't've": "would not have",
  "y'all": "you all",
  "y'alls": "you alls",
  "y'all'd": "you all would",
  "y'all'd've": "you all would have",
  "y'all're": "you all are",
  "y'all've": "you all have",
  "you'd": "you had",
  "you'd've": "you would have",
  "you'll": "you you will",
  "you'll've": "you you will have",
  "you're": "you are",
  "you've": "you have"
}

c_re = re.compile('(%s)' % '|'.join(c_dict.keys()))

stopwords = list(set(stopwords.words('english')))
add_stopwords = ['sep','say', 's', 'u', 'ap', 'afp', 'n','us','get','new','services','service','help','contact','company','call','view','best','home']
stopwords.extend(add_stopwords)

punc = list(set(string.punctuation))
punc.extend(['\\','\"','',' ','...','ã¢â‚¬â','\'','\'s','-','--',"''",'\``',"’"])

lemmatizer = WordNetLemmatizer()

###################################### text EDA ##################################################################

def word_count(text):
    """ counts number of words in a text
    
    Args:
    - text (str): text to count words
    """
    return len(str(text).split(' '))

def word_freq(clean_text_list, top_n):
    """ Count word frequency

    Args:
    - clean_text_list (list): list of strings
    - top_n (integer): number to filter top N values
    """
    flat = [item for sublist in clean_text_list for item in sublist]
    with_counts = Counter(flat)
    top = with_counts.most_common(top_n)
    word = [each[0] for each in top]
    num = [each[1] for each in top]
    return pd.DataFrame([word, num]).T

########################################## text preprocessing #######################################################
def join_text_columns(df, columns, separator=' '):
    """
    Joins text from multiple columns in a DataFrame.

    Args:
    - df (DF): pandas DataFrame
    - columns (list): list of column names to join
    - separator (str): string used to separate joined text (default is a space)

    Returns:
    - pandas Series containing the joined text
    """
    return df[columns].apply(lambda row: separator.join(row.dropna().astype(str)), axis=1)

def remove_html(text):
    """ Remove html formatting

    Args:
    - text (str): text to clean
    """
    soup = BeautifulSoup(text, "html5lib")
    tags_del = soup.get_text()
    uni = unicodedata.normalize("NFKD", tags_del)
    bracket_del = re.sub(r'\[.*?\]', '  ', uni)
    apostrphe = re.sub('’', "'", bracket_del)
    string = apostrphe.replace('\r','  ')
    string = string.replace('\n','  ')
    extra_space = re.sub(' +',' ', string)
    return extra_space

def expandContractions(text, c_re=c_re):
    def replace(match):
        return c_dict[match.group(0)]
    return c_re.sub(replace, text)

#Function to replace the nltk pos tags with the corresponding wordnet pos tag to use the wordnet lemmatizer
def get_word_net_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None
    
# def lemma_wordnet(tagged_text):
#     final = []
#     for word, tag in tagged_text:
#         wordnet_tag = get_word_net_pos(tag)
#         if wordnet_tag is None:
#             final.append(lemmatizer.lemmatize(word))
#         else:
#             final.append(lemmatizer.lemmatize(word, pos=wordnet_tag))
#     return final

def lemmatize_text(text):
    return [lemmatizer.lemmatize(w) for w in word_tokenize(text)]

def process_text(text):
    """ Remove html formatting

    Args:
    - text (str): text to clean
    """
    soup = BeautifulSoup(text, "lxml")
    tags_del = soup.get_text()
    no_html = re.sub('<[^>]*>', '', tags_del)
    tokenized = word_tokenize(no_html)
    lower = [item.lower() for item in tokenized]
    decontract = [expandContractions(item, c_re=c_re) for item in lower]
    # lemma = [lemmatize_text(item) for item in decontract]
    # tagged = nltk.pos_tag(decontract)
    # lemma = lemma_wordnet(tagged)
    no_num = [re.sub('[0-9]+', '', each) for each in decontract]
    no_punc = [w for w in no_num if w not in punc]
    no_stop = [w for w in no_punc if w not in stopwords]
    return no_stop
