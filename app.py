from flask import Flask, request, jsonify
from flask_cors import CORS
from textblob import TextBlob
from collections import Counter
import re

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

class SentimentAnalyzer:
    def analyze_sentiment(self, text):
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            return 'positive', abs(polarity)
        elif polarity < -0.1:
            return 'negative', abs(polarity)
        else:
            return 'neutral', abs(polarity)

# Sample comments data
SAMPLE_COMMENTS = [
    "The proposed amendments are very beneficial for small businesses.",
    "I find some provisions quite restrictive and unfavorable.",
    "The draft legislation lacks clarity in certain sections.",
    "Great initiative by MCA, looking forward to implementation.",
    "Some parts are good, but overall needs improvement."
]

sentiment_analyzer = SentimentAnalyzer()

@app.route('/analyze', methods=['POST'])
def analyze_comments():
    try:
        data = request.get_json() or {}
        comments = data.get('comments', [])
        
        if not comments:
            comments = SAMPLE_COMMENTS
        
        results = []
        sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
        all_text = ""
        
        for comment in comments:
            sentiment, confidence = sentiment_analyzer.analyze_sentiment(comment)
            
            results.append({
                'comment': comment,
                'sentiment': sentiment,
                'confidence': round(confidence, 3),
                'summary': comment[:100] + "..." if len(comment) > 100 else comment
            })
            
            sentiment_counts[sentiment] += 1
            all_text += comment + " "
        
        # Simple word frequency
        words = re.findall(r'\b[a-zA-Z]{4,}\b', all_text.lower())
        word_freq = dict(Counter(words).most_common(30))
        
        return jsonify({
            'individual_results': results,
            'sentiment_distribution': sentiment_counts,
            'wordcloud_data': word_freq,
            'total_comments': len(comments),
            'model_info': {
                'name': 'TextBlob',
                'description': 'Rule-based sentiment analysis',
                'accuracy': '75-80%',
                'type': 'Lexicon-based'
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
