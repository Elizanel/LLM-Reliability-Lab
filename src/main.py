import os
from openai import OpenAI
from dotenv import load_dotenv
from prompts import TEST_PROMPTS
from evaluator import evaluate_responses

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_prompt(prompt, runs=5):
    responses = []

    for i in range(runs):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Answer clearly and concisely."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        content = response.choices[0].message.content.strip()
        responses.append(content)

    return responses


def main():
    for test in TEST_PROMPTS:
        print("\n==============================")
        print(f"Running test: {test['name']}")
        print("==============================")

        responses = run_prompt(test["prompt"])

        for i, r in enumerate(responses):
            print(f"\nRun {i+1}: {r}")

        results = evaluate_responses(responses)

        print("\n--- Evaluation ---")
        print(f"Most common response: {results['most_common_response']}")
        print(f"Consistency rate: {results['consistency_rate']}")
        print(f"Length variance: {results['length_variance']}")


if __name__ == "__main__":
    main()