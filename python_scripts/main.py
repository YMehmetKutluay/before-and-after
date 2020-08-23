# Download
# import nltk
# nltk.download('vader_lexicon')
# Inspiration: https://amiham-singh.github.io/ 
# Small example: https://towardsdatascience.com/https-towardsdatascience-com-algorithmic-trading-using-sentiment-analysis-on-news-articles-83db77966704
# Dependencies
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import spacy
import pandas as pd

## Sentiment Analysis with NLTK
# Select political leader
leader = "sarkozy"
# Initialize sentiment intensity analyzer (see https://www.nltk.org/api/nltk.sentiment.html)
sia = SentimentIntensityAnalyzer()
# Get before and after text files as single strings
file_path = os.path.join(os.getcwd(), "data", leader, "after.txt")
with open(file_path, 'r') as file:
    after = file.read().replace("\n", "")
file_path = os.path.join(os.getcwd(), "data", leader, "before.txt")
with open(file_path, 'r') as file:
    before = file.read().replace("\n", "")
# Get sentiment score dictionaries
sentiments = {
    "before" : sia.polarity_scores(before),
    "after" : sia.polarity_scores(after)
    }    

## SpaCy Tokenization
# Load English NLP decoder
nlp = spacy.load("en_core_web_sm")
# Tokenize
token_before = nlp(before)
token_after = nlp(after)
## Count adjectives and verbs for both articles
# For before article
# Initiate pandas dataframe
pd_before = pd.DataFrame({"word":[], "pos_value":[]})
for token in token_before:
    # Make row of data
    sub_pd = pd.DataFrame({"word":str(token), "pos_value":token.pos_}, index = [0])
    # Append to pd_before
    pd_before = pd_before.append(sub_pd, ignore_index = True)
# Group by pos_value and count
n_rows = len(pd_before)
pd_before = (
    pd_before
    .groupby("pos_value")
    .agg(before_count = ("pos_value", "count"))
    .reset_index()
    )
# Get word count
before_word_count = pd_before[pd_before["pos_value"] != "PUNCT"]["before_count"].sum()
# Get relative word type counts
pd_before["before_relative_count"] = pd_before["before_count"]/n_rows

# For after article
# Initiate pandas dataframe
pd_after = pd.DataFrame({"word":[], "pos_value":[]})
for token in token_after:
    # Make row of data
    sub_pd = pd.DataFrame({"word":str(token), "pos_value":token.pos_}, index = [0])
    # Append to pd_before
    pd_after = pd_after.append(sub_pd, ignore_index = True)
# Group by pos_value and count
n_rows = len(pd_after)
pd_after = (
    pd_after
    .groupby("pos_value")
    .agg(after_count = ("pos_value", "count"))
    .reset_index()
    )
# Get word count
after_word_count = pd_after[pd_after["pos_value"] != "PUNCT"]["after_count"].sum()
# Get relative word type counts
pd_after["after_relative_count"] = pd_after["after_count"]/n_rows