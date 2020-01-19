from pymongo import MongoClient
import uuid
import os
from setiment_polarity import calculate_sentiment_polarity, emoji_mapper

password=os.getenv('mongo_password')
client = MongoClient(f'mongodb+srv://user1:{password}@cluster0-bf7gi.mongodb.net/test?retryWrites=true&w=majority')
db = client['InteractivityChallenge']
collection = db['individualUser']

def insert(transcript, sentiment_polarity, emoji):
    _id=uuid.uuid4()
    record = {
        '_id': str(_id),
        'transcript': transcript,
        'sentiment_polarity': sentiment_polarity,
        'emoji': emoji
    }
    collection.insert_one(record)

def find():
    record = collection.find({})
    for doc in record:
        print(doc)
    return record

def augment_and_insert(transcript):
    sentiment_polarity = calculate_sentiment_polarity(transcript)
    emoji = emoji_mapper(sentiment_polarity)
    insert(transcript, sentiment_polarity, emoji)

find()