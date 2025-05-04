from agents import Agent, Runner, AsyncOpenAI,  set_default_openai_api
from agents import set_default_openai_client , set_tracing_disabled , function_tool
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


@function_tool
def std_detail(name: str) -> str:
    """
    This function returns the details of a student by name.
    """
    student = students.get(name)
    if not student:
        return f"No details found for {name}."
    return f"Name: {name}, Age: {student['age']} Roll No: {student['roll_no']} Class: {student['class_name']}"



# Moc data
students = {
    "Ali": {
        "age": 20,
        "roll_no": 12345,
        "class_name": "10th Grade"
    },
    "sam": {
        "age": 18,
        "roll_no": 1254,
        "class_name": "9th Grade"
    },
    "John": {
        "age": 22,
        "roll_no": 1234,
        "class_name": "12th Grade"
    }
}

# Agent
agent = Agent(
    name="Student Details",
    instructions="You only respond to student details.",
    model="gemini-2.0-flash",
    tools=[std_detail]
)


result = Runner.run_sync(agent, "tell me about sam.")
print(result.final_output)
