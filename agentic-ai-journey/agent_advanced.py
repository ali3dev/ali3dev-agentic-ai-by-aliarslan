import os
import google.generativeai as genai
from dotenv import load_dotenv
from tools.calculator import CalculatorTool
from tools.text_analyzer import TextAnalyzerTool
import json
import re

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

class AdvancedGeminiAgent:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.tools = {
            'calculator': CalculatorTool(),
            'text_analyzer': TextAnalyzerTool()
        }
        self.conversation_history = []
    
    def detect_tool_needed(self, user_input):
        """
        Analyze if user input requires any tools
        """
        # Math detection
        math_patterns = [
            r'\d+\s*[\+\-\*\/\^]\s*\d+',  # Basic math operations
            r'calculate|math|solve|compute',  # Math keywords
            r'percentage|%|percent',  # Percentage
            r'square root|sqrt|sin|cos|tan|log'  # Advanced math
        ]
        
        # Text analysis detection
        text_patterns = [
            r'analyze.*text|sentiment|word count',
            r'how many words|character count',
            r'positive|negative.*sentiment'
        ]
        
        user_lower = user_input.lower()
        
        # Check for math
        for pattern in math_patterns:
            if re.search(pattern, user_lower):
                return 'calculator'
        
        # Check for text analysis
        for pattern in text_patterns:
            if re.search(pattern, user_lower):
                return 'text_analyzer'
        
        return None
    
    def extract_tool_input(self, user_input, tool_name):
        """
        Extract the relevant input for the tool
        """
        if tool_name == 'calculator':
            # Extract mathematical expression
            math_match = re.search(r'[\d\+\-\*\/\^\(\)\.\s%]+', user_input)
            if math_match:
                return math_match.group().strip()
            return user_input
        
        elif tool_name == 'text_analyzer':
            # Look for text in quotes or after keywords
            quote_match = re.search(r'["\']([^"\']+)["\']', user_input)
            if quote_match:
                return quote_match.group(1)
            
            # If no quotes, assume the whole input after "analyze"
            analyze_match = re.search(r'analyze\s+(?:this\s+)?(?:text\s+)?["\']?([^"\']+?)["\']?$', user_input, re.IGNORECASE)
            if analyze_match:
                return analyze_match.group(1).strip()
            
            return user_input
        
        return user_input
    
    def process_with_agent_pattern(self, user_input):
        """
        Full agentic pattern with tool integration
        """
        # Step 1: Analyze if tools are needed
        tool_needed = self.detect_tool_needed(user_input)
        
        tool_result = ""
        if tool_needed and tool_needed in self.tools:
            tool_input = self.extract_tool_input(user_input, tool_needed)
            
            if tool_needed == 'calculator':
                tool_result = self.tools[tool_needed].calculate(tool_input)
            elif tool_needed == 'text_analyzer':
                tool_result = self.tools[tool_needed].analyze(tool_input)
        
        # Step 2: Create comprehensive prompt
        prompt = f"""
You are an advanced AI agent with access to tools. Follow this process:

GOAL: Understand and fulfill the user's request
THINK: Analyze what the user needs step by step
PLAN: Decide the best approach to help them
ACT: Execute the plan (use tool results if available)
REFLECT: Ensure the goal is achieved

User Request: {user_input}

Tool Used: {tool_needed if tool_needed else "None"}
Tool Result: {tool_result if tool_result else "No tool needed"}

Provide a helpful response in this format:
GOAL: [What you understand]
THINK: [Your analysis]  
PLAN: [Your approach]
ACT: [Your response/solution]
REFLECT: [Goal achievement check]

Make your response conversational and helpful.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def chat(self, user_input):
        """
        Simple chat mode
        """
        try:
            response = self.model.generate_content(user_input)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"

# Interactive testing
def main():
    agent = AdvancedGeminiAgent()
    
    print("🚀 Advanced Gemini Agent with Tools!")
    print("\nCapabilities:")
    print("✓ Mathematical calculations")  
    print("✓ Text analysis and sentiment")
    print("✓ Agentic reasoning pattern")
    print("✓ Tool integration")
    
    print("\nCommands:")
    print("- 'quit': Exit")
    print("- 'simple': Simple chat mode")
    print("- 'agent': Agentic mode (default)")
    print("\nTry asking:")
    print("- 'Calculate 25% of 200 plus 30'")
    print("- 'Analyze this text: I love this amazing product!'")
    print("- 'What is the square root of 144?'")
    
    mode = "agent"
    
    while True:
        user_input = input(f"\n[{mode.upper()}] You: ")
        
        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'simple':
            mode = "simple"
            print("→ Switched to simple chat mode")
            continue
        elif user_input.lower() == 'agent':
            mode = "agent"  
            print("→ Switched to agentic mode")
            continue
        
        print("\n🤖 Agent is thinking...")
        
        if mode == "agent":
            response = agent.process_with_agent_pattern(user_input)
        else:
            response = agent.chat(user_input)
        
        print(f"Agent: {response}")

if __name__ == "__main__":
    main()