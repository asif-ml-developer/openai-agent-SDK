import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
import chainlit as cl



# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant", model=model)

# result = Runner.run_sync(agent, "Hello, how are you.", run_config=config)

print("\nCALLING AGENT\n")
# print(result.final_output)


@cl.on_chat_start
async def handle_start(): 
    cl.user_session.set("history", [])   # here it initialize history  
    await cl.Message(content="Welcome to the AI Assistant! How can I help you today?").send()
@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history") # here it get history
    history.append({"role": "user", "content": message.content})  # here it append user message
    result = await Runner.run(agent, input=history, run_config=config)
    history.append({"role": "assistant", "content": result.final_output}) # here it append assistant message
    cl.user_session.set("history", history) # here it update history
    mes1= cl.Message(content=result.final_output) 
    await mes1.send() # it is when send updated