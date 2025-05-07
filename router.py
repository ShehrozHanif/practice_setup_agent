import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

open_router_key = os.getenv("OPENROUTER_API_KEY")

# Check if the API key is present; if not, raise an error
if not open_router_key:
    raise ValueError("OPEN_ROUTER_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://openrouter.ai/docs/quickstart

BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "google/learnlm-1.5-pro-experimental:free"

# Some other free models on 26th March:
# https://openrouter.ai/deepseek/deepseek-chat-v3-0324:free
# https://openrouter.ai/google/gemini-2.5-pro-exp-03-25:free


# import requests
# import json

# response = requests.post(
#   url=f"https://openrouter.ai/api/v1/chat/completions",
#   headers={
#     "Authorization": f"Bearer {open_router_key}",
#   },
#   data=json.dumps({
#     "model": MODEL,
#     "messages": [
#       {
#         "role": "user",
#         "content": "as a model tell me your speciality which i can use"
#       }
#     ]
#   })
# )

# print(response.json())

# data = response.json()
# final_output= data['choices'][0]['message']['content']
# print("\nFinal Output\n", final_output)



# Now Implementing into OpenAI-Agent-SDK

import asyncio
from openai import AsyncOpenAI # chat completions
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled

set_tracing_disabled(disabled=True) # Open AI Tracing == Disable

client = AsyncOpenAI(
    api_key=open_router_key,
    base_url=BASE_URL
)


async def main():
    # This agent will use the custom LLM provider
    agent = Agent(
        name="jARVIS",
        instructions="You only respond in english.",
        model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
    )

    result = await Runner.run(
        agent, # starting agent
        "What is your name?.", # request
    )
    print(result.final_output)
    print(result.last_agent.name) # agent name


asyncio.run(main())