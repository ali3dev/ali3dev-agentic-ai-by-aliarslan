"""
Conversation History - Long-term conversation memory
Maintains context across sessions and interactions
"""

from datetime import datetime, timedelta
import json

class ConversationHistory:
    def __init__(self):
        self.sessions = {}
        self.user_profiles = {}
        self.conversation_summaries = {}
        self.context_retention_days = 30
        
    def start_session(self, user_id, session_type="general"):
        """Start a new conversation session"""
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{user_id}"
        
        self.sessions[session_id] = {
            'user_id': user_id,
            'session_type': session_type,
            'started_at': datetime.now().isoformat(),
            'last_activity': datetime.now().isoformat(),
            'messages': [],
            'context': {},
            'goals': [],
            'outcomes': [],
            'satisfaction_score': None
        }
        
        return session_id
    
    def add_message(self, session_id, speaker, message, message_type="text", metadata=None):
        """Add a message to the conversation history"""
        if session_id not in self.sessions:
            return False
        
        message_entry = {
            'speaker': speaker,
            'message': message,
            'type': message_type,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        
        self.sessions[session_id]['messages'].append(message_entry)
        self.sessions[session_id]['last_activity'] = datetime.now().isoformat()
        
        # Update user profile
        if speaker == 'user':
            self._update_user_profile(self.sessions[session_id]['user_id'], message, metadata)
        
        return True
    
    def update_session_context(self, session_id, context_updates):
        """Update session context information"""
        if session_id not in self.sessions:
            return False
        
        self.sessions[session_id]['context'].update(context_updates)
        return True
    
    def add_session_goal(self, session_id, goal, priority="normal"):
        """Add a goal to the current session"""
        if session_id not in self.sessions:
            return False
        
        goal_entry = {
            'goal': goal,
            'priority': priority,
            'added_at': datetime.now().isoformat(),
            'status': 'active'
        }
        
        self.sessions[session_id]['goals'].append(goal_entry)
        return True
    
    def complete_session_goal(self, session_id, goal_index, outcome):
        """Mark a session goal as completed"""
        if (session_id not in self.sessions or 
            goal_index >= len(self.sessions[session_id]['goals'])):
            return False
        
        goal = self.sessions[session_id]['goals'][goal_index]
        goal['status'] = 'completed'
        goal['completed_at'] = datetime.now().isoformat()
        goal['outcome'] = outcome
        
        return True
    
    def get_session_context(self, session_id):
        """Get current session context"""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        
        # Get recent messages for context
        recent_messages = session['messages'][-10:]  # Last 10 messages
        
        return {
            'session_info': {
                'user_id': session['user_id'],
                'session_type': session['session_type'],
                'duration': self._calculate_session_duration(session_id)
            },
            'recent_messages': recent_messages,
            'context': session['context'],
            'active_goals': [g for g in session['goals'] if g['status'] == 'active'],
            'user_profile': self.user_profiles.get(session['user_id'], {})
        }
    
    def get_user_history(self, user_id, days_back=7):
        """Get conversation history for a user"""
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        user_sessions = []
        for session_id, session in self.sessions.items():
            if (session['user_id'] == user_id and 
                datetime.fromisoformat(session['started_at']) > cutoff_date):
                user_sessions.append({
                    'session_id': session_id,
                    'started_at': session['started_at'],
                    'message_count': len(session['messages']),
                    'goals_completed': len([g for g in session['goals'] if g['status'] == 'completed']),
                    'satisfaction_score': session['satisfaction_score'],
                    'session_type': session['session_type'],
                    'duration': self._calculate_session_duration(session_id),
                    'last_activity': session['last_activity']
                })
        
        return sorted(user_sessions, key=lambda x: x['started_at'], reverse=True)
    
    def create_conversation_summary(self, session_id):
        """Create a summary of the conversation"""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        
        # Create summary based on messages and outcomes
        summary = {
            'session_id': session_id,
            'user_id': session['user_id'],
            'session_type': session['session_type'],
            'duration': self._calculate_session_duration(session_id),
            'total_messages': len(session['messages']),
            'main_topics': self._extract_main_topics(session['messages']),
            'goals_achieved': [g for g in session['goals'] if g['status'] == 'completed'],
            'key_decisions': self._extract_key_decisions(session['messages']),
            'satisfaction_score': session['satisfaction_score'],
            'outcome_summary': self._generate_outcome_summary(session),
            'created_at': datetime.now().isoformat()
        }
        
        self.conversation_summaries[session_id] = summary
        return summary
    
    def _update_user_profile(self, user_id, message, metadata):
        """Update user profile based on interactions"""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                'preferences': {},
                'interaction_patterns': {},
                'satisfaction_history': [],
                'common_requests': {},
                'expertise_areas': set(),
                'communication_style': 'unknown',
                'total_sessions': 0,
                'total_messages': 0,
                'first_interaction': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat()
            }
        
        profile = self.user_profiles[user_id]
        
        # Update basic counts
        profile['total_messages'] += 1
        
        # Update interaction patterns
        hour = datetime.now().hour
        if 'active_hours' not in profile['interaction_patterns']:
            profile['interaction_patterns']['active_hours'] = {}
        
        hour_key = f"{hour:02d}:00"
        profile['interaction_patterns']['active_hours'][hour_key] = \
            profile['interaction_patterns']['active_hours'].get(hour_key, 0) + 1
        
        # Analyze message for preferences (simplified)
        message_lower = message.lower()
        
        # Extract potential preferences
        if 'prefer' in message_lower or 'like' in message_lower:
            # Extract preference (simplified parsing)
            words = message_lower.split()
            for i, word in enumerate(words):
                if word in ['prefer', 'like'] and i + 1 < len(words):
                    preference = words[i + 1]
                    profile['preferences'][preference] = \
                        profile['preferences'].get(preference, 0) + 1
        
        # Track common request types
        request_keywords = {
            'research': ['research', 'find', 'analyze', 'study'],
            'writing': ['write', 'create', 'draft', 'compose'],
            'analysis': ['analyze', 'compare', 'evaluate', 'assess'],
            'planning': ['plan', 'strategy', 'organize', 'schedule']
        }
        
        for request_type, keywords in request_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                profile['common_requests'][request_type] = \
                    profile['common_requests'].get(request_type, 0) + 1
        
        # Determine communication style
        if len(message.split()) > 20:
            profile['communication_style'] = 'detailed'
        elif '?' in message:
            profile['communication_style'] = 'inquisitive'
        elif '!' in message:
            profile['communication_style'] = 'enthusiastic'
        else:
            profile['communication_style'] = 'concise'
        
        profile['last_updated'] = datetime.now().isoformat()
    
    def _calculate_session_duration(self, session_id):
        """Calculate session duration"""
        if session_id not in self.sessions:
            return "0 minutes"
        
        session = self.sessions[session_id]
        start_time = datetime.fromisoformat(session['started_at'])
        end_time = datetime.fromisoformat(session['last_activity'])
        
        duration = end_time - start_time
        minutes = int(duration.total_seconds() / 60)
        
        if minutes < 1:
            return "less than 1 minute"
        elif minutes < 60:
            return f"{minutes} minutes"
        else:
            hours = minutes // 60
            remaining_minutes = minutes % 60
            if remaining_minutes == 0:
                return f"{hours} hour{'s' if hours > 1 else ''}"
            else:
                return f"{hours}h {remaining_minutes}m"
    
    def _extract_main_topics(self, messages):
        """Extract main topics from conversation"""
        # Simplified topic extraction
        all_text = " ".join([msg['message'] for msg in messages if msg['speaker'] == 'user'])
        words = all_text.lower().split()
        
        # Count word frequency (excluding common words)
        common_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'i', 'you', 'we', 
            'they', 'he', 'she', 'it', 'this', 'that', 'can', 'will', 'would', 
            'could', 'should', 'have', 'has', 'had', 'do', 'does', 'did', 'get', 
            'got', 'make', 'made', 'go', 'went', 'come', 'came', 'see', 'saw'
        }
        
        word_count = {}
        for word in words:
            if len(word) > 3 and word not in common_words and word.isalpha():
                word_count[word] = word_count.get(word, 0) + 1
        
        # Return top topics
        sorted_topics = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        return [topic[0] for topic in sorted_topics[:8]]
    
    def _extract_key_decisions(self, messages):
        """Extract key decisions made during conversation"""
        decisions = []
        decision_keywords = [
            'decide', 'decided', 'choose', 'chose', 'select', 'selected', 
            'pick', 'picked', 'go with', 'prefer', 'preferred', 'option'
        ]
        
        for msg in messages:
            if msg['speaker'] == 'user':
                message_lower = msg['message'].lower()
                for keyword in decision_keywords:
                    if keyword in message_lower:
                        decisions.append({
                            'decision': msg['message'][:100] + "..." if len(msg['message']) > 100 else msg['message'],
                            'timestamp': msg['timestamp'],
                            'keyword_found': keyword
                        })
                        break
        
        return decisions[-10:]  # Return last 10 decisions
    
    def _generate_outcome_summary(self, session):
        """Generate a summary of session outcomes"""
        outcomes = []
        
        # Count completed goals
        completed_goals = [g for g in session['goals'] if g['status'] == 'completed']
        if completed_goals:
            outcomes.append(f"Completed {len(completed_goals)} goals")
        
        # Analyze message patterns
        total_messages = len(session['messages'])
        user_messages = len([m for m in session['messages'] if m['speaker'] == 'user'])
        agent_messages = total_messages - user_messages
        
        outcomes.append(f"Exchange of {user_messages} user messages and {agent_messages} agent responses")
        
        # Session duration outcome
        duration = self._calculate_session_duration(session['session_id'] if 'session_id' in session else 'unknown')
        outcomes.append(f"Session lasted {duration}")
        
        return ". ".join(outcomes)
    
    def cleanup_old_sessions(self):
        """Clean up old sessions beyond retention period"""
        cutoff_date = datetime.now() - timedelta(days=self.context_retention_days)
        
        sessions_to_remove = []
        summaries_created = 0
        
        for session_id, session in self.sessions.items():
            if datetime.fromisoformat(session['started_at']) < cutoff_date:
                # Create summary before removing
                if session_id not in self.conversation_summaries:
                    self.create_conversation_summary(session_id)
                    summaries_created += 1
                sessions_to_remove.append(session_id)
        
        # Remove old sessions
        for session_id in sessions_to_remove:
            del self.sessions[session_id]
        
        return {
            'sessions_removed': len(sessions_to_remove),
            'summaries_created': summaries_created,
            'retention_days': self.context_retention_days
        }
    
    def get_conversation_insights(self, user_id=None):
        """Get insights about conversations"""
        if user_id:
            # User-specific insights
            user_sessions = [s for s in self.sessions.values() if s['user_id'] == user_id]
            if not user_sessions:
                return {
                    'user_id': user_id,
                    'error': 'No sessions found for this user'
                }
            
            total_messages = sum(len(s['messages']) for s in user_sessions)
            satisfaction_scores = [s['satisfaction_score'] for s in user_sessions if s['satisfaction_score']]
            avg_satisfaction = sum(satisfaction_scores) / len(satisfaction_scores) if satisfaction_scores else None
            
            return {
                'user_id': user_id,
                'total_sessions': len(user_sessions),
                'total_messages': total_messages,
                'average_messages_per_session': total_messages / len(user_sessions) if user_sessions else 0,
                'average_satisfaction': round(avg_satisfaction, 2) if avg_satisfaction else None,
                'most_common_topics': self._get_user_common_topics(user_id),
                'interaction_patterns': self.user_profiles.get(user_id, {}).get('interaction_patterns', {}),
                'communication_style': self.user_profiles.get(user_id, {}).get('communication_style', 'unknown'),
                'common_requests': self.user_profiles.get(user_id, {}).get('common_requests', {})
            }
        else:
            # Overall system insights
            total_sessions = len(self.sessions)
            total_users = len(set(s['user_id'] for s in self.sessions.values()))
            total_messages = sum(len(s['messages']) for s in self.sessions.values())
            
            return {
                'total_sessions': total_sessions,
                'total_users': total_users,
                'total_messages': total_messages,
                'average_messages_per_session': total_messages / total_sessions if total_sessions > 0 else 0,
                'average_session_length': self._calculate_average_session_length(),
                'most_active_hours': self._get_most_active_hours(),
                'satisfaction_trends': self._get_satisfaction_trends(),
                'top_topics_overall': self._get_overall_common_topics()
            }
    
    def _get_user_common_topics(self, user_id):
        """Get most common topics for a user"""
        user_sessions = [s for s in self.sessions.values() if s['user_id'] == user_id]
        all_topics = []
        
        for session in user_sessions:
            topics = self._extract_main_topics(session['messages'])
            all_topics.extend(topics)
        
        topic_count = {}
        for topic in all_topics:
            topic_count[topic] = topic_count.get(topic, 0) + 1
        
        sorted_topics = sorted(topic_count.items(), key=lambda x: x[1], reverse=True)
        return [{'topic': topic, 'frequency': count} for topic, count in sorted_topics[:5]]
    
    def _get_overall_common_topics(self):
        """Get most common topics across all sessions"""
        all_topics = []
        
        for session in self.sessions.values():
            topics = self._extract_main_topics(session['messages'])
            all_topics.extend(topics)
        
        topic_count = {}
        for topic in all_topics:
            topic_count[topic] = topic_count.get(topic, 0) + 1
        
        sorted_topics = sorted(topic_count.items(), key=lambda x: x[1], reverse=True)
        return [{'topic': topic, 'frequency': count} for topic, count in sorted_topics[:10]]
    
    def _calculate_average_session_length(self):
        """Calculate average session length across all sessions"""
        if not self.sessions:
            return "0 minutes"
        
        total_minutes = 0
        valid_sessions = 0
        
        for session_id in self.sessions.keys():
            duration_str = self._calculate_session_duration(session_id)
            
            # Parse duration string to get minutes
            try:
                if 'hour' in duration_str:
                    if 'h' in duration_str and 'm' in duration_str:
                        parts = duration_str.replace('h', '').replace('m', '').split()
                        minutes = int(parts[0]) * 60 + int(parts[1])
                    else:
                        hours = int(duration_str.split()[0])
                        minutes = hours * 60
                elif 'minute' in duration_str:
                    if 'less than' in duration_str:
                        minutes = 0
                    else:
                        minutes = int(duration_str.split()[0])
                else:
                    minutes = 0
                
                total_minutes += minutes
                valid_sessions += 1
            except:
                continue
        
        if valid_sessions == 0:
            return "0 minutes"
        
        avg_minutes = total_minutes // valid_sessions
        if avg_minutes < 60:
            return f"{avg_minutes} minutes"
        else:
            hours = avg_minutes // 60
            remaining_minutes = avg_minutes % 60
            if remaining_minutes == 0:
                return f"{hours} hour{'s' if hours > 1 else ''}"
            else:
                return f"{hours}h {remaining_minutes}m"
    
    def _get_most_active_hours(self):
        """Get most active conversation hours"""
        hour_counts = {}
        
        for session in self.sessions.values():
            try:
                start_hour = datetime.fromisoformat(session['started_at']).hour
                hour_key = f"{start_hour:02d}:00"
                hour_counts[hour_key] = hour_counts.get(hour_key, 0) + 1
            except:
                continue
        
        sorted_hours = sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)
        return [{'hour': hour, 'sessions': count} for hour, count in sorted_hours[:5]]
    
    def _get_satisfaction_trends(self):
        """Get satisfaction score trends"""
        scores = [s['satisfaction_score'] for s in self.sessions.values() 
                 if s['satisfaction_score'] is not None]
        
        if not scores:
            return {
                'message': 'No satisfaction scores available',
                'total_ratings': 0
            }
        
        return {
            'average_score': round(sum(scores) / len(scores), 2),
            'highest_score': max(scores),
            'lowest_score': min(scores),
            'total_ratings': len(scores),
            'score_distribution': self._get_score_distribution(scores)
        }
    
    def _get_score_distribution(self, scores):
        """Get distribution of satisfaction scores"""
        distribution = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}
        
        for score in scores:
            score_key = str(int(score))
            if score_key in distribution:
                distribution[score_key] += 1
        
        return distribution
    
    def set_session_satisfaction(self, session_id, satisfaction_score):
        """Set satisfaction score for a session"""
        if session_id not in self.sessions:
            return False
        
        if not (1 <= satisfaction_score <= 5):
            return False
        
        self.sessions[session_id]['satisfaction_score'] = satisfaction_score
        
        # Update user profile satisfaction history
        user_id = self.sessions[session_id]['user_id']
        if user_id in self.user_profiles:
            self.user_profiles[user_id]['satisfaction_history'].append({
                'score': satisfaction_score,
                'session_id': session_id,
                'timestamp': datetime.now().isoformat()
            })
        
        return True
    
    def get_user_satisfaction_trend(self, user_id):
        """Get satisfaction trend for a specific user"""
        if user_id not in self.user_profiles:
            return None
        
        history = self.user_profiles[user_id].get('satisfaction_history', [])
        if not history:
            return None
        
        scores = [h['score'] for h in history]
        
        return {
            'user_id': user_id,
            'total_ratings': len(scores),
            'average_score': round(sum(scores) / len(scores), 2),
            'latest_score': scores[-1],
            'trend': 'improving' if len(scores) > 1 and scores[-1] > scores[-2] else 
                    'declining' if len(scores) > 1 and scores[-1] < scores[-2] else 'stable',
            'score_history': history[-5:]  # Last 5 scores
        }
    
    def export_user_data(self, user_id):
        """Export all data for a specific user"""
        user_data = {
            'user_id': user_id,
            'profile': self.user_profiles.get(user_id, {}),
            'sessions': [],
            'summaries': [],
            'insights': self.get_conversation_insights(user_id),
            'satisfaction_trend': self.get_user_satisfaction_trend(user_id),
            'export_timestamp': datetime.now().isoformat()
        }
        
        # Add session data
        for session_id, session in self.sessions.items():
            if session['user_id'] == user_id:
                user_data['sessions'].append(session)
        
        # Add conversation summaries
        for summary_id, summary in self.conversation_summaries.items():
            if summary['user_id'] == user_id:
                user_data['summaries'].append(summary)
        
        return user_data
    
    def get_system_health(self):
        """Get overall system health metrics"""
        return {
            'total_sessions': len(self.sessions),
            'total_users': len(self.user_profiles),
            'total_summaries': len(self.conversation_summaries),
            'memory_usage': {
                'sessions_mb': len(str(self.sessions)) / 1024 / 1024,
                'profiles_mb': len(str(self.user_profiles)) / 1024 / 1024,
                'summaries_mb': len(str(self.conversation_summaries)) / 1024 / 1024
            },
            'oldest_session': min([s['started_at'] for s in self.sessions.values()]) if self.sessions else None,
            'newest_session': max([s['started_at'] for s in self.sessions.values()]) if self.sessions else None,
            'retention_days': self.context_retention_days,
            'health_status': 'healthy' if len(self.sessions) < 10000 else 'needs_cleanup'
        }