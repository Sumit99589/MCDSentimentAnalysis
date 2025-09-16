import re
import nltk
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import io
import base64
import random

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

class TextProcessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.stop_words.update(['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'will', 'be'])
    
    def clean_text(self, text):
        """Clean and preprocess text"""
        text = re.sub(r'\s+', ' ', text.strip())
        return text
    
    def generate_summary(self, text, max_length=50):
        """Generate summary of the text"""
        if len(text.split()) < 10:
            return text
        
        sentences = sent_tokenize(text)
        if len(sentences) <= 2:
            return text
        
        words = word_tokenize(text.lower())
        word_freq = Counter([word for word in words if word.isalpha() and word not in self.stop_words])
        
        sentence_scores = {}
        for sentence in sentences:
            sentence_words = word_tokenize(sentence.lower())
            score = sum(word_freq.get(word, 0) for word in sentence_words)
            sentence_scores[sentence] = score
        
        if sentence_scores:
            top_sentence = max(sentence_scores, key=sentence_scores.get)
            
            if sentences[0] != top_sentence:
                return f"{sentences[0]} {top_sentence}"
            else:
                return '. '.join(sentences[:2]) + '.'
        else:
            return '. '.join(sentences[:2]) + '.'
    
    def generate_wordcloud_data(self, text):
        """Generate word frequency data for word cloud"""
        cleaned_text = self.clean_text(text.lower())
        words = word_tokenize(cleaned_text)
        
        filtered_words = [word for word in words 
                         if word.isalpha() 
                         and word not in self.stop_words 
                         and len(word) > 2]
        
        word_freq = Counter(filtered_words)
        return dict(word_freq.most_common(50))
    
    def create_simple_wordcloud_image(self, text, width=800, height=400):
        """Create a simple word cloud visualization using matplotlib"""
        word_freq = self.generate_wordcloud_data(text)
        
        if not word_freq:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.text(0.5, 0.5, 'No significant words found', 
                   ha='center', va='center', fontsize=20, color='gray')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
            plt.close()
            
            img_buffer.seek(0)
            return base64.b64encode(img_buffer.getvalue()).decode()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        max_freq = max(word_freq.values())
        min_freq = min(word_freq.values())
        
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                 '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        
        positions = []
        x_positions = np.linspace(0.1, 0.9, 8)
        y_positions = np.linspace(0.1, 0.9, 6)
        
        for x in x_positions:
            for y in y_positions:
                positions.append((x, y))
        
        random.shuffle(positions)
        
        word_items = list(word_freq.items())[:len(positions)]
        
        for i, (word, freq) in enumerate(word_items):
            if i >= len(positions):
                break
                
            x, y = positions[i]
            font_size = 10 + (freq - min_freq) / (max_freq - min_freq) * 30
            color = colors[i % len(colors)]
            
            ax.text(x, y, word, fontsize=font_size, color=color, 
                   ha='center', va='center', weight='bold')
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title('Stakeholder Comments Word Cloud', fontsize=16, pad=20)
        
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150, 
                   facecolor='white', edgecolor='none')
        plt.close()
        
        img_buffer.seek(0)
        return base64.b64encode(img_buffer.getvalue()).decode()
    
    def extract_keywords(self, text, num_keywords=10):
        """Extract top keywords from text"""
        word_freq = self.generate_wordcloud_data(text)
        return list(word_freq.keys())[:num_keywords]
