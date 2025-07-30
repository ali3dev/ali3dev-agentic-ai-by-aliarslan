from agent_advanced import AdvancedGeminiAgent

def test_agent():
    agent = AdvancedGeminiAgent()
    
    test_cases = [
        "Calculate 15 * 23 + 100",
        "What is 25% of 80?", 
        "Analyze this text: 'This product is absolutely amazing! I love it so much.'",
        "Find the square root of 256",
        "How many words are in this sentence: 'Hello world, this is a test'",
        "What's 2^10?"
    ]
    
    print("🧪 Testing Advanced Gemini Agent\n")
    
    for i, test in enumerate(test_cases, 1):
        print(f"Test {i}: {test}")
        print("-" * 50)
        response = agent.process_with_agent_pattern(test)
        print(f"Response: {response}\n")
        print("=" * 70)

if __name__ == "__main__":
    test_agent()