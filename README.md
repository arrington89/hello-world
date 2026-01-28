# Hello World AI Agent 🤖

A simple AI agent built with Python that demonstrates:
- Conversational AI using OpenAI's GPT
- Function/tool calling capabilities
- Weather information retrieval (simulated)

This is a beginner-friendly introduction to building AI agents!

## Features

- 💬 Interactive chat interface
- 🌤️ Weather tool (simulated data for demo purposes)
- 🔧 Function calling demonstration
- 🎯 Easy to understand code structure

## Prerequisites

- Python 3.8 or higher
- An OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Then edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 3. Run the Agent

```bash
python agent.py
```

## Usage Examples

Once running, try these prompts:

```
You: What's the weather in New York?
You: Tell me about AI agents
You: What's the weather like in London?
You: Compare the weather in Tokyo and Paris
```

## How It Works

1. **User Input**: You type a message to the agent
2. **AI Processing**: The agent uses GPT to understand your request
3. **Tool Calling**: If weather info is needed, it calls the `get_weather` function
4. **Response**: The agent provides a natural language response with the information

## Code Structure

- `agent.py` - Main agent code with tool definitions
- `requirements.txt` - Python dependencies
- `.env` - Your API keys (not tracked in git)
- `.env.example` - Template for environment variables

## Next Steps

Want to extend this agent? Try:

- ✅ Add a real weather API (like OpenWeatherMap)
- ✅ Create additional tools (calculator, web search, database queries)
- ✅ Add conversation memory/history
- ✅ Use different AI models (Claude, Gemini, local models)
- ✅ Build a web interface with Streamlit or Flask

## Learn More

- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [LangChain for more complex agents](https://python.langchain.com/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)

---

GitHub Tutorial Hello World.
Old School Software Dev. New world of AI Agents should be interesting! 🚀
