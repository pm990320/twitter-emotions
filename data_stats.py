from datetime import datetime
import os
from os.path import join, dirname, exists
import json

import pandas as pd

from web_science.database_models import connect_to_mongo, Tweet, ProcessedTweet
from web_science.utils.encode_emoji import replace_emoji_characters

RESULTS_DIR = join(dirname(__file__), "results")
if not exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

DATA_DIR = join(dirname(__file__), "data")
if not exists(DATA_DIR):
    os.makedirs(DATA_DIR)

connect_to_mongo()


def parse_created_at(x):
    if isinstance(x, dict):
        return datetime.fromtimestamp(x["$date"]/1000)
    else:
        return x


def tweets_to_df(queryset):
    df = pd.DataFrame(list(map(lambda x: json.loads(x.to_json()), queryset)))
    df.set_index(["id_str"], inplace=True, drop=False)
    if "created_at" in df.columns:
        df["created_at"] = df["created_at"].apply(parse_created_at)
    return df


tweets_df = tweets_to_df(Tweet.objects.all())
tweets_df.to_csv(join(DATA_DIR, "tweets-raw.csv"))

processed_tweets_df = tweets_to_df(ProcessedTweet.objects.all())
if len(processed_tweets_df):
    processed_tweets_df.to_csv(join(DATA_DIR, "tweets-processed.csv"))
    count_by_emotion_label = processed_tweets_df[["id_str", "emotion_label", "created_at"]].groupby(['emotion_label']).agg({
        "id_str": "count",
        "created_at": ["min", "max"]
    })
    count_by_emotion_label.to_csv(join(RESULTS_DIR, "2b.csv"), header=False)

sampled_ptdf = processed_tweets_df.groupby(["emotion_label"]).apply(pd.DataFrame.sample, n=15)
sampled_ptdf["text"] = sampled_ptdf["raw_text"]
sampled_ptdf["text"] = sampled_ptdf["text"].map(replace_emoji_characters)
sampled_ptdf[["text"]].to_csv(join(DATA_DIR, "mturk.csv"))
