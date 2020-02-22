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

## Instructions on Running (for Marker)

If you would like to use the sample data, do not run `save_tweets.py` as this will begin appending to the dataset and may skew the values.

The flow of execution then should be:
1. `process_tweets.py`
2. `data_stats.py`
3. `prune_data.py`
4. `analyse_crowdsource.py`

All data is inspectable under the `data/` path.
