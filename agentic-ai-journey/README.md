# Agentic AI Journey - Basic Implementation

## Overview
This project demonstrates the implementation of an intelligent agent using Google's Gemini model with integrated tools for mathematical calculations and text analysis.

## Features

### 1. Advanced Gemini Agent
- Dual operation modes:
  - Simple Chat Mode: Direct interaction with Gemini model
  - Agent Mode: Advanced reasoning with tool integration
- Tool-based problem solving
- Structured response pattern (GOAL, THINK, PLAN, ACT, REFLECT)

### 2. Integrated Tools
- **Calculator Tool**
  - Basic arithmetic operations
  - Percentage calculations
  - Square root and advanced math functions
  
- **Text Analyzer Tool**
  - Word count
  - Sentiment analysis
  - Text pattern recognition

## Project Structure
```
agentic-ai-journey/
├── agent_advanced.py      # Main agent implementation
├── agent_basic.py        # Basic version for learning
├── requirements.txt      # Project dependencies
├── test_agent.py        # Test cases
└── tools/
    ├── __init__.py
    ├── calculator.py     # Mathematical operations
    └── text_analyzer.py  # Text analysis functions
```

## Implementation Details

### Agent Components
1. **Tool Detection System**
   - Pattern matching for mathematical operations
   - Text analysis requirements detection
   - Automatic tool selection

2. **Input Processing**
   - Mathematical expression extraction
   - Text content parsing
   - Context-aware processing

3. **Response Generation**
   - Structured thinking pattern
   - Tool result integration
   - Error handling

## Usage Examples

```python
# Mathematical Operations
"Calculate 25% of 200 plus 30"
"What is the square root of 144?"

# Text Analysis
"Analyze this text: I love this amazing product!"
"How many words are in: This is a test sentence"
```

## Command Options
- `quit`: Exit the application
- `simple`: Switch to simple chat mode
- `agent`: Switch to agentic mode (default)

## Setup Instructions


1. Install dependencies (recommended: uv for faster installs):
```bash
uv pip install -r requirements.txt
```
Or, if you prefer pip:
```bash
pip install -r requirements.txt
```

2. Configure environment:
- Create a `.env` file
- Add your Google API key:
```
GOOGLE_API_KEY=your_key_here
```

3. Run the agent:
```bash
python agent_advanced.py
```

## Testing
Run the test suite:
```bash
python -m pytest test_agent.py
```

## Key Features Demonstrated
- Agent-based architecture
- Tool integration patterns
- Pattern recognition
- Context management
- Error handling
- User interaction flows

## Learning Outcomes
1. Understanding of agent-based systems
2. Tool integration in AI applications
3. Pattern matching and detection
4. Structured thinking in AI agents
5. Error handling in AI applications
