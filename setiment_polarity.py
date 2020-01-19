from textblob import TextBlob

def calculate_sentiment_polarity(transcript):
    analysis = TextBlob(transcript)
    return round(analysis.sentiment.polarity, 2)

def emoji_mapper(sentiment_polarity):
    if sentiment_polarity > 0.6:
        return ':D'
    elif 0.20 < sentiment_polarity <= 0.60:
        return ':)'
    elif -0.20 <= sentiment_polarity <= 0.20:
        return ':-|'
    elif -0.60 <= sentiment_polarity < -0.20:
        return '>:O'
    elif sentiment_polarity < -0.60:
        return ':`-('