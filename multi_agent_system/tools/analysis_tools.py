"""
Advanced Analysis Tools
Data analysis, trend identification, and insight generation utilities
"""

import json
import re
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import statistics
import random

class DataAnalyzer:
    """Advanced data analysis and processing"""
    
    def __init__(self):
        self.name = "data_analyzer"
        self.description = "Advanced data analysis and statistical processing"
        self.analysis_history = []
        
    def analyze_dataset(self, data, analysis_type='comprehensive'):
        """Comprehensive dataset analysis"""
        if isinstance(data, str):
            # Try to parse as JSON
            try:
                data = json.loads(data)
            except:
                # Treat as text data
                return self._analyze_text_data(data)
        
        if isinstance(data, list):
            return self._analyze_list_data(data)
        elif isinstance(data, dict):
            return self._analyze_dict_data(data)
        else:
            return {'error': 'Unsupported data format'}
    
    def _analyze_text_data(self, text):
        """Analyze textual data"""
        analysis = {
            'data_type': 'text',
            'basic_stats': {},
            'content_analysis': {},
            'insights': []
        }
        
        # Basic statistics
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        paragraphs = [p for p in text.split('\n\n') if p.strip()]
        
        analysis['basic_stats'] = {
            'word_count': len(words),
            'unique_words': len(set(words)),
            'sentence_count': len([s for s in sentences if s.strip()]),
            'paragraph_count': len(paragraphs),
            'avg_words_per_sentence': len(words) / len(sentences) if sentences else 0,
            'lexical_diversity': len(set(words)) / len(words) if words else 0
        }
        
        # Content analysis
        word_freq = Counter(word.lower().strip('.,!?";') for word in words if word.isalpha())
        
        analysis['content_analysis'] = {
            'most_common_words': word_freq.most_common(10),
            'word_frequency_distribution': dict(word_freq),
            'sentiment_indicators': self._analyze_sentiment_indicators(text),
            'topics': self._extract_topics(text)
        }
        
        # Generate insights
        if analysis['basic_stats']['avg_words_per_sentence'] > 20:
            analysis['insights'].append("Text has complex sentence structure")
        
        if analysis['basic_stats']['lexical_diversity'] > 0.7:
            analysis['insights'].append("High vocabulary diversity detected")
        
        return analysis
    
    def _analyze_list_data(self, data_list):
        """Analyze list/array data"""
        analysis = {
            'data_type': 'list',
            'basic_stats': {},
            'distribution': {},
            'insights': []
        }
        
        if not data_list:
            return analysis
        
        # Determine data types in list
        data_types = Counter(type(item).__name__ for item in data_list)
        analysis['basic_stats']['data_types'] = dict(data_types)
        analysis['basic_stats']['length'] = len(data_list)
        
        # Analyze numeric data
        numeric_data = [item for item in data_list if isinstance(item, (int, float))]
        if numeric_data:
            analysis['basic_stats']['numeric_stats'] = {
                'count': len(numeric_data),
                'mean': statistics.mean(numeric_data),
                'median': statistics.median(numeric_data),
                'min': min(numeric_data),
                'max': max(numeric_data),
                'std_dev': statistics.stdev(numeric_data) if len(numeric_data) > 1 else 0
            }
        
        # Analyze string data
        string_data = [item for item in data_list if isinstance(item, str)]
        if string_data:
            analysis['basic_stats']['string_stats'] = {
                'count': len(string_data),
                'avg_length': sum(len(s) for s in string_data) / len(string_data),
                'unique_count': len(set(string_data))
            }
        
        # Value distribution
        if len(set(data_list)) < len(data_list) / 2:  # Many repeated values
            value_counts = Counter(data_list)
            analysis['distribution']['value_counts'] = dict(value_counts.most_common(10))
        
        return analysis
    
    def _analyze_dict_data(self, data_dict):
        """Analyze dictionary/object data"""
        analysis = {
            'data_type': 'dictionary',
            'structure': {},
            'field_analysis': {},
            'insights': []
        }
        
        # Structure analysis
        analysis['structure'] = {
            'field_count': len(data_dict),
            'field_names': list(data_dict.keys()),
            'nested_fields': sum(1 for v in data_dict.values() if isinstance(v, (dict, list)))
        }
        
        # Analyze each field
        for key, value in data_dict.items():
            field_analysis = {
                'type': type(value).__name__,
                'sample_value': str(value)[:100] if isinstance(value, str) else value
            }
            
            if isinstance(value, list):
                field_analysis['list_length'] = len(value)
                if value:
                    field_analysis['element_types'] = list(set(type(item).__name__ for item in value))
            
            elif isinstance(value, dict):
                field_analysis['nested_keys'] = list(value.keys())
            
            analysis['field_analysis'][key] = field_analysis
        
        return analysis
    
    def _analyze_sentiment_indicators(self, text):
        """Simple sentiment analysis"""
        positive_words = [
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
            'love', 'like', 'enjoy', 'happy', 'pleased', 'satisfied', 'perfect'
        ]
        
        negative_words = [
            'bad', 'terrible', 'awful', 'horrible', 'hate', 'dislike',
            'disappointed', 'frustrated', 'angry', 'sad', 'poor', 'worst'
        ]
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        return {
            'positive_indicators': positive_count,
            'negative_indicators': negative_count,
            'sentiment_ratio': positive_count / (positive_count + negative_count) if (positive_count + negative_count) > 0 else 0.5
        }
    
    def _extract_topics(self, text):
        """Extract main topics from text"""
        # Simple topic extraction based on word frequency
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        
        # Filter out common words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'
        }
        
        filtered_words = [word for word in words if len(word) > 3 and word not in stop_words]
        word_freq = Counter(filtered_words)
        
        return [word for word, count in word_freq.most_common(5)]
    
    def statistical_analysis(self, data, metrics=['mean', 'median', 'std', 'correlation']):
        """Perform statistical analysis on numerical data"""
        if not isinstance(data, list) or not all(isinstance(x, (int, float)) for x in data):
            return {'error': 'Data must be a list of numbers'}
        
        if len(data) < 2:
            return {'error': 'Need at least 2 data points'}
        
        stats = {}
        
        if 'mean' in metrics:
            stats['mean'] = statistics.mean(data)
        
        if 'median' in metrics:
            stats['median'] = statistics.median(data)
        
        if 'std' in metrics:
            stats['standard_deviation'] = statistics.stdev(data)
        
        if 'variance' in metrics:
            stats['variance'] = statistics.variance(data)
        
        if 'range' in metrics:
            stats['range'] = {
                'min': min(data),
                'max': max(data),
                'span': max(data) - min(data)
            }
        
        if 'quartiles' in metrics:
            sorted_data = sorted(data)
            n = len(sorted_data)
            stats['quartiles'] = {
                'q1': sorted_data[n//4],
                'q2': statistics.median(data),
                'q3': sorted_data[3*n//4]
            }
        
        return stats
    
    def comparative_analysis(self, dataset1, dataset2, comparison_type='statistical'):
        """Compare two datasets"""
        comparison = {
            'comparison_type': comparison_type,
            'dataset1_stats': {},
            'dataset2_stats': {},
            'differences': {},
            'insights': []
        }
        
        # Analyze both datasets
        stats1 = self.analyze_dataset(dataset1)
        stats2 = self.analyze_dataset(dataset2)
        
        comparison['dataset1_stats'] = stats1
        comparison['dataset2_stats'] = stats2
        
        # Compare statistics
        if comparison_type == 'statistical' and isinstance(dataset1, list) and isinstance(dataset2, list):
            numeric1 = [x for x in dataset1 if isinstance(x, (int, float))]
            numeric2 = [x for x in dataset2 if isinstance(x, (int, float))]
            
            if numeric1 and numeric2:
                mean1 = statistics.mean(numeric1)
                mean2 = statistics.mean(numeric2)
                
                comparison['differences'] = {
                    'mean_difference': mean2 - mean1,
                    'mean_percentage_change': ((mean2 - mean1) / mean1) * 100 if mean1 != 0 else 0,
                    'size_difference': len(dataset2) - len(dataset1)
                }
                
                # Generate insights
                if abs(comparison['differences']['mean_percentage_change']) > 10:
                    comparison['insights'].append(f"Significant mean difference: {comparison['differences']['mean_percentage_change']:.1f}%")
                
                if comparison['differences']['size_difference'] != 0:
                    comparison['insights'].append(f"Dataset size difference: {comparison['differences']['size_difference']} items")
        
        return comparison

class TrendAnalyzer:
    def _detect_anomalies(self, data):
        """Detect simple anomalies in time series data (e.g., outliers)"""
        if not data or len(data) < 3:
            return []
        mean = sum(data) / len(data)
        std = (sum((x - mean) ** 2 for x in data) / len(data)) ** 0.5
        anomalies = []
        for i, value in enumerate(data):
            if abs(value - mean) > 2 * std:
                anomalies.append({'index': i, 'value': value, 'reason': 'outlier'})
        return anomalies
    """Trend analysis and pattern recognition"""
    
    def __init__(self):
        self.name = "trend_analyzer"
        self.description = "Trend analysis and pattern recognition tools"
    
    def identify_trends(self, time_series_data, time_period='monthly'):
        """Identify trends in time series data"""
        if not isinstance(time_series_data, list):
            return {'error': 'Time series data must be a list'}
        
        trends = {
            'overall_trend': 'stable',
            'trend_strength': 0,
            'patterns': [],
            'anomalies': [],
            'seasonal_patterns': {},
            'forecast': []
        }
        
        # Simple trend analysis
        if len(time_series_data) < 3:
            return trends
        
        # Calculate moving averages
        window_size = min(3, len(time_series_data) // 3)
        moving_averages = []
        
        for i in range(len(time_series_data) - window_size + 1):
            avg = sum(time_series_data[i:i+window_size]) / window_size
            moving_averages.append(avg)
        
        # Determine overall trend
        if moving_averages:
            first_avg = moving_averages[0]
            last_avg = moving_averages[-1]
            
            change_percentage = ((last_avg - first_avg) / first_avg) * 100 if first_avg != 0 else 0
            
            if change_percentage > 5:
                trends['overall_trend'] = 'increasing'
                trends['trend_strength'] = min(100, abs(change_percentage))
            elif change_percentage < -5:
                trends['overall_trend'] = 'decreasing'
                trends['trend_strength'] = min(100, abs(change_percentage))
            else:
                trends['overall_trend'] = 'stable'
                trends['trend_strength'] = abs(change_percentage)
        
        # Identify patterns
        trends['patterns'] = self._identify_patterns(time_series_data)
        
        # Detect anomalies
        trends['anomalies'] = self._detect_anomalies(time_series_data)
        
        # Simple forecast (linear projection)
        if len(time_series_data) >= 5:
            recent_trend = (time_series_data[-1] - time_series_data[-3]) / 2
            forecast_points = 3
            
            for i in range(1, forecast_points + 1):
                forecast_value = time_series_data[-1] + (recent_trend * i)
                trends['forecast'].append(round(forecast_value, 2))
        
        return trends
    
    def _identify_patterns(self, data):
        """Identify common patterns in data"""
        patterns = []
        
        if len(data) < 4:
            return patterns
        
        # Check for cycles
        differences = [data[i+1] - data[i] for i in range(len(data)-1)]
        
        # Look for alternating pattern
        alternating = True
        for i in range(len(differences)-1):
            if (differences[i] > 0) == (differences[i+1] > 0):
                alternating = False
                break
        
        if alternating:
            patterns.append({
                'type': 'alternating',
                'description': 'Data alternates between increases and decreases'
            })
        
        # Look for consistent growth/decline
        consistent_growth = all(d > 0 for d in differences)
        consistent_decline = all(d < 0 for d in differences)
        
        if consistent_growth:
            patterns.append({
                'type': 'consistent_growth',
                'description': 'Consistent upward trend'
            })
        if consistent_decline:
            patterns.append({
                'type': 'consistent_decline',
                'description': 'Consistent downward trend'
            })
        return patterns

# Add missing InsightGenerator class
class InsightGenerator:
    """Business and data insight generation utility."""
    def __init__(self):
        self.name = "insight_generator"
        self.description = "Generates business and data insights from analysis results."

    def generate_business_insights(self, analysis_result):
        """Generate business insights from analysis results (stub logic)."""
        # This is a placeholder. You can expand this logic as needed.
        if isinstance(analysis_result, dict):
            return "Key insights: " + ", ".join(f"{k}: {v}" for k, v in analysis_result.items() if isinstance(v, (int, float, str)))
        elif isinstance(analysis_result, list):
            return f"List of {len(analysis_result)} items analyzed."
        elif isinstance(analysis_result, str):
            return f"Insight: {analysis_result[:100]}..."
        else:
            return "No significant insights generated."