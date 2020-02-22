import sys
import re
import html
from pprint import pprint

import gensim
import gensim.downloader as api
from mongoengine import DoesNotExist
from nltk.tokenize import word_tokenize
import nltk
import numpy as np

from web_science.database_models import connect_to_mongo, Tweet, ProcessedTweet
from web_science.emotions import get_emotion_pure_words

RT_REGEX = re.compile("^(RT @.*: )")
HANDLE_REGEX = re.compile("(@\w{1,15})\s")
INCOMPLETE_WORD_REGEX = re.compile("^.* (\w+…) ")
EMOTION_WORDS = get_emotion_pure_words()
SIMILARITY_THRESHOLD = 0.20


def remove_retweet(text):
    rt_match = RT_REGEX.match(text)
    if rt_match:
        return text.replace(rt_match.group(1), "")
    return text


def remove_ellipsis_incomplete_word(text):
    ellipsis_match = INCOMPLETE_WORD_REGEX.match(text)
    if ellipsis_match:
        return text.replace(ellipsis_match.group(1), "")
    return text


def remove_twitter_handles(text):
    handle_match = HANDLE_REGEX.search(text)
    new_text = text
    if handle_match:
        for matched_handle in handle_match.groups():
            new_text = new_text.replace(matched_handle, "")
    return new_text


def relabel_word2vec(text, word2vec_model):
    def filter_non_vocabulary_words(tweet_word):
        if tweet_word not in word2vec_model.vocab:
            # print(f"\t{tweet_word} not in vocabulary")
            return False
        return True

    tokenised_tweet = word_tokenize(text)
    tokenised_tweet = list(filter(filter_non_vocabulary_words, tokenised_tweet))

    emotion_scores = {}
    for emotion, emotion_words in EMOTION_WORDS.items():
        word_scores = []

        valid_emotion_words = list(filter(filter_non_vocabulary_words, emotion_words))
        if len(valid_emotion_words) == 0:
            raise ValueError(f"Emotion {emotion} has no valid words in dictionary!")

        for emotion_word in valid_emotion_words:
            tweet_word_scores = []
            
            for tweet_word in tokenised_tweet:
                similarity = word2vec_model.similarity(emotion_word, tweet_word)
                tweet_word_scores.append(similarity)

            if len(tweet_word_scores) > 0:
                word_scores.append(np.mean(tweet_word_scores))
        
        emotion_scores[emotion] = np.max(word_scores) if len(word_scores) > 0 else 0

    new_emotion_label = max(emotion_scores.keys(), key=lambda k: emotion_scores[k])
    return emotion_scores, new_emotion_label


def process_tweet(tweet_model, word2vec_model):
    raw_text = tweet_model.text

    # HTML unescape the tweet
    processed_text = html.unescape(raw_text)

    # remove RT, twitter handles, ellipsis
    processed_text = remove_retweet(processed_text)
    processed_text = remove_twitter_handles(processed_text)
    processed_text = remove_ellipsis_incomplete_word(processed_text)

    print(processed_text)

    # relabel according to Word2Vec
    emotion_scores, new_emotion_label = relabel_word2vec(processed_text, word2vec_model)
    pprint(emotion_scores)

    if new_emotion_label != tweet_model.emotion_label:
        print(f"Tweet {tweet_model.id_str} changed from {tweet_model.emotion_label} to {new_emotion_label}\n{processed_text}")

    try:
        processed_tweet_model = ProcessedTweet.objects(id_str=tweet_model.id_str).get()
    except DoesNotExist:
        processed_tweet_model = ProcessedTweet(id_str=tweet_model.id_str)

    # if the tweet scores more than the similarity threshold for any emotion other than it's labelled one, discard it, it's not clean
    if len(list(filter(lambda item: item[1] > SIMILARITY_THRESHOLD, emotion_scores.items()))) > 1:
        print(f"Discarding tweet {tweet_model.id_str} due to ambiguous emotion.")
        pprint(emotion_scores)
        try:
            processed_tweet_model.delete()
        except DoesNotExist:
            pass

    processed_tweet_model.emotion_label = new_emotion_label
    processed_tweet_model.raw_text = raw_text
    processed_tweet_model.processed_text = processed_text
    processed_tweet_model.created_at = tweet_model.created_at
    processed_tweet_model.save()


def process_tweets():
    print("Loading Word2Vec model...")
    word2vec_model = api.load('word2vec-google-news-300')
    print("Word2Vec model loaded.")

    # for tweet in Tweet.objects(id_str__nin=[t.id_str for t in ProcessedTweet.objects.all()]):
    for tweet in Tweet.objects():
        print(f"Processing {tweet.id_str}")
        try:
            process_tweet(tweet, word2vec_model)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(e, file=sys.stderr)


if __name__ == "__main__":
    connect_to_mongo()
    nltk.download("punkt")
    process_tweets()
