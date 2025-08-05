import re
from collections import Counter


class TextAnalyzerTool:
    def __init__(self):
        self.name = "text_analyzer"
        self.description = "Analyze text for metrics and insights"

    def analyze(self, text):
        """
        Comprehensive text analysis
        """
        # Basic metrics
        word_count = len(text.split())
        char_count =  len(text)
        sentence_count = len(re.findall(r'[.!?]', text))

        # Word frequency
        words = re.findall(r'\b\w+\b', text.lower())
        word_freq = Counter(words)
        most_common = word_freq.most_common(3)

        #Simple sentiment analysis
        positive_words = [
            'good', 'great', 'excellent', 'amazing', 'wonderful', 
            'fantastic', 'awesome', 'love', 'best', 'perfect'
        ]
        negative_words = [
            'bad', 'terrible', 'awful', 'horrible', 'poor', 
            'disappointing', 'worst', 'hate', 'boring', 'ugly'
        ]

        text_lower = text.lower()
        pos_score = sum(1 for word in positive_words if word in text_lower)

        neg_score = sum(1 for word in negative_words
        if word in text_lower)

        if pos_score > neg_score:
            sentiment = "Positive"
        elif neg_score > pos_score:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        analysis = f"""
                    Text Analysis Results:
                    ├── Word Count: {word_count}
                    ├── Character Count: {char_count}
                    ├── Sentence Count: {sentence_count}
                    ├── Sentiment: {sentiment} (Pos: {pos_score}, Neg: {neg_score})
                    └── Most Common Words: {', '.join([f"{word}({count})" for word, count in most_common])}
                            """
        
        return analysis.strip()