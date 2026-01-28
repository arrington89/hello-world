# Weather Agent Architecture

## System Overview

This document describes the architectural design of the Hello World Weather Agent.

## High-Level Architecture Diagram

```mermaid
flowchart TD
    User([User Input]) --> Agent[Agent Main Loop]
    Agent --> LoadEnv[Load Environment Variables]
    LoadEnv --> InitClient[Initialize Groq Client]
    InitClient --> ProcessMsg[Process User Message]
    
    ProcessMsg --> API1[API Call #1: Chat Completion]
    API1 --> CheckTools{Tool Call Needed?}
    
    CheckTools -->|No| DirectResponse[Return Direct Response]
    CheckTools -->|Yes| ExecuteTool[Execute Tool Function]
    
    ExecuteTool --> WeatherFunc[get_weather Function]
    WeatherFunc --> MockData[(Mock Weather Data)]
    MockData --> ToolResult[Tool Result JSON]
    
    ToolResult --> API2[API Call #2: Chat Completion with Tool Results]
    API2 --> FinalResponse[Generate Final Response]
    
    DirectResponse --> Output([Display to User])
    FinalResponse --> Output
    
    Output --> Loop{Continue?}
    Loop -->|Yes| Agent
    Loop -->|No| End([Exit])

    style Agent fill:#4CAF50
    style WeatherFunc fill:#2196F3
    style API1 fill:#FF9800
    style API2 fill:#FF9800
    style MockData fill:#9C27B0
```

## Component Breakdown

### 1. **User Interface Layer**
- **Terminal Input/Output**: Simple command-line interface for user interaction
- **Main Loop**: Continuous conversation loop until user exits
- **Input Validation**: Checks for exit commands and empty inputs

### 2. **Agent Core**
```mermaid
classDiagram
    class Agent {
        +client: OpenAI
        +tools: list
        +available_functions: dict
        +run_agent(message: str)
    }
    
    class MessageProcessor {
        +messages: list
        +process_request()
        +handle_tool_calls()
    }
    
    class ToolExecutor {
        +execute_function(name, args)
        +format_response(result)
    }
    
    Agent --> MessageProcessor
    Agent --> ToolExecutor
```

**Key Functions:**
- `run_agent(user_message)`: Main orchestration function
- Manages conversation context
- Handles API communication
- Coordinates tool execution

### 3. **LLM Integration Layer**
```mermaid
sequenceDiagram
    participant Agent
    participant Groq API
    participant Tools
    
    Agent->>Groq API: Send message + tool definitions
    Groq API-->>Agent: Response (may include tool calls)
    
    alt Tool Call Required
        Agent->>Tools: Execute function(args)
        Tools-->>Agent: Function result
        Agent->>Groq API: Send tool result
        Groq API-->>Agent: Final natural language response
    else Direct Response
        Agent-->>Agent: Use direct response
    end
```

**Features:**
- **Model**: Llama 3.3 70B (via Groq)
- **Function Calling**: Automatic tool selection
- **Context Management**: System + user messages
- **Error Handling**: API errors and quota issues

### 4. **Tool System**

#### Tool Definition Schema
```json
{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "Get current weather for a location",
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "City name"
        },
        "unit": {
          "type": "string",
          "enum": ["celsius", "fahrenheit"]
        }
      },
      "required": ["location"]
    }
  }
}
```

#### Weather Tool Implementation
```mermaid
flowchart LR
    Input[Location + Unit] --> Normalize[Normalize Location]
    Normalize --> Lookup[Lookup in Mock Data]
    Lookup --> Found{Found?}
    Found -->|Yes| Format[Format Response]
    Found -->|No| Default[Return Default Data]
    Format --> Output[JSON Response]
    Default --> Output
```

**Mock Data Structure:**
```python
{
    "location": "New York",
    "temperature": 72,
    "unit": "fahrenheit",
    "condition": "sunny",
    "humidity": 65
}
```

### 5. **Data Flow**

```mermaid
flowchart LR
    A[User Query] --> B{Parse Intent}
    B -->|Weather Query| C[Extract Location]
    B -->|General Query| D[Direct LLM Response]
    
    C --> E[Call get_weather]
    E --> F[Retrieve Mock Data]
    F --> G[Return JSON]
    G --> H[LLM Formats Response]
    
    D --> I[Natural Language]
    H --> I
    I --> J[Display to User]
```

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.10+ | Core implementation |
| **LLM Provider** | Groq | Free, fast API access |
| **LLM Model** | Llama 3.3 70B Versatile | Chat and function calling |
| **API Client** | OpenAI SDK | Groq-compatible client |
| **Config** | python-dotenv | Environment variable management |
| **Data Format** | JSON | Tool responses and API communication |

## Key Design Patterns

### 1. **Function Registry Pattern**
```python
available_functions = {
    "get_weather": get_weather
}
# Allows dynamic function lookup and execution
```

### 2. **Tool Abstraction Pattern**
- Tools defined declaratively (JSON schema)
- Execution separated from definition
- Easy to add new tools

### 3. **Message Context Pattern**
```python
messages = [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "...", "tool_calls": [...]},
    {"role": "tool", "content": "..."}
]
```

## Extensibility Points

### Adding New Tools
1. Define the tool function
2. Add function schema to `tools` list
3. Register in `available_functions` dict

### Example: Calculator Tool
```python
def calculate(expression: str) -> dict:
    result = eval(expression)  # Use safe eval in production!
    return {"expression": expression, "result": result}

# Add to tools list and available_functions
```

### Switching LLM Providers
- Change `base_url` in OpenAI client initialization
- Update `GROQ_API_KEY` → `OTHER_API_KEY`
- Adjust model name if needed

## Security Considerations

1. **API Key Management**
   - Stored in `.env` (not in version control)
   - Loaded via `python-dotenv`
   - Never logged or displayed

2. **Input Validation**
   - User inputs are passed to LLM (sandboxed)
   - Tool parameters validated by LLM

3. **Mock Data**
   - Weather tool uses simulated data
   - No external API calls (no data leakage)

## Performance Characteristics

- **First Response Time**: ~1-2 seconds
- **Tool Call Response**: ~2-3 seconds (includes function execution)
- **Groq Inference Speed**: Very fast (faster than OpenAI)
- **Rate Limits**: Groq free tier (6000 requests/minute)

## Future Enhancements

1. **Real Weather API Integration**
   - OpenWeatherMap, WeatherAPI, etc.
   - API key management for multiple services

2. **Conversation Memory**
   - Persistent message history
   - Context window management

3. **Multi-Tool Orchestration**
   - Chain multiple tool calls
   - Parallel tool execution

4. **Enhanced Error Handling**
   - Retry logic for API failures
   - Graceful degradation

5. **Web Interface**
   - Streamlit or Flask frontend
   - Chat history visualization
   - Real-time streaming responses

---

**Last Updated**: January 28, 2026
