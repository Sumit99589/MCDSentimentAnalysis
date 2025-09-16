from textblob import TextBlob
import re

class SentimentAnalyzer:
    def __init__(self):
        print("Initializing SentimentAnalyzer with TextBlob")
    
    def analyze_sentiment(self, text):
        """Analyze sentiment using TextBlob"""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            sentiment = 'positive'
        elif polarity < -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        confidence = abs(polarity)
        
        return {
            'sentiment': sentiment,
            'confidence': round(confidence, 3)
        }
    
    def batch_analyze(self, comments):
        """Analyze multiple comments at once"""
        results = []
        for comment in comments:
            results.append(self.analyze_sentiment(comment))
        return results
