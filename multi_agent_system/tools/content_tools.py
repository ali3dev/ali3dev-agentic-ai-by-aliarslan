"""
Content Processing Tools
Advanced utilities for content creation, optimization, and validation
"""

import re
import json
from datetime import datetime
from collections import Counter
import hashlib

class ContentProcessor:
    """Advanced content processing and manipulation"""
    
    def __init__(self):
        self.name = "content_processor"
        self.description = "Advanced content processing and manipulation tools"
        self.processing_history = []
        
        # Content type templates
        self.templates = {
            'blog_post': {
                'structure': ['title', 'introduction', 'main_content', 'conclusion', 'call_to_action'],
                'min_words': 800,
                'max_words': 2500
            },
            'article': {
                'structure': ['headline', 'lead', 'body', 'conclusion'],
                'min_words': 500,
                'max_words': 1500
            },
            'report': {
                'structure': ['executive_summary', 'introduction', 'methodology', 'findings', 'recommendations', 'conclusion'],
                'min_words': 1500,
                'max_words': 5000
            },
            'social_post': {
                'structure': ['hook', 'content', 'call_to_action'],
                'min_words': 50,
                'max_words': 280
            }
        }
    
    def extract_structure(self, content):
        """Extract content structure and components"""
        structure = {
            'word_count': len(content.split()),
            'character_count': len(content),
            'paragraph_count': len([p for p in content.split('\n\n') if p.strip()]),
            'sentence_count': len(re.findall(r'[.!?]+', content)),
            'headings': self._extract_headings(content),
            'links': self._extract_links(content),
            'images': self._extract_images(content),
            'lists': self._extract_lists(content),
            'quotes': self._extract_quotes(content)
        }
        
        return structure
    
    def _extract_headings(self, content):
        """Extract headings from content"""
        headings = []
        
        # Markdown headings
        md_headings = re.findall(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)
        for level, text in md_headings:
            headings.append({
                'level': len(level),
                'text': text.strip(),
                'type': 'markdown'
            })
        
        # HTML headings
        html_headings = re.findall(r'<h([1-6])>(.*?)</h[1-6]>', content, re.IGNORECASE)
        for level, text in html_headings:
            headings.append({
                'level': int(level),
                'text': text.strip(),
                'type': 'html'
            })
        
        return headings
    
    def _extract_links(self, content):
        """Extract links from content"""
        links = []
        
        # Markdown links
        md_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        for text, url in md_links:
            links.append({'text': text, 'url': url, 'type': 'markdown'})
        
        # HTML links
        html_links = re.findall(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', content, re.IGNORECASE)
        for url, text in html_links:
            links.append({'text': text, 'url': url, 'type': 'html'})
        
        # Plain URLs
        urls = re.findall(r'https?://[^\s]+', content)
        for url in urls:
            links.append({'text': url, 'url': url, 'type': 'plain'})
        
        return links
    
    def _extract_images(self, content):
        """Extract image references from content"""
        images = []
        
        # Markdown images
        md_images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content)
        for alt, src in md_images:
            images.append({'alt': alt, 'src': src, 'type': 'markdown'})
        
        # HTML images
        html_images = re.findall(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', content, re.IGNORECASE)
        for src in html_images:
            images.append({'alt': '', 'src': src, 'type': 'html'})
        
        return images
    
    def _extract_lists(self, content):
        """Extract lists from content"""
        lists = []
        
        # Markdown lists
        md_list_items = re.findall(r'^[\s]*[-*+]\s+(.+)$', content, re.MULTILINE)
        if md_list_items:
            lists.append({
                'type': 'unordered',
                'items': md_list_items,
                'format': 'markdown'
            })
        
        # Numbered lists
        num_list_items = re.findall(r'^\s*\d+\.\s+(.+)$', content, re.MULTILINE)
        if num_list_items:
            lists.append({
                'type': 'ordered',
                'items': num_list_items,
                'format': 'markdown'
            })
        
        return lists
    
    def _extract_quotes(self, content):
        """Extract quotes from content"""
        quotes = []
        
        # Markdown blockquotes
        md_quotes = re.findall(r'^>\s+(.+)$', content, re.MULTILINE)
        for quote in md_quotes:
            quotes.append({'text': quote, 'type': 'blockquote'})
        
        # Quoted text
        quoted_text = re.findall(r'["""]([^"""]+)["""]', content)
        for quote in quoted_text:
            quotes.append({'text': quote, 'type': 'inline'})
        
        return quotes
    
    def format_content(self, content, target_format='markdown'):
        """Format content to target format"""
        if target_format == 'markdown':
            return self._format_to_markdown(content)
        elif target_format == 'html':
            return self._format_to_html(content)
        elif target_format == 'plain':
            return self._format_to_plain(content)
        else:
            return content
    
    def _format_to_markdown(self, content):
        """Convert content to markdown format"""
        # Already markdown or plain text
        if not re.search(r'<[^>]+>', content):
            return content
        
        # Convert HTML to markdown (simplified)
        formatted = content
        
        # Convert headings
        for i in range(1, 7):
            formatted = re.sub(rf'<h{i}>(.*?)</h{i}>', rf'{"#" * i} \1', formatted, flags=re.IGNORECASE)
        
        # Convert bold and italic
        formatted = re.sub(r'<strong>(.*?)</strong>', r'**\1**', formatted, flags=re.IGNORECASE)
        formatted = re.sub(r'<em>(.*?)</em>', r'*\1*', formatted, flags=re.IGNORECASE)
        
        # Convert links
        formatted = re.sub(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', r'[\2](\1)', formatted, flags=re.IGNORECASE)
        
        # Remove remaining HTML tags
        formatted = re.sub(r'<[^>]+>', '', formatted)
        
        return formatted.strip()
    
    def _format_to_html(self, content):
        """Convert content to HTML format"""
        if re.search(r'<[^>]+>', content):
            return content  # Already HTML
        
        # Convert markdown to HTML (simplified)
        formatted = content
        
        # Convert headings
        for i in range(6, 0, -1):
            pattern = rf'^{"#" * i}\s+(.+)$'
            replacement = rf'<h{i}>\1</h{i}>'
            formatted = re.sub(pattern, replacement, formatted, flags=re.MULTILINE)
        
        # Convert bold and italic
        formatted = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted)
        formatted = re.sub(r'\*(.*?)\*', r'<em>\1</em>', formatted)
        
        # Convert links
        formatted = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', formatted)
        
        # Convert paragraphs
        paragraphs = formatted.split('\n\n')
        formatted = '\n'.join([f'<p>{p}</p>' for p in paragraphs if p.strip()])
        
        return formatted
    
    def _format_to_plain(self, content):
        """Convert content to plain text"""
        # Remove HTML tags
        plain = re.sub(r'<[^>]+>', '', content)
        
        # Remove markdown formatting
        plain = re.sub(r'\*\*(.*?)\*\*', r'\1', plain)  # Bold
        plain = re.sub(r'\*(.*?)\*', r'\1', plain)      # Italic
        plain = re.sub(r'#{1,6}\s+', '', plain)         # Headings
        plain = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', plain)  # Links
        
        return plain.strip()
    
    def optimize_readability(self, content):
        """Optimize content for readability"""
        optimizations = []
        
        # Check sentence length
        sentences = re.split(r'[.!?]+', content)
        long_sentences = [s for s in sentences if len(s.split()) > 25]
        if long_sentences:
            optimizations.append({
                'type': 'sentence_length',
                'issue': f'Found {len(long_sentences)} sentences with >25 words',
                'suggestion': 'Break long sentences into shorter ones'
            })
        
        # Check paragraph length
        paragraphs = [p for p in content.split('\n\n') if p.strip()]
        long_paragraphs = [p for p in paragraphs if len(p.split()) > 150]
        if long_paragraphs:
            optimizations.append({
                'type': 'paragraph_length',
                'issue': f'Found {len(long_paragraphs)} paragraphs with >150 words',
                'suggestion': 'Split long paragraphs for better readability'
            })
        
        # Check passive voice (simplified detection)
        passive_indicators = ['was', 'were', 'been', 'is being', 'are being']
        passive_count = sum(content.lower().count(indicator) for indicator in passive_indicators)
        total_sentences = len([s for s in sentences if s.strip()])
        
        if total_sentences > 0 and (passive_count / total_sentences) > 0.2:
            optimizations.append({
                'type': 'passive_voice',
                'issue': f'High passive voice usage ({passive_count} instances)',
                'suggestion': 'Use more active voice for engagement'
            })
        
        return optimizations
    
    def generate_summary(self, content, max_sentences=3):
        """Generate content summary"""
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.split()) > 5]
        
        if not sentences:
            return "No content to summarize."
        
        # Simple extractive summarization
        # Score sentences by word frequency and position
        word_freq = Counter()
        for sentence in sentences:
            words = [w.lower() for w in sentence.split() if w.isalpha()]
            word_freq.update(words)
        
        # Score sentences
        sentence_scores = []
        for i, sentence in enumerate(sentences):
            words = [w.lower() for w in sentence.split() if w.isalpha()]
            score = sum(word_freq[word] for word in words)
            
            # Boost score for earlier sentences
            position_boost = 1.0 - (i / len(sentences)) * 0.3
            score *= position_boost
            
            sentence_scores.append((score, sentence))
        
        # Select top sentences
        sentence_scores.sort(reverse=True)
        summary_sentences = [sentence for _, sentence in sentence_scores[:max_sentences]]
        
        # Reorder by original position
        original_order = []
        for sentence in summary_sentences:
            original_order.append((sentences.index(sentence), sentence))
        
        original_order.sort()
        summary = '. '.join([sentence for _, sentence in original_order]) + '.'
        
        return summary
    
    def validate_content_type(self, content, content_type):
        """Validate content against type requirements"""
        if content_type not in self.templates:
            return {'valid': False, 'error': f'Unknown content type: {content_type}'}
        
        template = self.templates[content_type]
        structure = self.extract_structure(content)
        
        issues = []
        
        # Check word count
        word_count = structure['word_count']
        if word_count < template['min_words']:
            issues.append(f"Too short: {word_count} words (minimum: {template['min_words']})")
        elif word_count > template['max_words']:
            issues.append(f"Too long: {word_count} words (maximum: {template['max_words']})")
        
        # Check structure requirements
        required_sections = template['structure']
        content_lower = content.lower()
        
        missing_sections = []
        for section in required_sections:
            # Simple check for section presence
            section_indicators = {
                'title': ['title', '#', 'h1'],
                'introduction': ['introduction', 'intro', 'overview'],
                'main_content': ['content', 'body', 'main'],
                'conclusion': ['conclusion', 'summary', 'final'],
                'call_to_action': ['call to action', 'cta', 'contact'],
                'executive_summary': ['executive summary', 'summary'],
                'methodology': ['methodology', 'method', 'approach'],
                'findings': ['findings', 'results', 'data'],
                'recommendations': ['recommendations', 'suggest']
            }
            
            indicators = section_indicators.get(section, [section])
            if not any(indicator in content_lower for indicator in indicators):
                missing_sections.append(section)
        
        if missing_sections:
            issues.append(f"Missing sections: {', '.join(missing_sections)}")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'word_count': word_count,
            'structure_analysis': structure
        }

class ContentOptimizer:
    """Content optimization for SEO and engagement"""
    
    def __init__(self):
        self.name = "content_optimizer"
        self.description = "SEO and engagement optimization tools"
    
    def optimize_for_seo(self, content, target_keywords=None, meta_description=None):
        """Optimize content for search engines"""
        optimizations = {
            'keyword_analysis': {},
            'seo_score': 0,
            'recommendations': []
        }
        if target_keywords:
            # Analyze keyword density
            content_words = content.lower().split()
            total_words = len(content_words)
            for keyword in target_keywords:
                keyword_lower = keyword.lower()
                count = content.lower().count(keyword_lower)
                density = (count / total_words) * 100 if total_words > 0 else 0
                optimizations['keyword_analysis'][keyword] = {
                    'count': count,
                    'density': round(density, 2),
                    'optimal_density': '1-3%'
                }
                # SEO recommendations
                if density < 1:
                    optimizations['recommendations'].append(f"Increase '{keyword}' usage (current: {density:.1f}%)")
                elif density > 3:
                    optimizations['recommendations'].append(f"Reduce '{keyword}' usage (current: {density:.1f}%)")
        # Check headings for keywords
        headings = re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
        found_keyword_in_heading = False
        for heading in headings:
            for keyword in target_keywords or []:
                if keyword.lower() in heading.lower():
                    optimizations['recommendations'].append(f"Heading contains target keyword: '{keyword}'")
                    found_keyword_in_heading = True
                    break
        if not found_keyword_in_heading and target_keywords:
            optimizations['recommendations'].append("Consider adding target keywords to headings")
        # Meta description
        if meta_description:
            if len(meta_description) > 160:
                optimizations['recommendations'].append("Meta description is too long (should be <= 160 characters)")
            elif len(meta_description) < 50:
                optimizations['recommendations'].append("Meta description is too short (should be >= 50 characters)")
            else:
                optimizations['recommendations'].append("Meta description length is optimal")
        # Simple SEO score (out of 100)
        score = 70
        if target_keywords:
            for keyword in target_keywords:
                density = optimizations['keyword_analysis'][keyword]['density']
                if 1 <= density <= 3:
                    score += 5
                else:
                    score -= 5
        if meta_description and 50 <= len(meta_description) <= 160:
            score += 5
        optimizations['seo_score'] = min(max(score, 0), 100)
        return optimizations

    def optimize_for_engagement(self, content):
        """Suggest improvements for engagement (hooks, CTAs, questions, etc.)"""
        suggestions = []
        # Check for hook (first sentence/paragraph)
        paragraphs = [p for p in content.split('\n\n') if p.strip()]
        if paragraphs:
            first = paragraphs[0].strip()
            if len(first.split()) < 8:
                suggestions.append("Opening is too short; consider a stronger hook.")
            elif not re.search(r'[?!]$', first):
                suggestions.append("Consider starting with a question or bold statement to hook readers.")
        # Check for call to action
        if not re.search(r'(call to action|cta|contact|subscribe|learn more|sign up|follow|share)', content, re.IGNORECASE):
            suggestions.append("Add a clear call to action (CTA) to guide readers.")
        # Check for questions
        if not re.search(r'\?', content):
            suggestions.append("Engage readers by asking questions.")
        # Check for use of lists
        if not re.search(r'^[-*+]\s+.+$', content, re.MULTILINE):
            suggestions.append("Use bullet or numbered lists to improve readability.")
        return suggestions

    def optimize_readability(self, content):
        """Suggest improvements for readability (sentence/paragraph length, passive voice)"""
        suggestions = []
        # Sentence length
        sentences = re.split(r'[.!?]+', content)
        long_sentences = [s for s in sentences if len(s.split()) > 25]
        if long_sentences:
            suggestions.append(f"Found {len(long_sentences)} sentences with >25 words. Break them up for clarity.")
        # Paragraph length
        paragraphs = [p for p in content.split('\n\n') if p.strip()]
        long_paragraphs = [p for p in paragraphs if len(p.split()) > 150]
        if long_paragraphs:
            suggestions.append(f"Found {len(long_paragraphs)} paragraphs with >150 words. Split them for better readability.")
        # Passive voice
        passive_indicators = ['was', 'were', 'been', 'is being', 'are being']
        passive_count = sum(content.lower().count(ind) for ind in passive_indicators)
        total_sentences = len([s for s in sentences if s.strip()])
        if total_sentences > 0 and (passive_count / total_sentences) > 0.2:
            suggestions.append(f"High passive voice usage ({passive_count} instances). Use more active voice.")
        return suggestions

    def suggest_improvements(self, content, target_keywords=None, meta_description=None):
        """Aggregate all suggestions for SEO, engagement, and readability."""
        suggestions = []
        seo = self.optimize_for_seo(content, target_keywords, meta_description)
        engagement = self.optimize_for_engagement(content)
        readability = self.optimize_readability(content)
        suggestions.extend(seo['recommendations'])
        suggestions.extend(engagement)
        suggestions.extend(readability)
        return suggestions


# ContentValidator class for content validation and quality checks
class ContentValidator:
    """Content validation for quality, structure, and compliance."""

    def __init__(self):
        self.name = "content_validator"
        self.description = "Validates content for quality, structure, and compliance"

    def validate_content(self, content):
        """Validate content and return a quality report."""
        return self.validate_quality(content)

    def validate_quality(self, content):
        """Validate content quality and return a report."""
        issues = []
        score = 100

        # Check for minimum length
        word_count = len(content.split())
        if word_count < 100:
            issues.append("Content is too short (<100 words)")
            score -= 20

        # Check for missing punctuation
        if not any(p in content for p in ".!?"):
            issues.append("No sentence-ending punctuation found")
            score -= 10

        # Check for repeated words
        words = content.lower().split()
        repeated = [word for word in set(words) if words.count(word) > 5]
        if repeated:
            issues.append(f"Repeated words: {', '.join(repeated)}")
            score -= 10

        # Check for forbidden words (example)
        forbidden = ['lorem', 'ipsum', 'dummy']
        found_forbidden = [w for w in forbidden if w in content.lower()]
        if found_forbidden:
            issues.append(f"Forbidden words found: {', '.join(found_forbidden)}")
            score -= 10

        # Check for structure (simple)
        if len(content) < 50 or len(content.split('\n')) < 2:
            issues.append("Content lacks structure (too short or no paragraphs)")
            score -= 10

        return {
            "overall_score": max(score, 0),
            "issues": issues,
            "word_count": word_count
        }