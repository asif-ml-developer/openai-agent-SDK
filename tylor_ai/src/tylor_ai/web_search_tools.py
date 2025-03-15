import asyncio
import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, function_tool, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, trace
from agents.tool import WebSearchTool, UserLocation

load_dotenv(find_dotenv())

gemini_api_key=os.environ.get("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("api key is not working")
print(gemini_api_key)
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model =  OpenAIChatCompletionsModel(
    model= "gemini-1.5-flash",
    openai_client= provider
)

config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True,
)

async def main():
    agent = Agent(
        name="Web Searcher",
        instructions="You are helpful agent.",
        model=model,
        tools=[WebSearchTool(UserLocation(type="approximate", city="Lahore"))]  # not work with gemini 
    )

    with trace("Web Search Example"):
        result =await Runner.run(agent, "Search news for local sports",  run_config=config)
        print(result)
        
if __name__ == "__main__":
    asyncio.run(main())