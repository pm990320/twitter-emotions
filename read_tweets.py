from mongoengine import DoesNotExist

from web_science.get_tweets import get_preclean_tweets
from web_science.database_models import connect_to_mongo, Tweet, ProcessedTweet

connect_to_mongo()

# for tweet in Tweet.objects.limit(10):
#     unwrapped_text = tweet.text.replace('\n', '\t')
#     print(f"{tweet.id_str} [{tweet.emotion_label}]: {unwrapped_text}")

for tweet in ProcessedTweet.objects(emotion_label="fear").limit(50):
    unwrapped_text = tweet.processed_text.replace('\n', '\t')
    print(f"{tweet.id_str} [{tweet.emotion_label}]: {unwrapped_text}")

print(f"{Tweet.objects.count()} Tweets stored in DB")
print(f"{ProcessedTweet.objects.count()} Processed Tweets stored in DB")
