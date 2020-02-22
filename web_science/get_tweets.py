import itertools

from .twitter_stream import stream_tweets_matching_filter


def filter_unclean_tweet(tweet, desired_emotion_class, match_terms_map):
    for emotion_class, match_terms in match_terms_map.items():
        if emotion_class == emotion_class:
            continue

        for term in match_terms:
            if term in tweet.text:
                return False
    
    return True


def get_preclean_tweets(match_terms_map, num_per_class):
    clean_tweets_by_emotion = {}

    for emotion_class, match_terms in match_terms_map.items():
        query_expr = ",".join(match_terms)

        def _filter_unclean_tweet(tweet):
            return filter_unclean_tweet(tweet, emotion_class, match_terms_map)

        stream = stream_tweets_matching_filter(query_expr, _filter_unclean_tweet)
        clean_tweets = itertools.islice(stream, num_per_class)
        clean_tweets_by_emotion[emotion_class] = clean_tweets

    return clean_tweets_by_emotion
