"""
Shared Memory - Knowledge base accessible by all agents
Stores facts, insights, and learned information
"""

from datetime import datetime
import json

class SharedMemory:
    def get_fact(self, category, key, requesting_agent):
        """Retrieve a single fact from the knowledge base (for compatibility with tests)"""
        if category in self.knowledge_base['facts'] and key in self.knowledge_base['facts'][category]:
            fact = self.knowledge_base['facts'][category][key]
            fact['access_count'] += 1
            self._log_access('get_fact', requesting_agent, f'{category}.{key}')
            return fact
        return None
    def __init__(self):
        self.knowledge_base = {
            'facts': {},
            'insights': {},
            'templates': {},
            'best_practices': {},
            'user_preferences': {},
            'project_history': {}
        }
        self.access_log = []

    def store_fact(self, category, key, value, source_agent, confidence=1.0):
        """Store a verified fact in the knowledge base"""
        if category not in self.knowledge_base['facts']:
            self.knowledge_base['facts'][category] = {}
        
        fact_entry = {
            'value': value,
            'source_agent': source_agent,
            'confidence': confidence,
            'stored_at': datetime.now().isoformat(),
            'verified': False,
            'access_count': 0
        }
        self.knowledge_base['facts'][category][key] = fact_entry
        self._log_access('store_fact', source_agent, f"{category}.{key}")

    
    def get_facts(self, category, key, requesting_agent):
        """Retrieve a fact from the knowledge base"""
        if (category in self.knowledge_base['facts'] and 
            key in self.knowledge_base['facts'][category]):

            fact = self.knowledge_base['facts'][category][key]
            fact['access_count'] += 1
            self._log_access('get_fact', requesting_agent, f'{category}.{key}')
            return fact
        
        return None
    
    def store_insight(self, topic, insight, source_agent, relevance_score=1.0):
        """Store strategic insights"""
        if topic not in self.knowledge_base['insights']:
            self.knowledge_base['insights'][topic] = []
        
        insight_entry = {
            'content': insight,
            'source_agent': source_agent,
            'relevance_score': relevance_score,
            'stored_at': datetime.now().isoformat(),
            'tags': self._extract_tags(insight),
            'access_count': 0
        }

        self.knowledge_base['insights'][topic].append(insight_entry)
        self._log_access('store_insight', source_agent, topic)

    def get_insights(self,topic, requesting_agent, limit=5):
        if topic not in self.knowledge_base['insights']:
            return []
        
        insights = self.knowledge_base['insights'][topic]

        #Sort by relevance score and recency
        sorted_insights = sorted(insights,
                                 key=lambda x: (x['relevance_score'], x['stored_at']),
                                 reverse=True)
        
        #Update access counts
        for insight in sorted_insights[:limit]:
            insight['access_count'] += 1

        self._log_access('get_insights', requesting_agent, topic)
        return sorted_insights[:limit]
    
    def store_template(self, template_type, name, template_content, source_agent):
        """Store reusable templates"""

        if template_type not in self.knowledge_base['templates']:
            self.knowledge_base['templates'][template_type] = {}

        template_entry = {
            'content': template_content,
            'source_agent': source_agent,
            'created_at': datetime.now().isoformat(),
            'usage_count': 0,
            'effectiveness_rating': 0.0
        }
                
        self.knowledge_base['templates'][template_type][name] = template_entry
        self._log_access('store_template', source_agent, f"{template_type}")

    def get_template(self, template_type, name, requesting_agent):
        """Retrieve a template"""
        if (template_type in self.knowledge_base['templates'] and 
            name in self.knowledge_base['templates'][template_type]):
        
            template = self.knowledge_base['templates'][template_type][name]
            template['usage_count'] += 1
            self._log_access('get_template', requesting_agent, f"{template_type}. {name}")

            return template
         
        return None


    def store_best_practice(self, domain, practice, source_agent, effectiveness_score=1.0):
        """Store best practices learned"""
        if domain not in self.knowledge_base['best_practices']:
            self.knowledge_base['best_practices'][domain] = []
        
        practice_entry = {
            'practice': practice,
            'source_agent': source_agent,
            'effectiveness_score': effectiveness_score,
            'stored_at': datetime.now().isoformat(),
            'validation_count': 1
        }

        self.knowledge_base['base_practices'][domain].append(practice_entry)
        self._log_access('store_best_practice', source_agent, domain)

    def get_best_practices(self, domain, requesting_agent):
        """Retrieve best practices for a domain"""
        if domain not in self.knowledge_base['best_practices']:
            return []
        
        practices = self.knowledge_base['best_practices'][domain]

        # Sort by effectiveness score
        sorted_practices = sorted(practices, 
                                key=lambda x: x['effectiveness_score'], 
                                reverse=True)


    def store_user_preference(self, user_id, preference_type, value, source_agent):
        """Store user preferences for personalization"""
        if user_id not in self.knowledge_base['user_preferences']:
            self.knowledge_base['user_preferences'][user_id] = {}
        
        self.knowledge_base['user_preferences'][user_id][preference_type] = {
            'value': value,
            'source_agent': source_agent,
            'updated_at': datetime.now().isoformat()
        }
        
        self._log_access('store_user_preference', source_agent, f"{user_id}.{preference_type}")
        
    def get_user_preferences(self, user_id, requesting_agent):
        """Retrieve user preferences"""
        preferences = self.knowledge_base['user_preferences'].get(user_id, {})
        self._log_access('get_user_preferences', requesting_agent, user_id)
        return preferences
    
    def search_knowledge(self, query, requesting_agent, limit=10):
        """Search across all knowledge categories"""
        results = []
        
        # Search facts
        for category, facts in self.knowledge_base['facts'].items():
            for key, fact in facts.items():
                if query.lower() in f"{category} {key} {fact['value']}".lower():
                    results.append({
                        'type': 'fact',
                        'category': category,
                        'key': key,
                        'content': fact['value'],
                        'relevance': self._calculate_relevance(query, f"{category} {key} {fact['value']}")
                    })
        
        # Search insights
        for topic, insights in self.knowledge_base['insights'].items():
            for insight in insights:
                if query.lower() in f"{topic} {insight['content']}".lower():
                    results.append({
                        'type': 'insight',
                        'topic': topic,
                        'content': insight['content'],
                        'relevance': self._calculate_relevance(query, f"{topic} {insight['content']}")
                    })
        
        # Sort by relevance
        results.sort(key=lambda x: x['relevance'], reverse=True)
        
        self._log_access('search_knowledge', requesting_agent, query)
        return results[:limit]
    
    def _extract_tags(self, text):
        """Extract relevant tags from text"""
        # Simple tag extraction (in real implementation, use NLP)
        words = text.lower().split()
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were'}
        tags = [word for word in words if len(word) > 3 and word not in common_words]
        return tags[:10]  # Return top 10 relevant words as tags
    
    def _calculate_relevance(self, query, text):
        """Calculate relevance score between query and text"""
        query_words = set(query.lower().split())
        text_words = set(text.lower().split())
        overlap = len(query_words.intersection(text_words))
        return overlap / len(query_words) if query_words else 0
    
    def _log_access(self, action, agent, resource):
        """Log memory access for analytics"""
        log_entry = {
            'action': action,
            'agent': agent,
            'resource': resource,
            'timestamp': datetime.now().isoformat()
        }
        self.access_log.append(log_entry)
        
        # Keep only recent logs (last 1000)
        if len(self.access_log) > 1000:
            self.access_log = self.access_log[-1000:]
    
    def get_memory_stats(self):
        """Get memory system statistics"""
        return {
            'total_facts': sum(len(facts) for facts in self.knowledge_base['facts'].values()),
            'total_insights': sum(len(insights) for insights in self.knowledge_base['insights'].values()),
            'total_templates': sum(len(templates) for templates in self.knowledge_base['templates'].values()),
            'total_best_practices': sum(len(practices) for practices in self.knowledge_base['best_practices'].values()),
            'total_users': len(self.knowledge_base['user_preferences']),
            'total_accesses': len(self.access_log)
        }