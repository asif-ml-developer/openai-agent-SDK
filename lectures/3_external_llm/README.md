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

## Key Points for Each Approach

### 1. Agent Level
- **Agent Configuration**: The model and provider are directly specified when creating the `Agent` object.
- **Behavior**: The agent is instructed to respond only in haikus.
- **Run**: The agent is run asynchronously using `Runner.run`.

### 2. Run Level
- **Run Configuration**: The model, provider, and tracing are specified in a `RunConfig` object.
- **Flexibility**: The same agent can be run with different configurations.
- **Run**: The agent is run synchronously using `Runner.run_sync`.

### 3. Global Level
- **Global Configuration**: The provider is set globally using `set_default_openai_client`.
- **Default Behavior**: Any agent created afterward will use the default provider and model unless specified otherwise.
- **Run**: The agent is run synchronously without needing to specify a run configuration.

---

## Summary of Differences

| **Approach**   | **Configuration Level** | **Flexibility** | **Use Case** |
|----------------|-------------------------|-----------------|--------------|
| **Agent Level** | Directly in the agent's definition | Low | Specific agent behavior |
| **Run Level**   | At runtime using `RunConfig` | High | Flexible, same agent with different configurations |
| **Global Level**| Globally for the entire project | Medium | Default provider for all agents |

---

## Key Concepts for Beginners

- **Provider**: The service that provides the LLM (e.g., Gemini API).
- **Model**: The specific LLM being used (e.g., `gemini-2.0-flash`).
- **Agent**: The entity that interacts with the user, using the LLM to generate responses.
- **Configuration**: Settings like the model, provider, and tracing can be specified at different levels (agent, run, or globally).
- **Synchronous vs Asynchronous**: Synchronous code runs sequentially, while asynchronous code can handle multiple tasks concurrently.

By understanding these approaches, you can choose the best way to configure and run your LLM agent based on your needs.

---

## Installation

To run the code, you need to install the `openai-agents` library. Use the following command:

```bash
pip install -Uq openai-agents
