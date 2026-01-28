"""
Hello World AI Agent with Weather Tool
A simple AI agent that can answer questions and check the weather
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client (uses OpenAI-compatible API)
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# Define the weather tool
def get_weather(location: str, unit: str = "fahrenheit") -> dict:
    """
    Simulated weather tool - returns mock weather data.
    In a real application, this would call a weather API like OpenWeatherMap.
    """
    # Mock weather data for demonstration
    weather_data = {
        "new york": {"temp": 72, "condition": "sunny", "humidity": 65},
        "london": {"temp": 58, "condition": "cloudy", "humidity": 80},
        "tokyo": {"temp": 68, "condition": "rainy", "humidity": 75},
        "paris": {"temp": 62, "condition": "partly cloudy", "humidity": 70},
    }
    
    location_lower = location.lower()
    
    if location_lower in weather_data:
        data = weather_data[location_lower]
        return {
            "location": location,
            "temperature": data["temp"],
            "unit": unit,
            "condition": data["condition"],
            "humidity": data["humidity"]
        }
    else:
        return {
            "location": location,
            "temperature": 70,
            "unit": unit,
            "condition": "unknown",
            "humidity": 50,
            "note": "Weather data not available for this location (simulated data returned)"
        }

# Define available tools for the AI
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a specific location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city name, e.g., 'New York', 'London'"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The temperature unit to use"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

# Map function names to actual functions
available_functions = {
    "get_weather": get_weather
}

def run_agent(user_message: str):
    """
    Main agent function that processes user messages and handles tool calls
    """
    print(f"\n🤖 Agent: Processing your request...\n")
    
    # System prompt with strict guardrails
    system_prompt = """You are a specialized Weather Assistant. Your ONLY purpose is to provide weather information.

STRICT RULES:
1. You can ONLY answer questions about weather, temperature, climate, and atmospheric conditions
2. You MUST refuse to answer ANY questions about:
   - General knowledge, facts, or trivia
   - Programming, coding, or technical help
   - Math calculations or conversions (unless weather-related)
   - Current events, news, or politics
   - Entertainment, sports, or celebrities
   - Personal advice or opinions
   - ANY topic not directly related to weather

3. For weather queries, use the get_weather tool to provide information
4. If asked a non-weather question, politely respond: "I'm a specialized weather assistant and can only help with weather-related questions. Please ask me about the weather in any location!"

Be friendly but firm about your limitations. Always redirect users to ask about weather."""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
    
    # First API call
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    
    # Check if the agent wants to call a tool
    if tool_calls:
        messages.append(response_message)
        
        # Execute each tool call
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"🔧 Calling tool: {function_name} with args: {function_args}")
            
            # Call the actual function
            function_response = available_functions[function_name](**function_args)
            
            # Add the function response to messages
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": json.dumps(function_response)
            })
        
        # Get final response from the agent
        second_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )
        
        return second_response.choices[0].message.content
    else:
        # No tool call needed, return direct response
        return response_message.content

def main():
    """
    Main function to run the interactive agent
    """
    print("=" * 60)
    print("�️  Weather Assistant - Weather Info Only! 🌤️")
    print("=" * 60)
    print("\n⚠️  IMPORTANT: I can ONLY answer weather-related questions!")
    print("\nAsk me about:")
    print("  ✅ Weather conditions in any city")
    print("  ✅ Temperature, humidity, forecasts")
    print("  ✅ Climate information")
    print("\nI CANNOT answer:")
    print("  ❌ General knowledge questions")
    print("  ❌ Programming or tech support")
    print("  ❌ Math problems (unless weather-related)")
    print("  ❌ Any non-weather topics")
    print("\nExamples:")
    print("  - What's the weather in New York?")
    print("  - Tell me the temperature in London")
    print("  - Compare weather in Tokyo and Paris")
    print("\nType 'quit' or 'exit' to end the conversation.\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye! Stay weather-aware!")
            break
        
        if not user_input:
            continue
        
        try:
            response = run_agent(user_input)
            print(f"\n🤖 Agent: {response}\n")
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            print("Make sure your GROQ_API_KEY is set correctly in .env file")

if __name__ == "__main__":
    main()
