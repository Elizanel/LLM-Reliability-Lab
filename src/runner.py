import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY. Add it to your .env file.")
    return OpenAI(api_key=api_key)

def run_prompt(prompt: str, model: str, temperature: float) -> str:
    client = get_client()
    resp = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": "Answer clearly and concisely."},
            {"role": "user", "content": prompt},
        ],
    )
    return resp.choices[0].message.content.strip()