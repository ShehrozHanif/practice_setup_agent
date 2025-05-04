import os 
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel


load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

set_tracing_disabled(disabled=True)

MODEL = 'gemini/gemini-2.0-flash'

agent = Agent(
    name="Assistant",
    instructions="You only respond in haikus.",
    # model=LitellmModel(model=MODEL, api_key=api_key),
    model=LitellmModel(model=MODEL),

)

result = Runner.run_sync(agent, "Who is the founder of Pakistan?")
print(result.final_output)

