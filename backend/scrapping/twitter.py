import os
from typing import List

import tweepy
from tweepy import API
import pandas as pd
from snscrape.modules import twitter

DEPRESSION = "depression OR feelings of sadness OR hopelessness OR emptiness OR angry " \
             "OR outbursts OR irritability OR " \
             "frustration OR loss of interest OR worthlessness OR guilt OR failures " \
             "OR self blame OR thoughts of death " \
             "OR suicide OR anxiety"

BIPOLAR_DISORDER = "bipolar disorder OR mood swings OR loss of interest OR euphoria " \
                   "OR suicide attempt OR talkativeness OR racing " \
                   "thought OR alcohol abuse"

SCHIZOPHRENIA = "schizophrenia OR thought disorder OR delusion OR amnesia OR false belief of superiority " \
                "OR disorientation OR self-harm " \
                "OR aggression OR hostility OR lack of restraint OR incoherent speech OR circumstantial speech " \
                "OR rapid speaking OR frenzied speaking OR speech disorder"

PSYCHOSIS = "psychosis OR depressive symptoms OR general anxiety OR social isolation OR neglecting self-care " \
            "OR feelings of suspicion OR lower tolerance to stress OR mild disturbance in language " \
            "OR sleep problems OR hallucinations"

PTSD = "ptsd OR nightmares OR flashbacks OR heightened reactivity to stimuli " \
       "OR anxiety OR depressed mood OR Post-Traumatic Stress Disorder OR severe emotional distress"

queries_store = {
    "Depression": DEPRESSION,
    "Bipolar Disorder": BIPOLAR_DISORDER,
    "Schizophrenia": SCHIZOPHRENIA,
    "Psychosis": PSYCHOSIS,
    "Ptsd": PTSD
}


def search():
    for query in queries_store.values():
        tweets: List = []
        for i, tweet in enumerate(twitter.TwitterSearchScraper(query, top=True).get_items()):
            tweets.append(tweet.content)
            __to_csv(query.strip("OR")[0], tweets)


def __to_csv(file_name: str, tweets: List):
    df = pd.DataFrame(tweets, columns=['Text'])
    df.to_csv(f"twitter_data/{file_name}.csv", index=False)
