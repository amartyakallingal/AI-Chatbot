import os
from together import Together
import tiktoken

api_key = os.getenv("TOGETHER_API_KEY")

client = Together(api_key=api_key) # auth defaults to os.environ.get("TOGETHER_API_KEY") but I did it manually

MAX_TOKENS = 200
MODEL = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free" # Free TogetherAI model by Meta (https://api.together.xyz/models)
SYSTEM_PROMPT = "You are a working-class Italian-American man from the 1960s living in Brooklyn."
TEMPERATURE = 0.7
TOKEN_BUDGET = 1000

messages = [{"role": "system", "content": f"{SYSTEM_PROMPT}"}]


def get_model_encoding(model):
    try:
        return tiktoken.encoding_for_model(model)
    except KeyError:
        print(f"Warning: Tokenizer for model {model} not found --> falling back to 'cl100k_base' encoding")
        return tiktoken.get_encoding("cl100k_base")
    

ENCODING = get_model_encoding(MODEL)


def count_tokens(message):
    return len(ENCODING.encode(message))


def total_tokens_used(messages):
    try:
        return sum(count_tokens(message["content"]) for message in messages)
    except Exception as e:
        print(f"Error finding total tokens used: {e}")
        raise


def enforce_token_budget(messages, budget=TOKEN_BUDGET):
    try:
        while total_tokens_used(messages) > budget:
            if len(messages) <= 2:
                break
            messages.pop(1) # Keeps system message (index 0 of list) but removes oldest user/assistant message when current tokens exceeds budget
    except Exception as e:
        print(f"Error enforcing token budget: {e}")
        raise


def chat(user_input):
    messages.append({"role": "user", "content": f"{user_input}"})

    response = client.chat.completions.create(
        model = MODEL,
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS
    )

    response_content = response.choices[0].message.content
    messages.append({"role": "assistant", "content": f"{response_content}"})

    enforce_token_budget(messages)

    return response_content


while True:
    user_input = input("User: ")
    if user_input.strip().lower() in {"exit", "quit"}:
        break
    chatbot_output = chat(user_input)
    print(f"Chatbot: {chatbot_output}")
    print(f"Current tokens used: {total_tokens_used(messages)}")