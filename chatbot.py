import os
# from openai import OpenAI
from together import Together

# api_key = os.getenv("OPENAI_API_KEY")
api_key = os.getenv("TOGETHER_API_KEY")
# print(f"API key {api_key} loaded in correctly.")

# client = OpenAI(api_key=api_key)
client = Together(api_key=api_key) # auth defaults to os.environ.get("TOGETHER_API_KEY") but I did it manually
# print(f"Client: {client}")

response = client.chat.completions.create(
#     # model="gpt-4.1-nano-2025-04-14", # Paid OpenAI model
    model = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free", # Free TogetherAI model by Meta (https://api.together.xyz/models)
    messages=[
        {"role": "system", "content": "You are a fed up and sassy assistant who hates answering questions."},
        {"role": "user", "content": "What is the weather like today?"}
    ],
    temperature=0.7,
    max_tokens=100
)
# print(f"Response: {response}")
response_content = response.choices[0].message.content
print(f"Response content: {response_content}\n")