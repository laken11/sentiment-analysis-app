import glob
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from backend.scrapping.twitter import queries_store

TRUE_POSITIVE = "True Positive"
FALSE_POSITIVE = "False Positive"
FALSE_NEGATIVE = "False Negative"
TRUE_NEGATIVE = "True Negative"


def open_file(path_to_file: str) -> pd.DataFrame:
    df = pd.read_csv(path_to_file)
    return df


def save_file(df: pd.DataFrame, path_to_file: str):
    df.to_csv(path_to_file, index=False)


# preprocess the tweets
def preprocess_tweet(tweet):
    # convert to lowercase
    if pd.isna(tweet):
        return
    tweet = tweet.lower()
    # remove URLs, mentions, and hashtags
    tweet = re.sub(r"http\S+|www\S+|@\w+|\#\w+", "", tweet)
    # remove punctuation
    tweet = re.sub(r"[^\w\s]", "", tweet)
    # tokenize the tweet
    tokens = word_tokenize(tweet)
    # remove stop words
    stop_words = set(stopwords.words("english"))
    filtered_tokens = [token for token in tokens if token not in stop_words]
    # return the filtered tokens as a string
    return " ".join(filtered_tokens)


# analyze the sentiment of a tweet
def analyze_sentiment(tweet):
    try:
        # use TextBlob to get the sentiment score
        blob = TextBlob(tweet)
        sentiment_score = blob.sentiment.polarity
        # use VADER to get the sentiment score
        analyzer = SentimentIntensityAnalyzer()
        vader_scores = analyzer.polarity_scores(tweet)
        vader_score = vader_scores["compound"]
        return sentiment_score, vader_score
    except TypeError:
        return 0, 0


def determine_the_emotional_state(filtered_tweet, stressors):
    try:
        sentiment_record = analyze_sentiment(filtered_tweet)
        stressor_present = any(keyword in filtered_tweet for keyword in stressors)
        # determine the emotional state based on stressors and sentiment
        if stressor_present and sentiment_record[0] < 0:
            return TRUE_POSITIVE
        elif stressor_present and sentiment_record[1] < -0.5:
            return TRUE_POSITIVE
        elif sentiment_record[0] < 0:
            return FALSE_POSITIVE
        elif sentiment_record[0] > 0:
            return TRUE_NEGATIVE
        else:
            return FALSE_NEGATIVE
    except Exception:
        return FALSE_NEGATIVE


def get_stressors(file: str):
    for key, query in queries_store.items():
        if key in file:
            return query


def main():
    csv_files = glob.glob("../scrapping/twitter_data/*.csv")
    # preprocess the tweets
    for csv_file in csv_files:
        stressor = get_stressors(csv_file)
        df = open_file(csv_file)
        df = df.applymap(preprocess_tweet)
        df["Category"] = df['Text'].apply(determine_the_emotional_state, args=(stressor,))
        save_file(df, csv_file)


main()
