from datetime import datetime
import os
from os.path import join, dirname, exists
import json

import pandas as pd

from web_science.database_models import connect_to_mongo, Tweet, ProcessedTweet

RESULTS_DIR = join(dirname(__file__), "results")
if not exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

connect_to_mongo()


def parse_created_at(x):
    return datetime.fromtimestamp(x["$date"]/1000)


def tweets_to_df(queryset):
    tweets_df = pd.DataFrame(list(map(lambda x: json.loads(x.to_json()), queryset)))
    tweets_df["created_at"] = tweets_df["created_at"].apply(parse_created_at)
    return tweets_df


def count_by_emotion_label(df, file_name):
    count_by_emotion_label = df[["id_str", "emotion_label", "created_at"]].groupby(['emotion_label']).agg({
        "id_str": "count",
        "created_at": ["min", "max"]
    })
    print(count_by_emotion_label)
    count_by_emotion_label.to_csv(join(RESULTS_DIR, file_name), header=False)


tweets_df = tweets_to_df(Tweet.objects.all())
count_by_emotion_label(tweets_df, "2b.csv")

tweets_df = tweets_to_df(ProcessedTweet.objects.all())
count_by_emotion_label(tweets_df, "2b-post.csv")
