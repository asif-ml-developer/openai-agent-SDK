import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
import chainlit as cl

load_dotenv(find_dotenv())

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("Gemini key is not set")

print (gemini_api_key)

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider,
)
config = RunConfig(
    model_provider=provider,
    model=model,
    tracing_disabled=True
)

agent= Agent(
    name="Assistance",
    instructions= "You are helpful Assistance"
)

@cl.on_message
async def main(message:cl.Message):
    
    result = await Runner.run(
        agent,
        input=message.content,
        run_config=config
    )
    mes=cl.Message(content=result.final_output)
    await mes.send()

# print(result.final_output)