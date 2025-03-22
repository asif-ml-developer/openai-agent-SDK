import asyncio
import os
from dataclasses import dataclass
from dotenv import load_dotenv
from agents import (
    Agent,
    RunContextWrapper,
    Runner,
    function_tool,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    RunConfig,
)

# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is missing in .env file.")

# Set up the Gemini API client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Define the model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash", openai_client=external_client
)

# Define RunConfig
config = RunConfig(
    model=model, model_provider=external_client, tracing_disabled=True
)

# Define a UserInfo object
@dataclass
class UserInfo:
    name: str
    uid: int


# Define a tool to fetch user age
@function_tool
async def fetch_user_age(wrapper: RunContextWrapper[UserInfo]) -> str:
    print("DEBUG: Inside fetch_user_age()")
    print(f"DEBUG: Context received - {wrapper.context}")
    
    if not wrapper.context:
        return "Error: User information is missing."

    return f"User {wrapper.context.name} is 47 years old."


async def main():
    user_info = UserInfo(name="John", uid=123)
    print(f"DEBUG: Context being sent - {user_info}")

    agent = Agent[UserInfo](name="Assistant", tools=[fetch_user_age])

    result = await Runner.run(
        starting_agent=agent,
        input="Please use the fetch_user_age tool to tell me the age of the user. No need for additional arguments as the context is already available.",
        context=user_info,
        run_config=config,
    )

    print(f"DEBUG: Final Output - {result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())
