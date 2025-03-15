# mix for both agent and chainlit

import os
from dotenv import load_dotenv
from typing import cast
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig


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

from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant", model=model)

# result = Runner.run_sync(agent, "Hello, how are you.", run_config=config) #this adjusted below

# print("\nCALLING AGENT\n")

# print(result.final_output)


@cl.on_message

async def handle_message(message: cl.Message):
    result = await Runner.run(agent, input=message.content, run_config=config) # here place await and then Runner.run instead of Runner.sync
    await cl.Message(content=result.final_output).send()











# #this part is adjust in above

# @cl.on_message

# async def handle_message(message: cl.Message):
#     await cl.Message(content=f"Hello {message.content}").send()
