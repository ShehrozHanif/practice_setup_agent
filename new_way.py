

from agents import Agent, Runner, AsyncOpenAI,  set_default_openai_api
from agents import set_default_openai_client , set_tracing_disabled
import os
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

gemini_api_key = os.getenv('GEMINI_API_KEY')
set_tracing_disabled(False)

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
set_default_openai_client(external_client)
set_default_openai_api("chat_completions")


web_agent: Agent = Agent(
                          name="Web Agent",
                          instructions="You only respond to website development related question",
                          model="gemini-2.0-flash",
                          handoff_description="Web Developer"
                        )


result = Runner.run_sync(web_agent, "tell me about web developer.",)


print(result.final_output)