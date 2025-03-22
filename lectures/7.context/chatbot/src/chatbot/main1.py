import os
from dotenv import load_dotenv
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from agents.tool import function_tool

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in your .env file.")

# Define tools
@function_tool
@cl.step(type="weather tool")
def get_weather(location: str, unit: str = "C") -> str:
    """Fetch weather for a location."""
    return f"The weather in {location} is 22 degrees {unit}."

@function_tool
@cl.step(type="greeting tool")
def greet_user(greeting: str) -> str:
    """Greet the user."""
    return f"Hello there! You said: {greeting}"

# Set up chat starters
@cl.set_starters
async def set_starts():
    return [
        cl.Starter(label="Greetings", message="Hello! What can you help me with today?"),
        cl.Starter(label="Weather", message="Find the weather in Karachi."),
    ]

class MyContext:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.seen_messages = []

# Initialize chat session
@cl.on_chat_start
async def start():
    # Set up Gemini model
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    
    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash", openai_client=external_client
    )
    
    config = RunConfig(model=model, model_provider=external_client)
    
    # Create agent with tools
    agent = Agent(
        name="Assistant",
        tools=[greet_user, get_weather],
        instructions="You are a helpful assistant. Always greet the user when session starts.",
        model=model,
    )
    
    # Store in session
    cl.user_session.set("chat_history", [])
    cl.user_session.set("config", config)
    cl.user_session.set("agent", agent)
    
    await cl.Message(content="Welcome to the AI Assistant! How can I help you today?").send()

# Process messages
@cl.on_message
async def main(message: cl.Message):
    # Send thinking message
    msg = cl.Message(content="Thinking...")
    await msg.send()
    
    # Get agent and config from session
    agent = cl.user_session.get("agent")
    config = cl.user_session.get("config")
    history = cl.user_session.get("chat_history") or []
    
    # Add user message to history
    history.append({"role": "user", "content": message.content})
    
    my_ctx = MyContext(user_id="Zia")

    try:
        # Run the agent
        result = Runner.run_sync(agent, history, run_config=config, context=my_ctx)

        response_content = result.final_output
        
        # Update message with response
        msg.content = response_content
        await msg.update()
        
        # Update history
        history.append({"role": "assistant", "content": response_content})
        cl.user_session.set("chat_history", history)
        
    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()