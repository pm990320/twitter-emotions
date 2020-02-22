import json

import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report

from web_science.database_models import connect_to_mongo, Tweet, ProcessedTweet

connect_to_mongo()

# Load mechanical turk results into familiar format
cs_df = pd.read_csv("data/mturk_results.csv")
cs_df = cs_df[["Answer.emotion.label", "Input.id_str"]]
cs_df["id_str"] = cs_df["Input.id_str"].apply(str)

MTURK_TO_EMOTION = {
    "Excitement": "excitement",
    "Happiness": "happy",
    "Fear": "fear",
    "Surprise": "surprise",
    "Pleasant": "pleasant",
    "Anger": "anger",
}
def map_mturk_name_to_emotion(mturk):
    return MTURK_TO_EMOTION.get(mturk, mturk)

cs_df["human_emotion_label"] = cs_df["Answer.emotion.label"].map(map_mturk_name_to_emotion)
cs_df = cs_df[["id_str", "human_emotion_label"]]
cs_df.set_index("id_str", drop=True, inplace=True)

# load processed tweets
queryset = ProcessedTweet.objects.all()
pt_df = pd.DataFrame(list(map(lambda x: json.loads(x.to_json()), queryset)))
pt_df = pt_df[["id_str", "emotion_label", "raw_text", "processed_text"]]
pt_df.set_index(["id_str"], inplace=True, drop=True)

df = cs_df.merge(pt_df, how="inner", left_index=True, right_index=True)

cl_report = classification_report(df['human_emotion_label'].values, df['emotion_label'].values, labels=df['emotion_label'].unique().sort())
with open("results/cl_report.txt", "w") as f:
    f.write(cl_report)
