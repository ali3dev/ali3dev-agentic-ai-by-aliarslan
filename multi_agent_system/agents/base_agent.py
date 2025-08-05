"""
Base Agent Class - Foundation for all specialized agents
This provides common functionality that all agents inherit
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

class BaseAgent:
    def __init__(self, name, role, expertise):
        self.name = name
        self.role = role
        self.expertise = expertise
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.conversation_history = []
        self.task_history = []
        
    def think_and_act(self, task, context=None):
        """
        Core agentic pattern for all agents
        GOAL → THINK → PLAN → ACT → REFLECT
        """
        prompt = f"""
                You are {self.name}, a {self.role} with expertise in {self.expertise}.

                GOAL: {task}
                THINK: Analyze the task from your specialized perspective
                PLAN: Create a strategy using your expertise  
                ACT: Execute your plan and provide results
                REFLECT: Evaluate if you achieved the goal effectively

                Context: {context if context else "No additional context"}

                Previous tasks: {self.task_history[-3:] if self.task_history else "None"}

                Respond in the agentic format with clear sections.
                        """
        
        try:
            response = self.model.generate_content(prompt)
            
            # Log the interaction
            interaction = {
                'timestamp': datetime.now().isoformat(),
                'task': task,
                'response': response.text,
                'context': context
            }
            self.conversation_history.append(interaction)
            self.task_history.append(task)
            
            return response.text
        
        except Exception as e:
            return f"Error in {self.name}: {str(e)}"
    
    def collaborate(self, message_from_agent, original_task):
        """
        Handle collaboration with other agents
        """
        prompt = f"""
                You are {self.name} ({self.role}). Another agent has sent you information to help with a collaborative task.

                Original Task: {original_task}
                Message from other agent: {message_from_agent}

                Your expertise: {self.expertise}

                GOAL: Use the information provided to contribute your specialized knowledge
                THINK: How can your expertise add value to what's already been done?
                PLAN: What specific contribution should you make?
                ACT: Provide your specialized input or improvement
                REFLECT: How does your contribution improve the overall result?

                Be collaborative and build upon the previous work.
                        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Collaboration error in {self.name}: {str(e)}"
    
    def get_status(self):
        """Get current status of the agent"""
        return {
            'name': self.name,
            'role': self.role,
            'expertise': self.expertise,
            'tasks_completed': len(self.task_history),
            'last_active': self.conversation_history[-1]['timestamp'] if self.conversation_history else None
        }