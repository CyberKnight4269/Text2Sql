import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))

stream = client.interactions.create(
    model="gemini-3.8-flash",
    input="get all the names of the students from a sql table",
    stream=True
)

for event in stream:
    if event.event_type == "step.delta":
        if event.delta.type == "text":
            text = event.delta.text
            for char in text:
                print(char, end="", flush=True)
                time.sleep(0.01)