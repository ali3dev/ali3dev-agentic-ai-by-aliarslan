"""
Tools Package - Advanced utilities for multi-agent system
Provides enhanced capabilities for web search, content processing, and analysis
"""

from .web_search import WebSearchTool, SearchResult
from .content_tools import ContentProcessor, ContentOptimizer, ContentValidator
from .analysis_tools import DataAnalyzer, TrendAnalyzer, InsightGenerator


__all__ = [
    'WebSearchTool', 'SearchResult',
    'ContentProcessor', 'ContentOptimizer', 'ContentValidator',
    'DataAnalyzer', 'TrendAnalyzer', 'InsightGenerator'
]

__version__ = '1.0.0'
__author__ = 'Multi-Agent System Team (Developer (Ali Arslan Khan))'
__license__ = 'MIT License'
__description__ = 'A collection of tools for enhancing multi-agent system capabilities in web search, content processing, and data analysis.'
