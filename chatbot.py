import os
from together import Together

api_key = os.getenv("TOGETHER_API_KEY")

client = Together(api_key=api_key) # auth defaults to os.environ.get("TOGETHER_API_KEY") but I did it manually

MODEL = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free" # Free TogetherAI model by Meta (https://api.together.xyz/models)
TEMPERATURE = 0.7
MAX_TOKENS = 100
SYSTEM_PROMPT = "You are a fed up and sassy assistant who hates answering questions."
messages = [{"role": "system", "content": f"{SYSTEM_PROMPT}"}]


def chat(user_input):
    messages.append({"role": "user", "content": f"{user_input}"})

    response = client.chat.completions.create(
        model = MODEL,
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS
    )

    # print(f"Response: {response}")
    response_content = response.choices[0].message.content
    messages.append({"role": "assistant", "content": f"{response_content}"})
    return response_content


while True:
    user_input = input("User: ")
    if user_input.strip().lower() in {"exit", "quit"}:
        break
    chatbot_output = chat(user_input)
    print(f"Chatbot: {chatbot_output}")