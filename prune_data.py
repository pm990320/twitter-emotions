import json

import pandas as pd

from web_science.database_models import connect_to_mongo, Tweet, ProcessedTweet

connect_to_mongo()

def tweets_to_df(queryset):
    df = pd.DataFrame(list(map(lambda x: json.loads(x.to_json()), queryset)))
    df.set_index(["id_str"], inplace=True, drop=False)
    return df

tweets_df = tweets_to_df(ProcessedTweet.objects.all())
sampled_ptdf = tweets_df.groupby(["emotion_label"]).apply(lambda x: x.head(150))

ok_ids = sampled_ptdf["id_str"].tolist()
ProcessedTweet.objects(id_str__nin=ok_ids).delete()
# Tweet.objects(id_str__nin=ok_ids).delete()
