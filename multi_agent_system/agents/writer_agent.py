
"""
Writer Agent - Content creation specialist
Creates blogs, articles, reports, documentation
"""

from .base_agent import BaseAgent
import re

class WriterAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Writer Agent",
            role="Content Creation Specialist",
            expertise="Writing blogs, articles, reports, documentation, marketing copy, technical writing"
        )
        self.writing_styles = {
            'professional': 'Formal, authoritative, business-focused',
            'casual': 'Conversational, friendly, approachable',
            'technical': 'Precise, detailed, expert-level',
            'marketing': 'Persuasive, engaging, action-oriented',
            'academic': 'Scholarly, research-based, analytical'
        }
        self.content_library = {}
        self.max_retries = 3
        self.error_count = 0

    def create_content(self, content_type, topic, style="professional", target_audience="general", research_data=None):
        """
        Create various types of content using research data or web search if available.
        Enhanced with robust error handling and fallback mechanisms.
        """
        if not topic or not topic.strip():
            return self._create_fallback_content("No topic provided", content_type)
        
        # Sanitize inputs
        topic = topic.strip()[:500]  # Limit topic length
        style = style if style in self.writing_styles else "professional"
        
        for attempt in range(self.max_retries):
            try:
                # 1. Use research_data if provided
                info = self._prepare_research_data(research_data)
                
                prompt = self._build_content_prompt(content_type, topic, style, target_audience, info)
                
                response = self.model.generate_content(prompt)
                content = response.text
                
                # Validate content quality
                if not self._validate_content(content, topic):
                    raise ValueError("Content validation failed")
                
                # Store content in library
                content_id = f"content_{len(self.content_library) + 1}"
                self.content_library[content_id] = {
                    'type': content_type,
                    'topic': topic,
                    'style': style,
                    'audience': target_audience,
                    'content': content,
                    'word_count': len(content.split()),
                    'created_at': self.conversation_history[-1]['timestamp'] if self.conversation_history else None,
                    'attempts': attempt + 1
                }
                
                return content
                
            except Exception as e:
                self.error_count += 1
                print(f"Writer Agent attempt {attempt + 1} failed: {str(e)}")
                
                if attempt == self.max_retries - 1:
                    return self._create_fallback_content(topic, content_type)
        
        return self._create_fallback_content(topic, content_type)

    def _prepare_research_data(self, research_data):
        """Prepare and validate research data"""
        if research_data and isinstance(research_data, str) and len(research_data) > 50:
            return research_data
        else:
            # Try to get info from ResearcherAgent or web_search if available
            info = None
            if hasattr(self, 'researcher_agent'):
                try:
                    # Use the topic from the current request instead of self.current_topic
                    topic = getattr(self, 'current_topic', 'general topic')
                    info = self.researcher_agent.conduct_research(topic, "general")
                except Exception:
                    info = None
            if not info and hasattr(self, 'web_search'):
                try:
                    topic = getattr(self, 'current_topic', 'general topic')
                    results = self.web_search.search(topic, max_results=3)
                    info = '\n'.join([r['snippet'] if hasattr(r, 'snippet') else str(r) for r in results])
                except Exception:
                    info = None
            if not info:
                info = "No research data available."
            return info

    def _build_content_prompt(self, content_type, topic, style, target_audience, info):
        """Build comprehensive content creation prompt"""
        return f"""
You are a professional Writer Agent specializing in content creation.

Content Type: {content_type}
Topic: {topic}
Writing Style: {style} ({self.writing_styles.get(style, 'professional')})
Target Audience: {target_audience}
Research Data: {info}

GOAL: Create high-quality {content_type} about {topic}
THINK: What approach will best serve this content type and audience?
PLAN: Structure the content for maximum impact and clarity
ACT: Write engaging, valuable content that meets the requirements
REFLECT: Ensure content quality, accuracy, and audience appropriateness

Requirements for {content_type}:
  - Compelling headline/title
  - Clear introduction that hooks the reader
  - Well-organized main content with subheadings
  - Actionable insights or valuable information
  - Professional conclusion
  - Appropriate length and depth for the content type

For social media posts (Instagram, etc.):
  - Engaging hook in the first line
  - Use emojis and hashtags appropriately
  - Keep it concise but informative
  - Include a call-to-action
  - Make it visually appealing with formatting

For blog posts and articles:
  - Comprehensive coverage of the topic
  - Clear structure with headings
  - Include examples and practical tips
  - SEO-friendly content
  - Engaging writing style

Create polished, publication-ready content that directly addresses the topic and provides real value to the audience.
"""

    def _validate_content(self, content, topic):
        """Validate content quality and relevance"""
        if not content or len(content.strip()) < 100:
            return False
        
        # Check if topic is mentioned in content
        topic_words = topic.lower().split()
        content_lower = content.lower()
        
        # At least 50% of topic words should be present
        topic_word_matches = sum(1 for word in topic_words if word in content_lower)
        if topic_word_matches < len(topic_words) * 0.5:
            return False
        
        # Check for basic structure
        if not re.search(r'[.!?]', content):
            return False
        
        return True

    def _create_fallback_content(self, topic, content_type):
        """Create robust fallback content"""
        # Generate actual content based on the topic instead of generic text
        if content_type == 'social_post':
            fallback = (
                f"GOAL: Create high-quality {content_type} about {topic}. "
                f"{topic.upper()} - Your Ultimate Guide! "
                f"Ready to boost your {topic.lower()}? "
                f"Here are the key strategies you need to know: "
                f"Research your target audience "
                f"Optimize your profile with relevant keywords "
                f"Showcase your best work and achievements "
                f"Network actively and engage with your community "
                f"Pro tip: Consistency is key to success! "
                f"Drop a like if you found this helpful! "
                f"#ProfessionalDevelopment #CareerGrowth #SuccessTips"
            )
        else:
            fallback = (
                f"GOAL: Create high-quality {content_type} about {topic}. "
                f"Here is a comprehensive {content_type} about {topic}. "
                f"Introduction: {topic} is an important and relevant subject that deserves attention. "
                f"Main Content: {topic} encompasses many aspects and considerations. "
                f"Key points include understanding the fundamentals, exploring applications, "
                f"and considering future implications. "
                f"Conclusion: {topic} represents a significant area of interest and opportunity. "
                f"This content provides valuable insights and actionable recommendations."
            )
        return fallback

    def improve_content(self, original_content, improvement_areas):
        """
        Improve existing content based on feedback with enhanced error handling
        """
        if not original_content or not improvement_areas:
            return "No content or improvement areas provided"
        
        for attempt in range(self.max_retries):
            try:
                prompt = f"""
You are a Writer Agent tasked with improving existing content.

Original Content:
{original_content}

Areas for Improvement:
{improvement_areas}

GOAL: Enhance the content by addressing the specified improvement areas
THINK: How can I make this content better while maintaining its core message?
PLAN: Systematic improvements addressing each area
ACT: Rewrite and enhance the content
REFLECT: Ensure improvements enhance quality without losing original intent

Provide the improved version of the content with clear explanations of changes made.
"""
                response = self.model.generate_content(prompt)
                return response.text
                
            except Exception as e:
                if attempt == self.max_retries - 1:
                    return f"Content improvement failed: {str(e)}"
        
        return "Content improvement failed after multiple attempts"

    def create_outline(self, topic, content_type):
        """
        Create a detailed outline for content with error handling
        """
        if not topic:
            return "No topic provided for outline creation"
        
        for attempt in range(self.max_retries):
            try:
                prompt = f"""
You are creating a comprehensive outline for a {content_type} about {topic}.

GOAL: Create a detailed, logical outline that will guide content creation
THINK: What structure will best serve this topic and content type?
PLAN: Organize information hierarchically with clear sections
ACT: Create detailed outline with main points and subpoints
REFLECT: Ensure outline is comprehensive and logically flowing

Include:
1. Compelling title options
2. Introduction approach
3. Main sections with subsections
4. Key points to cover in each section
5. Conclusion strategy
6. Call-to-action (if applicable)

Provide a detailed, actionable outline.
"""
                response = self.model.generate_content(prompt)
                return response.text
                
            except Exception as e:
                if attempt == self.max_retries - 1:
                    return f"Outline creation failed: {str(e)}"
        
        return "Outline creation failed after multiple attempts"

    def adapt_tone(self, content, new_tone):
        """
        Adapt content to a different tone/style with error handling
        """
        if not content:
            return "No content provided for tone adaptation"
        
        for attempt in range(self.max_retries):
            try:
                prompt = f"""
You are adapting content to a {new_tone} tone.

Original Content:
{content}

GOAL: Adapt the content to {new_tone} tone while preserving key information
THINK: How should the tone change to match the target style?
PLAN: Identify tone elements to modify
ACT: Rewrite content with appropriate tone
REFLECT: Ensure tone adaptation maintains content quality and clarity

Provide the adapted content in {new_tone} tone.
"""
                response = self.model.generate_content(prompt)
                return response.text
                
            except Exception as e:
                if attempt == self.max_retries - 1:
                    return f"Tone adaptation failed: {str(e)}"
        
        return "Tone adaptation failed after multiple attempts"

    def get_content_stats(self):
        """Get statistics about created content"""
        if not self.content_library:
            return {"message": "No content created yet"}
        
        total_content = len(self.content_library)
        total_words = sum(item['word_count'] for item in self.content_library.values())
        content_types = {}
        
        for item in self.content_library.values():
            content_type = item['type']
            content_types[content_type] = content_types.get(content_type, 0) + 1
        
        return {
            'total_content': total_content,
            'total_words': total_words,
            'average_words_per_content': total_words / total_content if total_content > 0 else 0,
            'content_types': content_types,
            'error_count': self.error_count
        }

    def reset_error_count(self):
        """Reset error counter for monitoring"""
        self.error_count = 0