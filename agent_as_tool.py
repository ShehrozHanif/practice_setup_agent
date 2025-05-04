
from agents import Agent, Runner, AsyncOpenAI,  set_default_openai_api
from agents import set_default_openai_client , set_tracing_disabled
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

gemini_api_key = os.getenv('GEMINI_API_KEY')
set_tracing_disabled(True)

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
set_default_openai_client(external_client)
set_default_openai_api("chat_completions")

model = "gemini-2.0-flash"


# 🗣️ Spanish Agent
spanish_agent = Agent(
    name="Spanish Agent",
    instructions="You translate the user's message to Spanish.",
    model=model
)

# 🗣️ French Agent
french_agent = Agent(
    name="French Agent",
    instructions="You translate the user's message to French.",
    model=model
)


orchestrator_agent = Agent(
    name="Orchestrator Agent",
    instructions="You are a translation agent. Use the tools provided to translate as requested.",
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate input to Spanish."
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translate input to French."
        )
    ],
    model=model
)


async def main():
    result = await Runner.run(
        orchestrator_agent,
        input="Say 'Hello, how are you?' in Spanish."
    )
    print("🟢 Final Output:\n", result.final_output)
    print("🔵 Last Agent:\n", result.last_agent.name)

# Entry point
if __name__ == "__main__":
    asyncio.run(main())