import os

# Official OpenAI Python SDK.
# This is what actually sends requests to the model.
from openai import OpenAI

# Loads environment variables from my .env file.
# This keeps my API key out of the codebase.
from dotenv import load_dotenv

# TEST_PROMPTS is a list of evaluation scenarios.
# Each contains a name + prompt string.
from prompts import TEST_PROMPTS

# This function calculates consistency + variance metrics.
from evaluator import evaluate_responses

# Env Setup

# Load variables from .env into environment.
# This makes OPENAI_API_KEY available via os.getenv().
load_dotenv()

# Create OpenAI client once.
# If the API key is missing, this will fail when I try to call the model.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Run a Prompt Multiple Times

def run_prompt(prompt, runs=5):
    """
    Run the same prompt multiple times against the model.
    This lets me measure output consistency and variability.
    """

    # Store all responses here.
    responses = []

    # Run the prompt N times.
    for i in range(runs):

        # Call OpenAI chat completion endpoint.
        response = client.chat.completions.create(
            model="gpt-4o-mini",

            # I include a short system instruction
            # to encourage concise, structured answers.
            messages=[
                {"role": "system", "content": "Answer clearly and concisely."},
                {"role": "user", "content": prompt}
            ],

            # Temperature controls randomness.
            # Higher = more variation between runs.
            temperature=0.7
        )

        # Extract model response text.
        content = response.choices[0].message.content.strip()

        # Save response for later analysis.
        responses.append(content)

    return responses



# Main Benchmark Loop

def main():
    """
    Loop through each test case and:
    1. Run the prompt multiple times
    2. Print responses
    3. Evaluate consistency metrics
    """

    for test in TEST_PROMPTS:

        print("\n==============================")
        print(f"Running test: {test['name']}")
        print("==============================")

        # Run prompt multiple times.
        responses = run_prompt(test["prompt"])

        # Print each run result.
        for i, r in enumerate(responses):
            print(f"\nRun {i+1}: {r}")

        # Evaluate responses for consistency + stability.
        results = evaluate_responses(responses)

        print("\n--- Evaluation ---")

        # Most common answer across runs.
        print(f"Most common response: {results['most_common_response']}")

        # % of runs that matched the most common answer.
        # Higher = more stable model behavior.
        print(f"Consistency rate: {results['consistency_rate']}")

        # Variation in output length.
        # Higher variance may indicate unstable reasoning.
        print(f"Length variance: {results['length_variance']}")


# Standard Python entry point.
# Ensures main() only runs if this file is executed directly.
if __name__ == "__main__":
    main()

