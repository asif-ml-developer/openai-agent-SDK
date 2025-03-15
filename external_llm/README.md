# LLM Agent Configuration Approaches

This project demonstrates three different approaches to configuring and running a Language Model (LLM) agent using the `openai-agents` library. Each approach configures the LLM agent at a different level of granularity: **Agent Level**, **Run Level**, and **Global Level**. Below is a detailed explanation of each approach.

---

## 1. Agent Level

In this approach, the LLM agent is configured directly within the agent's definition. The model and provider are specified when creating the agent.

### Code Example

```python
import asyncio
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled

# Set up the provider (Gemini API)
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Disable tracing for cleaner output
set_tracing_disabled(disabled=True)

async def main():
    # Create an agent with a specific model and provider
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",  # Agent's behavior
        model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=provider),  # Model and provider
    )

    # Run the agent with a specific input
    result = await Runner.run(
        agent,
        "Tell me about recursion in programming.",
    )
    print(result.final_output)  # Print the agent's response

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())
