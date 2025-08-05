"""
Message Hub - Handles communication between agents
Central communication system for multi-agent coordination
"""

from datetime import datetime
import json

class MessageHub:
    def __init__(self):
        self.message_queue = []
        self.agent_registry = {}
        self.conversation_threads = {}
        
    def register_agent(self, agent_name, agent_instance):
        """Register an agent with the communication system"""
        self.agent_registry[agent_name] = agent_instance
        
    def send_message(self, from_agent, to_agent, message_type, content, priority="normal"):
        """Send a message between agents"""
        message = {
            'id': f"msg_{len(self.message_queue) + 1}",
            'from': from_agent,
            'to': to_agent,
            'type': message_type,
            'content': content,
            'priority': priority,
            'timestamp': datetime.now().isoformat(),
            'status': 'pending'
        }
        
        self.message_queue.append(message)
        return message['id']
    
    def get_messages_for_agent(self, agent_name):
        """Retrieve pending messages for an agent"""
        messages = [msg for msg in self.message_queue 
                   if msg['to'] == agent_name and msg['status'] == 'pending']
        
        # Mark messages as delivered
        for msg in messages:
            msg['status'] = 'delivered'
            
        return messages
    
    def create_conversation_thread(self, thread_name, participants):
        """Create a conversation thread for multiple agents"""
        thread_id = f"thread_{len(self.conversation_threads) + 1}"
        self.conversation_threads[thread_id] = {
            'name': thread_name,
            'participants': participants,
            'messages': [],
            'created_at': datetime.now().isoformat(),
            'status': 'active'
        }
        return thread_id
    
    def post_to_thread(self, thread_id, from_agent, content):
        """Post a message to a conversation thread"""
        if thread_id not in self.conversation_threads:
            return None
        
        message = {
            'from': from_agent,
            'content': content,
            'timestamp': datetime.now().isoformat()
        }
        
        self.conversation_threads[thread_id]['messages'].append(message)
        return len(self.conversation_threads[thread_id]['messages'])
    
    def get_thread_history(self, thread_id):
        """Get full conversation thread history"""
        if thread_id not in self.conversation_threads:
            return None
        return self.conversation_threads[thread_id]
    
    def broadcast_message(self, from_agent, content, agent_list=None):
        """Broadcast a message to multiple agents"""
        targets = agent_list or list(self.agent_registry.keys())
        targets = [agent for agent in targets if agent != from_agent]
        
        message_ids = []
        for target in targets:
            msg_id = self.send_message(from_agent, target, 'broadcast', content)
            message_ids.append(msg_id)
        
        return message_ids
    
    def get_communication_stats(self):
        """Get communication system statistics"""
        return {
            'total_messages': len(self.message_queue),
            'active_threads': len([t for t in self.conversation_threads.values() if t['status'] == 'active']),
            'registered_agents': len(self.agent_registry),
            'pending_messages': len([m for m in self.message_queue if m['status'] == 'pending'])
        }