# mutliple agents wiht tracing

import asyncio
import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, function_tool, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, enable_verbose_stdout_logging
from pydantic import BaseModel

# import and enable verbose to get whole details of process
enable_verbose_stdout_logging()



load_dotenv(find_dotenv())

# uv add agnetops
# login agent ops https://app.agentops.ai/projects
import agentops
agentops_api_key=os.environ.get("AGENTOPS_API_KEY")
print(agentops_api_key)
session=agentops.init(api_key=agentops_api_key)

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
    # tracing_disabled=True,

)

class HomeworkOutput(BaseModel):
    is_homework: bool
    resoning:str

math_tutor_agent = Agent(
    name="Math Tutor",      
    handoff_description= "Specialist agent for Math Question",
    instructions= "You provide assistance with historical queries. Explain important events and context clearly."
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries, Explain improtant events and context clearly.",
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determin which agent to use based on the user's question",
    handoffs=[history_tutor_agent, math_tutor_agent]
)


async def main():
    
    result = await Runner.run(triage_agent, "Let me know about Pakistan", run_config=config)
    print(result.final_output)

    # agentops session success will close here
    session.end_session("Success")

if __name__ == "__main__":
    asyncio.run(main())