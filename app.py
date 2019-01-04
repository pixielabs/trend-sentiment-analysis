# Imports the Google Cloud client library
from google.cloud import language
from google.cloud import bigquery
from google.cloud.language import enums
from google.cloud.language import types
from google.api_core.exceptions import InvalidArgument
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from models import Base, Entity, Mention

# Instantiate a BigQuery client and get data from reddit dataset
def query_reddit():
    query_job = bigquery_client.query("""
        SELECT CONCAT(title, selftext) AS text, id, created_utc
        FROM `fh-bigquery.reddit_posts.2017_10`
        WHERE subreddit='technology'
        AND created_utc>1507852800
        AND created_utc<=1507939199""")
    results = query_job.result()  # Waits for job to complete.

    for row in results:
        analyse_sentiment(row.id, row.text, row.created_utc)

    session.commit()

# Makes an entity sentiment analysis call to Natural Language API and inserts the resulting entities and
# entity mentions into the database.
def analyse_sentiment(id, text, posted_at):
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detect the entities in the text
    try:
        entities = nl_api_client.analyze_entity_sentiment(document=document, encoding_type='UTF8').entities

        # Build up our entities object to insert into the table
        entities_object = []
        for e in entities:
            entity = Entity(
                name=e.name, \
                type=e.type, \
                wikipedia_url=e.metadata['wikipedia_url'], \
                mid=e.metadata['mid'], \
                salience=e.salience, \
                sentiment_score=e.sentiment.score, \
                sentiment_magnitude=e.sentiment.magnitude, \
                posted_at=posted_at, \
                remote_post_id=id )

            entity.mentions = create_entity_mentions(e.mentions)
            entities_object.append(entity)

    except InvalidArgument as err:
        print(err)
        return False

    # Insert entities and mentions into the database
    session.add_all(entities_object)

# Create an entity mentions object.
def create_entity_mentions(mentions):
    mentions_object = []
    for m in mentions:
        mention = Mention(
           content=m.text.content, \
           begin_offset=m.text.begin_offset, \
           type=m.type, \
           sentiment_score=m.sentiment.score, \
           sentiment_magnitude=m.sentiment.magnitude )

        mentions_object.append(mention)
    return mentions_object

# Clients for BigQuery and NL API.
nl_api_client = language.LanguageServiceClient()
bigquery_client = bigquery.Client()

# Create the engine.
engine = create_engine(config.DATABASE_URI, echo=True)
Session = sessionmaker(bind=engine)

# Create a new Session.
session = Session()

# Create the schema.
Base.metadata.create_all(engine)

query_reddit()
