import glob
import re
from typing import Dict
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd

TRUE_POSITIVE = "True Positive"
FALSE_POSITIVE = "False Positive"
FALSE_NEGATIVE = "False Negative"
TRUE_NEGATIVE = "True Negative"

DEPRESSION = ["depression", "feelings", "sadness", "hopelessness", "emptiness", "angry", "outbursts",
                   "irritability", "frustration", "loss of interest", "worthlessness", "guilt", "failures",
                   "self blame", "thoughts of death", "suicide", "anxiety"]


BIPOLAR_DISORDER = ["bipolar disorder", "mood swings", "loss of interest", "euphoria", "suicide attempt",
                         "talkativeness", "racing thought", "alcohol abuse"]


SCHIZOPHRENIA =  ["schizophrenia", "thought disorder", "delusion", "amnesia", "false belief of superiority",
                      "disorientation", "self-harm", "aggression", "hostility", "lack of restraint",
                      "incoherent speech", "circumstantial speech", "rapid speaking", "frenzied speaking",
                      "speech disorder"]


PSYCHOSIS = ["psychosis", "depressive symptoms", "general anxiety", "social isolation", "neglecting self-care",
                  "feelings of suspicion", "lower tolerance to stress", "mild disturbance in language",
                  "sleep problems", "hallucinations"]


PTSD = ["ptsd", "nightmares", "flashbacks", "heightened reactivity to stimuli", "anxiety",
             "depressed mood", "Post-Traumatic Stress Disorder", "severe emotional distress"]

stressors = {
    "Depression": DEPRESSION,
    "Bipolar Disorder": BIPOLAR_DISORDER,
    "Schizophrenia": SCHIZOPHRENIA,
    "Psychosis": PSYCHOSIS,
    "Ptsd": PTSD
}


def open_file(path_to_file: str) -> pd.DataFrame:
    df = pd.read_csv(path_to_file)
    return df


def save_file(df: pd.DataFrame, path_to_file: str):
    df.to_csv(path_to_file, index=False)


# preprocess the tweets
def preprocess_tweet(tweet):
    nltk.download('all')
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
        filtered_tweet = preprocess_tweet(filtered_tweet)
        sentiment_record = analyze_sentiment(filtered_tweet)
        stressor_present = any(keyword in filtered_tweet for keyword in stressors)
        # determine the emotional state based on stressors and sentiment
        if stressor_present and sentiment_record[1] <= -0.05:
            return TRUE_POSITIVE
        elif sentiment_record[1] <= -0.05 and not stressor_present:
            return FALSE_POSITIVE
        elif sentiment_record[1] > -0.05 and sentiment_record[1] < 0.05 and not sentiment_record:
            return TRUE_NEGATIVE
        elif sentiment_record[1] > -0.05 and sentiment_record[1] < 0.05 and sentiment_record:
            return FALSE_NEGATIVE
        elif sentiment_record[1] >= 0.05:
            return TRUE_NEGATIVE
        elif sentiment_record[1] >= 0.05 and stressor_present:
            return FALSE_NEGATIVE
       
    except Exception:
        return TRUE_NEGATIVE


def run_semtiment_analysis_for_view(text: str) -> Dict:
    outcome = {}
    for stressor, identifiers in stressors.items():
        text = preprocess_tweet(text)
        result = determine_the_emotional_state(text, identifiers)
        outcome[stressor] = result
    return outcome
        
    
# def get_stressors(file: str):
#     for key, query in queries_store.items():
#         if key in file:
#             return query


# def main():
#     csv_files = glob.glob("../scrapping/twitter_data/*.csv")
#     # preprocess the tweets
#     for csv_file in csv_files:
#         stressor = get_stressors(csv_file)
#         df = open_file(csv_file)
#         df = df.applymap(preprocess_tweet)
#         df["Category"] = df['Text'].apply(determine_the_emotional_state, args=(stressor,))
#         save_file(df, csv_file)


# main()
