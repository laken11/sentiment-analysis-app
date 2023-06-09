import re
from typing import Dict
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
from backend.GBT import engine

TRUE_POSITIVE = "True Positive"
FALSE_POSITIVE = "False Positive"
FALSE_NEGATIVE = "False Negative"
TRUE_NEGATIVE = "True Negative"

DEPRESSION = ["depression", "feelings", "sadness", "hopelessness", "emptiness", "angry", "outbursts",
              "irritability", "frustration", "loss of interest", "worthlessness", "guilt", "failures",
              "self blame", "thoughts of death", "suicide", "anxiety"]

BIPOLAR_DISORDER = ["bipolar disorder", "mood swings", "loss of interest", "euphoria", "suicide attempt",
                    "talkativeness", "racing thought", "alcohol abuse"]

SCHIZOPHRENIA = ["schizophrenia", "thought disorder", "delusion", "amnesia", "false belief of superiority",
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
    # convert to lowercase
    if pd.isna(tweet):
        return
    tweet = tweet.lower()
    # remove URLs, mentions, and hashtags
    tweet = re.sub(r"http\S+|www\S+|@\w+|\#\w+", "", tweet)
    # remove punctuation
    tweet = re.sub(r"[^\w\s]", "", tweet)
    return tweet


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


def pretty_response(response: dict):
    ...


def analyze_sentiment_gbt(statement: str):
    prompt = "Category a statement if 0 = Positive, 1 = Negative or 2 = Neutral respond with just 0, 1, or 2"
    response = engine.chat_completion_gbt(prompt, args=[statement])
    if "1" in response or 'Negative'.lower() in response.lower():
        return 1
    elif "2" in response or 'Positive'.lower() in response.lower():
        return 2
    elif "0" in response or 'Neutral'.lower() in response.lower():
        return 0
    return 2


def get_pretty_response(info: str):
    prompt = f"{info} is a result of a sentiment analysis on a given text by a user, " \
             f"make this human readable response in just few sentences as assuming the response would " \
             f"be shown to the user in very simple format"
    response = engine.chat_completion_gbt(prompt, args=[info])
    return response


def determine_the_emotional_state(filtered_tweet, stressors):
    try:
        sentiment_record = analyze_sentiment(filtered_tweet)
        stressor_present = any(keyword in filtered_tweet for keyword in stressors)
        # determine the emotional state based on stressors and sentiment
        if stressor_present and sentiment_record[1] <= -0.05:
            return TRUE_POSITIVE
        elif sentiment_record[1] <= -0.05 and not stressor_present:
            return FALSE_POSITIVE
        elif -0.05 < sentiment_record[1] < 0.05 and not sentiment_record:
            return FALSE_NEGATIVE
        elif -0.05 < sentiment_record[1] < 0.05 and sentiment_record:
            return TRUE_NEGATIVE
        elif sentiment_record[1] >= 0.05 and stressor_present:
            return TRUE_NEGATIVE
        elif sentiment_record[1] >= 0.05 and not stressor_present:
            return FALSE_NEGATIVE
    except Exception as e:
        print(e)
        return TRUE_NEGATIVE


def categorize_statement(sentiment_analysis: int, statement: str,  stressors):
    stressor_present = any(keyword in statement for keyword in stressors)
    if sentiment_analysis == 1 and stressor_present:
        return TRUE_POSITIVE
    elif sentiment_analysis == 1 and not stressor_present:
        return FALSE_POSITIVE
    elif (sentiment_analysis == 0 or sentiment_analysis == 2) and stressor_present:
        return TRUE_NEGATIVE
    elif (sentiment_analysis == 0 or sentiment_analysis == 2) and not stressor_present:
        return FALSE_NEGATIVE


def run_sentiment_analysis_for_view(text: str) -> Dict:
    outcome = {}
    text = preprocess_tweet(text)
    sentiment_analysis = analyze_sentiment_gbt(text)
    for stressor, identifiers in stressors.items():
        result = categorize_statement(sentiment_analysis, text, identifiers)
        response = get_pretty_response(f"{stressor}: {result}")
        outcome[stressor] = response + f" ({result})"
    return outcome
