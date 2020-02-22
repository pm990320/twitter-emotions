import os

from dotenv import load_dotenv
from mongoengine import connect, Document, StringField, DateTimeField


def connect_to_mongo():
    load_dotenv()
    connect(
        os.getenv("MONGO_INITDB_DATABASE"),
        username=os.getenv("MONGO_INITDB_ROOT_USERNAME"),
        password=os.getenv("MONGO_INITDB_ROOT_PASSWORD"),
        authentication_source='admin'
    )


class Tweet(Document):
    id_str = StringField(unique=True)
    emotion_label = StringField()
    text = StringField()
    created_at = DateTimeField()
    meta = {'allow_inheritance': True}


class ProcessedTweet(Document):
    id_str = StringField(unique=True)
    created_at = DateTimeField()
    emotion_label = StringField()
    processed_text = StringField()
    raw_text = StringField()


if __name__ == "__main__":
    connect_to_mongo()
