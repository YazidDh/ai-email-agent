from langchain.agents import initialize_agent, Tool
from langchain_ollama.llms import OllamaLLM
from mcp.client.session import ClientSession
import asyncio


async def mcp_call(tool_name, params):
    """Call an MCP tool and return the result."""
    async with await ClientSession.connect("ws://localhost:8000") as session:
        result = await session.call_tool(tool_name, params)
        return result.output


def get_conversation(thread_id: str):
    """Sync wrapper to fetch email conversation via MCP."""
    return asyncio.run(mcp_call("get_conversation", {"thread_id": thread_id}))["formatted_conversation"]


# LLM setup
llm = OllamaLLM(model="qwen3:1.7b", temperature=0.1)

# Tool for the agent
tools = [
    Tool(
        name="Get Email Conversation",
        func=get_conversation,
        description="Fetch an email thread from Gmail by ID."
    )
]

# Initialize agent
agent = initialize_agent(tools, llm, agent_type="zero-shot-react-description", verbose=True)


def generate_reply(thread_id: str):
    """Generate a professional reply for the last email."""
    conv = get_conversation(thread_id)
    return agent.run(f"Write a professional reply to the last email in this conversation:\n{conv}")


# Example
if __name__ == "__main__":
    thread_id = "YOUR_THREAD_ID"
    print(generate_reply(thread_id))
