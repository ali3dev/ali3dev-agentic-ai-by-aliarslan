import os 

import google.generativeai as genai 
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class SimpleGeminiAgent:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.conversation_history = []

    def think_and_act(self, user_input):
        """
        Implements the Agentic AI pattern:
        Goal -> Think -> Plan -> Act -> Reflect
        """

        prompt = f""" You are an intelligent agent that follows this thinking process:

        1. GOAL: Understand what the user wants
        2. THINK: Analyze the problem step by step
        3. PLAN: Create a strategy to solve it
        4. ACT: Execute the plan
        5. REFLECT: Check if the goal is achieved
        
        User Input: {user_input}

        Please respond in this format:
        GOAL: [What you understand the user wants]
        THINK: [Your step-by-step analysis]
        PLAN: [Your strategy]
        ACT: [Your execution/answer]
        REFLECT: [Did you achieve the goal?]
        """

        try:
            response = self.model.generate_content(prompt)

            # Store in conversation history
            self.conversation_history.append({
                'user': user_input,
                'agent': response.text
            })

            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    def simple_chat(self, user_input):
        """Simple chat without agentic pattern"""
        try:
            response = self.model.generate_content(user_input)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"

# Test the agent
if __name__ == "__main__":
    agent = SimpleGeminiAgent()
    
    print("🤖 Gemini Agent Ready!")
    print("Type 'quit' to exit, 'simple' for simple chat, 'agent' for agentic mode\n")
    
    mode = "agent"  # default mode
    
    while True:
        user_input = input(f"[{mode.upper()}] You: ")
        
        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'simple':
            mode = "simple"
            print("Switched to simple chat mode")
            continue
        elif user_input.lower() == 'agent':
            mode = "agent"
            print("Switched to agentic mode")
            continue
        
        if mode == "agent":
            response = agent.think_and_act(user_input)
        else:
            response = agent.simple_chat(user_input)
        
        print(f"Agent: {response}\n")