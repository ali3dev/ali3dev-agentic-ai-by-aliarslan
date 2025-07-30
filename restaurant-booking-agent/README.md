# Agentic AI Learning Journey - Day 1

## Projects Overview

### 1. Basic Agentic AI Journey
A project focused on understanding the fundamentals of agentic AI using Google's Gemini model. This project demonstrates:

#### Features
- Advanced Gemini Agent with integrated tools
- Multiple operation modes (simple chat and agent mode)
- Tool integration pattern
- Mathematical calculations
- Text analysis capabilities

#### Components
- `agent_advanced.py`: Main agent implementation with tool integration
- `agent_basic.py`: Basic implementation for learning purposes
- Tools:
  - Calculator Tool
  - Text Analyzer Tool

#### Key Learnings
- Implementation of agent patterns
- Tool integration in AI agents
- Conversation management
- Error handling in AI responses
- Pattern detection for tool selection
- Prompt engineering

### 2. Restaurant Booking Agent
A practical application of agentic AI in a real-world scenario.

#### Features
- Restaurant search functionality
- Booking management system
- Email notification system
- User preference handling
- Availability checking

#### Components
- Agent:
  - `restaurant_agent.py`: Main booking agent implementation
- Tools:
  - Availability Checker
  - Booking Manager
  - Email Sender
  - Restaurant Search
  - User Preference Handler

#### Key Learnings
- Real-world application of agentic AI
- Complex system architecture
- Multiple tool orchestration
- User interaction flow management
- Integration of various services

## Technical Stack
- Python
- Google Gemini AI Model
- Environment Management (dotenv)
- Regular Expressions
- Object-Oriented Programming

## Project Structure
```
.
├── agentic-ai-journey/
│   ├── agent_advanced.py
│   ├── agent_basic.py
│   └── tools/
│       ├── calculator.py
│       └── text_analyzer.py
│
└── restaurant-booking-agent/
    ├── agent/
    │   └── restaurant_agent.py
    └── tools/
        ├── availability_checker.py
        ├── booking_manager.py
        ├── email_sender.py
        ├── restaurant_search.py
        └── user_preference.py
```

## Key Takeaways
1. Understanding of agent-based architecture
2. Tool integration patterns
3. State management in AI agents
4. Error handling and edge cases
5. Practical implementation of AI in business scenarios

## Challenges Faced
1. Tool selection logic implementation
2. Pattern matching for different types of user inputs
3. Maintaining conversation context
4. Integrating multiple tools efficiently
5. Balancing between simple and complex agent modes

## Next Steps
- Enhance error handling
- Add more sophisticated tools
- Implement better conversation memory
- Add unit tests
- Improve documentation

## Setup Instructions
1. Clone the repository
2. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```
3. Set up environment variables:
   - Create a `.env` file
   - Add your Google API key: `GOOGLE_API_KEY=your_key_here`
4. Run the projects:
   ```bash
   # For agentic journey
   python agent_advanced.py
   
   # For restaurant booking
   python main.py
   ```

## Testing
- Basic test cases are included in `test_agent.py`
- Run tests using:
  ```bash
  python -m pytest test_agent.py
  ```
