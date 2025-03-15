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
    model= "gemini-2.0-flash",
    openai_client= provider
)

config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True,
)

async def main():
    agent = Agent(
        name="Poet",
        instructions="You are helpful assistant in poetry.",
        model=model,
    )

    """
    below code is in video not running
    # result =Runner.run_streamed(agent, "write poem on 5 different topics",  run_config=config)
    # async for event in result.stream_events():
    #     # print(event)
    #     if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
    #         print(event.data.delta, end="", flush=True)
    """

    
    result =Runner.run_streamed(agent, "write poem on 5 different topics",  run_config=config)
    async for event in result.stream_events():
        print(event)

if __name__ == "__main__":
    asyncio.run(main())