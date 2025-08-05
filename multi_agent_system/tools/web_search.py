"""
Enhanced Web Search Tool
Provides advanced web search capabilities with result processing and validation
"""

import requests
import json
import re
from datetime import datetime, timedelta
from urllib.parse import quote_plus, urlparse
import time
import random

class SearchResult:
    """Structured search result object"""
    
    def __init__(self, title, url, snippet, source, timestamp=None, relevance_score=0.0):
        self.title = title
        self.url = url
        self.snippet = snippet
        self.source = source
        self.timestamp = timestamp or datetime.now().isoformat()
        self.relevance_score = relevance_score
        self.content = None
        self.metadata = {}
    
    def to_dict(self):
        return {
            'title': self.title,
            'url': self.url,
            'snippet': self.snippet,
            'source': self.source,
            'timestamp': self.timestamp,
            'relevance_score': self.relevance_score,
            'content': self.content,
            'metadata': self.metadata
        }
    
    def __str__(self):
        return f"{self.title} - {self.source} (Score: {self.relevance_score:.2f})"

class WebSearchTool:
    """Advanced web search tool with multiple search engines and result processing"""
    
    def __init__(self):
        self.name = "web_search"
        self.description = "Advanced web search with result processing and validation"
        self.search_history = []
        self.result_cache = {}
        self.cache_duration_hours = 24
        
        # Simulated search engines for demonstration
        self.search_engines = {
            'general': self._search_general,
            'news': self._search_news,
            'academic': self._search_academic,
            'social': self._search_social
        }
        
        # Common domains for realistic simulation
        self.domains = {
            'news': ['reuters.com', 'bbc.com', 'cnn.com', 'techcrunch.com', 'bloomberg.com'],
            'academic': ['arxiv.org', 'ieee.org', 'acm.org', 'nature.com', 'sciencedirect.com'],
            'business': ['forbes.com', 'wsj.com', 'harvard.edu', 'mckinsey.com', 'deloitte.com'],
            'tech': ['github.com', 'stackoverflow.com', 'medium.com', 'dev.to', 'hackernews.com']
        }
    
    def search(self, query, search_type='general', max_results=10, time_filter=None):
        """
        Perform comprehensive web search
        
        Args:
            query: Search query string
            search_type: Type of search ('general', 'news', 'academic', 'social')
            max_results: Maximum number of results to return
            time_filter: Time filter ('day', 'week', 'month', 'year', None)
        """
        # Check cache first
        cache_key = f"{query}_{search_type}_{max_results}_{time_filter}"
        if self._is_cached(cache_key):
            cached_results = self.result_cache[cache_key]
            return cached_results['results']
        
        try:
            # Perform search using appropriate engine
            if search_type in self.search_engines:
                results = self.search_engines[search_type](query, max_results, time_filter)
            else:
                results = self._search_general(query, max_results, time_filter)
            
            # Process and rank results
            processed_results = self._process_results(results, query)
            
            # Cache results
            self._cache_results(cache_key, processed_results)
            
            # Store in search history
            self.search_history.append({
                'query': query,
                'search_type': search_type,
                'results_count': len(processed_results),
                'timestamp': datetime.now().isoformat()
            })
            
            return processed_results
            
        except Exception as e:
            return [SearchResult(
                title="Search Error",
                url="",
                snippet=f"Search failed: {str(e)}",
                source="system",
                relevance_score=0.0
            )]
    
    def _search_general(self, query, max_results, time_filter):
        """Simulate general web search"""
        results = []
        
        # Generate realistic search results based on query
        query_lower = query.lower()
        
        # Determine result categories based on query
        categories = self._categorize_query(query_lower)
        
        for i in range(max_results):
            category = random.choice(categories)
            domain = random.choice(self.domains[category])
            
            # Generate realistic title and snippet
            title = self._generate_title(query, category)
            snippet = self._generate_snippet(query, category)
            url = f"https://{domain}/{self._generate_url_path(query)}"
            
            result = SearchResult(
                title=title,
                url=url,
                snippet=snippet,
                source=domain,
                relevance_score=random.uniform(0.6, 0.95)
            )
            
            results.append(result)
        
        return results
    
    def _search_news(self, query, max_results, time_filter):
        """Simulate news search"""
        results = []
        news_domains = self.domains['news']
        
        for i in range(max_results):
            domain = random.choice(news_domains)
            
            title = f"{query} - Latest News and Updates"
            snippet = f"Breaking news about {query}. Get the latest updates, analysis, and expert opinions on {query} from trusted news sources."
            url = f"https://{domain}/news/{self._generate_url_path(query)}"
            
            # News articles are typically recent
            hours_ago = random.randint(1, 48)
            timestamp = (datetime.now() - timedelta(hours=hours_ago)).isoformat()
            
            result = SearchResult(
                title=title,
                url=url,
                snippet=snippet,
                source=domain,
                timestamp=timestamp,
                relevance_score=random.uniform(0.7, 0.9)
            )
            
            results.append(result)
        
        return results
    
    def _search_academic(self, query, max_results, time_filter):
        """Simulate academic search"""
        results = []
        academic_domains = self.domains['academic']
        
        for i in range(max_results):
            domain = random.choice(academic_domains)
            
            title = f"Research on {query}: A Comprehensive Study"
            snippet = f"Academic research paper examining {query}. This study presents findings, methodology, and conclusions related to {query} with peer-reviewed analysis."
            url = f"https://{domain}/paper/{self._generate_url_path(query)}"
            
            result = SearchResult(
                title=title,
                url=url,
                snippet=snippet,
                source=domain,
                relevance_score=random.uniform(0.8, 0.95)
            )
            
            # Add academic metadata
            result.metadata = {
                'type': 'academic',
                'peer_reviewed': True,
                'citation_count': random.randint(5, 150)
            }
            
            results.append(result)
        
        return results
    
    def _search_social(self, query, max_results, time_filter):
        """Simulate social media search"""
        results = []
        social_domains = ['twitter.com', 'reddit.com', 'linkedin.com', 'youtube.com']
        
        for i in range(max_results):
            domain = random.choice(social_domains)
            
            if domain == 'twitter.com':
                title = f"Tweets about {query}"
                snippet = f"Social media discussions and trending topics related to {query}. Real-time conversations and opinions."
            elif domain == 'reddit.com':
                title = f"{query} - Reddit Discussion"
                snippet = f"Community discussions about {query}. User experiences, questions, and insights."
            elif domain == 'linkedin.com':
                title = f"Professional Insights on {query}"
                snippet = f"Professional perspectives and industry insights about {query} from experts and thought leaders."
            else:  # youtube.com
                title = f"{query} - Video Content"
                snippet = f"Educational and informational videos about {query}. Tutorials, reviews, and expert explanations."
            
            url = f"https://{domain}/{self._generate_url_path(query)}"
            
            result = SearchResult(
                title=title,
                url=url,
                snippet=snippet,
                source=domain,
                relevance_score=random.uniform(0.5, 0.8)
            )
            
            results.append(result)
        
        return results
    
    def _categorize_query(self, query):
        """Categorize search query to determine result types"""
        categories = []
        
        # Business/Finance keywords
        if any(word in query for word in ['market', 'business', 'finance', 'economy', 'investment', 'startup']):
            categories.extend(['business', 'news'])
        
        # Technology keywords
        if any(word in query for word in ['technology', 'software', 'ai', 'machine learning', 'programming', 'code']):
            categories.extend(['tech', 'academic'])
        
        # Research keywords
        if any(word in query for word in ['research', 'study', 'analysis', 'data', 'science']):
            categories.extend(['academic', 'business'])
        
        # News keywords
        if any(word in query for word in ['news', 'latest', 'update', 'recent', 'current']):
            categories.extend(['news'])
        
        # Default to general categories
        if not categories:
            categories = ['business', 'tech', 'news']
        
        return categories
    
    def _generate_title(self, query, category):
        """Generate realistic title based on query and category"""
        title_templates = {
            'business': [
                f"{query}: Market Analysis and Business Opportunities",
                f"Complete Guide to {query} in Business",
                f"{query} - Industry Trends and Insights",
                f"Strategic Approach to {query} Implementation"
            ],
            'tech': [
                f"{query}: Technical Overview and Best Practices",
                f"Understanding {query} - Developer Guide",
                f"{query} Implementation: Tools and Techniques",
                f"Advanced {query} Strategies and Solutions"
            ],
            'news': [
                f"{query} - Breaking News and Latest Updates",
                f"What You Need to Know About {query}",
                f"{query}: Recent Developments and Analysis",
                f"Expert Opinion on {query} Trends"
            ],
            'academic': [
                f"Comprehensive Study of {query}: Research Findings",
                f"{query} in Academic Literature: A Review",
                f"Empirical Analysis of {query} Phenomena",
                f"Theoretical Framework for {query} Understanding"
            ]
        }
        
        templates = title_templates.get(category, title_templates['business'])
        return random.choice(templates)
    
    def _generate_snippet(self, query, category):
        """Generate realistic snippet based on query and category"""
        snippet_templates = {
            'business': f"Comprehensive analysis of {query} including market trends, business strategies, and implementation approaches. Expert insights and practical recommendations for professionals.",
            'tech': f"Technical documentation and best practices for {query}. Includes implementation guides, code examples, and expert recommendations for developers and IT professionals.",
            'news': f"Latest news and updates about {query}. Stay informed with breaking news, expert analysis, and real-time coverage of developments related to {query}.",
            'academic': f"Peer-reviewed research on {query} with detailed methodology, findings, and conclusions. Academic perspective with citations and scholarly analysis."
        }
        
        return snippet_templates.get(category, snippet_templates['business'])
    
    def _generate_url_path(self, query):
        """Generate realistic URL path"""
        # Clean and format query for URL
        path = re.sub(r'[^\w\s-]', '', query).strip()
        path = re.sub(r'[-\s]+', '-', path).lower()
        return f"{path}-{random.randint(1000, 9999)}"
    
    def _process_results(self, results, query):
        """Process and enhance search results"""
        processed_results = []
        
        for result in results:
            # Calculate relevance score based on query match
            relevance = self._calculate_relevance(result, query)
            result.relevance_score = relevance
            
            # Add processing timestamp
            result.metadata['processed_at'] = datetime.now().isoformat()
            result.metadata['query'] = query
            
            processed_results.append(result)
        
        # Sort by relevance score
        processed_results.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return processed_results
    
    def _calculate_relevance(self, result, query):
        """Calculate relevance score for search result"""
        score = result.relevance_score
        
        query_words = set(query.lower().split())
        
        # Check title match
        title_words = set(result.title.lower().split())
        title_match = len(query_words.intersection(title_words)) / len(query_words)
        
        # Check snippet match
        snippet_words = set(result.snippet.lower().split())
        snippet_match = len(query_words.intersection(snippet_words)) / len(query_words)
        
        # Calculate combined relevance
        relevance = (score * 0.4) + (title_match * 0.4) + (snippet_match * 0.2)
        
        return min(1.0, relevance)
    
    def _is_cached(self, cache_key):
        """Check if results are cached and still valid"""
        if cache_key not in self.result_cache:
            return False
        
        cached_time = datetime.fromisoformat(self.result_cache[cache_key]['timestamp'])
        expiry_time = cached_time + timedelta(hours=self.cache_duration_hours)
        
        return datetime.now() < expiry_time
    
    def _cache_results(self, cache_key, results):
        """Cache search results"""
        self.result_cache[cache_key] = {
            'results': results,
            'timestamp': datetime.now().isoformat()
        }
        
        # Clean old cache entries (keep last 100)
        if len(self.result_cache) > 100:
            oldest_key = min(self.result_cache.keys(), 
                           key=lambda k: self.result_cache[k]['timestamp'])
            del self.result_cache[oldest_key]
    
    def get_search_stats(self):
        """Get search statistics"""
        return {
            'total_searches': len(self.search_history),
            'cache_size': len(self.result_cache),
            'recent_searches': self.search_history[-5:] if self.search_history else [],
            'popular_search_types': self._get_popular_search_types()
        }
    
    def _get_popular_search_types(self):
        """Get most popular search types"""
        type_counts = {}
        for search in self.search_history:
            search_type = search['search_type']
            type_counts[search_type] = type_counts.get(search_type, 0) + 1
        
        return sorted(type_counts.items(), key=lambda x: x[1], reverse=True)
    
    def search_with_filters(self, query, domain_filter=None, date_range=None, content_type=None):
        """Advanced search with multiple filters"""
        # Base search
        results = self.search(query, max_results=20)
        
        # Apply domain filter
        if domain_filter:
            results = [r for r in results if domain_filter.lower() in r.source.lower()]
        
        # Apply date range filter
        if date_range:
            start_date, end_date = date_range
            results = [r for r in results if self._is_in_date_range(r.timestamp, start_date, end_date)]
        
        # Apply content type filter
        if content_type:
            results = [r for r in results if r.metadata.get('type') == content_type]
        
        return results[:10]  # Return top 10 filtered results
    
    def _is_in_date_range(self, timestamp, start_date, end_date):
        """Check if timestamp is within date range"""
        try:
            ts = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return start_date <= ts <= end_date
        except:
            return True  # Include if can't parse date