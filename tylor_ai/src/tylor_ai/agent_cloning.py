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
        name="Professional Poet",
        instructions="You are helpful assistant in poetry. Give me professional peom ",
        model=model,
    )
    # in cloning we only mentioned the change part all other details will be taken from orignal agent
    agent1 = agent.clone(
        name="Children Poet",
        instructions="You are helpful assistant in poetry. Give me Childish like poem",
    )

    
    result =await Runner.run(agent, "write poem on unity",  run_config=config)
    
    print(result.final_output)

    result =await Runner.run(agent1, "write poem on unity",  run_config=config)
    
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())