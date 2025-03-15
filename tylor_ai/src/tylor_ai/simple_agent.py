import asyncio
import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, function_tool, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig

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

def get_weather(city:str) -> str:
    return f"The weather in {city} is sunny"

async def main():
    agent = Agent(
        name="Assistance",
        instructions="You only respond dramatic fashion.",
        model=model,
        tools=[function_tool(get_weather)]
    )

    result = await Runner.run(agent, "How's the weather in Lahore?",  run_config=config)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())