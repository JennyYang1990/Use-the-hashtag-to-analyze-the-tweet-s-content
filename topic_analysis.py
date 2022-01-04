import json
from gensim.models import LdaModel
from gensim.corpora.dictionary import Dictionary
import re
#import nltk
from nltk.corpus import stopwords
import string
#import pickle

#tweet_json = "tweet.json"
#tweet_json = "tweet_clean.json"
#nltk.download('stopwords')
punctuation = list(string.punctuation)
stop = set(stopwords.words('english') + punctuation + ['rt', 'via', 'RT', '…', '#backtoschool', 'back', 'school'])

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)


def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=True):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
        tokens = [tk for tk in tokens if tk not in stop]
        tokens = [tk for tk in tokens if tk[0]=='#' or tk[0].isalpha()]
        tokens = [tk for tk in tokens if not tk.startswith('https://')]
    return tokens

def load_clean_data(input_file):
    data = []
    with open(input_file, 'r') as f:
        for line in f:
            tweet = json.loads(line)
            tokens = preprocess(tweet['text'])
            data.append(tokens)
    return data

tweet_json = "tweet_no_duplicate.json"

data = load_clean_data(tweet_json)
common_dictionary = Dictionary(data)
common_corpus = [common_dictionary.doc2bow(text) for text in data]

# Train the model on the corpus.
topic_numbers = 40
lda = LdaModel(common_corpus, num_topics=topic_numbers, alpha='auto')
topics = []
for i in range(topic_numbers):
	topic_tuples = lda.show_topic(i, topn=20)
	topic_words = [common_dictionary[int(tp[0])] for tp in topic_tuples]
	topics.append(topic_words)
#lda.save('lda_model_good')
#pickle.dump(topics, open('topics_of_backtoschool.pkl','wb'))