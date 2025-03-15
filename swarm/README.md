# OpenAI Swarm Framework & Agents SDK

## **Swarm Framework**
- **Purpose**: Lightweight, experimental framework for orchestrating multi-agent systems.
- **Key Abstractions**:
  1. **Agents**: Autonomous entities with specific tasks and tools.
  2. **Handoffs**: Mechanism to transfer control between agents based on context.
- **Example**: In customer service, different agents handle billing, tech support, and general inquiries. If a general agent detects a billing issue, it hands off to the billing agent.

## **Agents SDK**
- **Evolution**: Production-ready version of Swarm, enhancing multi-agent orchestration.
- **Features**: Scalable, testable, and efficient coordination of agents for complex tasks.

## **Anthropic Design Patterns in Agents SDK**
1. **Prompt Chaining**: Break tasks into sequential steps, executed by agents in order.
2. **Routing**: Direct tasks to the most suitable agent using handoffs.
3. **Parallelization**: Execute multiple subtasks concurrently for efficiency.
4. **Orchestrator-Workers**: Orchestrator agent breaks tasks and assigns them to worker agents.
5. **Evaluator-Optimizer**: Evaluator agent assesses performance and suggests improvements.

## **Summary**
- **Swarm**: Experimental, lightweight multi-agent orchestration.
- **Agents SDK**: Advanced, production-ready framework based on Swarm, integrating Anthropic design patterns for efficient AI agent systems.