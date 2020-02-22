# Twitter Scraper and Emotion Analysis

Patrick Menlove - 2250066M

This code is part of an academic assignment of Web Science - University of Glasgow.


## Setup

You can use `conda` to create a virtualenv with all required dependencies
```bash
conda env create -f environment.yml
```

The example also uses Docker to run a MongoDB instance with the sample data.
```bash
docker-compose up -d
```

If you would like to run the `save_tweets.py` file to ingest new tweets, you will need to set up the `.env` file with the following environment variables, corresponding to the Twitter API credentials
```
TWITTER_CONSUMER_KEY
TWITTER_CONSUMER_SECRET
TWITTER_ACCESS_TOKEN
TWITTER_ACCESS_TOKEN_SECRET
```
