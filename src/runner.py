import os

# Load environment variables from .env into the system environment.
# This allows me to store secrets (like API keys) safely outside the code.
from dotenv import load_dotenv

# the OpenAI SDK.
# This is the client that actually sends requests to the model.
from openai import OpenAI


# Load .env file at import time.
# This ensures OPENAI_API_KEY is available before any client creation.
load_dotenv()


def get_client() -> OpenAI:
    """
    Create and return an OpenAI client instance.

    I separate this into its own function so:
    - API key logic is centralized
    - I can reuse it anywhere
    - I fail fast if the key is missing
    """

    # Read API key from environment.
    api_key = os.getenv("OPENAI_API_KEY")

    # If key is missing, stop immediately.
    # This prevents confusing runtime errors later.
    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY. Add it to your .env file.")

    # Return configured OpenAI client.
    return OpenAI(api_key=api_key)


def run_prompt(prompt: str, model: str, temperature: float) -> str:
    """
    Run a single prompt against a specified model.

    Args:
        prompt: The user input prompt.
        model: The model name (e.g., 'gpt-4o-mini').
        temperature: Controls randomness in generation.

    Returns:
        The model's text response as a clean string.
    """

    # Create a client for this call.
    # (Could optimize by creating once globally, but this keeps it simple and safe.)
    client = get_client()

    # Send chat completion request.
    resp = client.chat.completions.create(
        model=model,

        # Temperature controls randomness:
        # 0.0 → deterministic
        # higher → more varied responses
        temperature=temperature,

        # Messages follow chat format:
        # system = behavior instruction
        # user = actual question
        messages=[
            {"role": "system", "content": "Answer clearly and concisely."},
            {"role": "user", "content": prompt},
        ],
    )

    # Extract the assistant’s message content.
    # choices[0] = first response candidate.
    # Strip whitespace to normalize output.
    return resp.choices[0].message.content.strip()
