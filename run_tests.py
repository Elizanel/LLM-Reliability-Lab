import argparse

# Import my structured test suites (math, confidence, etc.)
# This is basically my "benchmark dataset" in Python form.
from src.prompts import TEST_SUITES

# run_prompt is my thin wrapper around the OpenAI call.
# It takes (prompt, model, temperature) and returns a single string response.
from src.runner import run_prompt

# evaluate_responses calculates consistency + variance metrics
# across multiple runs of the same prompt.
from src.evaluator import evaluate_responses

# save_report writes the final benchmark output to a timestamped JSON file.
from src.report import save_report


def main():

    # CLI ARGUMENTS
    # I’m using argparse so I can run this tool like:
    # python main.py --suite math --model gpt-4o-mini --runs 10 --temperature 0.2
    parser = argparse.ArgumentParser(
        description="LLM Reliability Lab - CLI benchmark tool"
    )

    # Which suite of tests to run.
    # choices=TEST_SUITES.keys() prevents typos and keeps usage clean.
    parser.add_argument(
        "--suite",
        type=str,
        default="confidence",
        choices=TEST_SUITES.keys()
    )

    # Which model I want to benchmark.
    # This lets me swap models without editing code.
    parser.add_argument("--model", type=str, default="gpt-4o-mini")

    # How many times to run each prompt.
    # More runs = better reliability signal, but more cost/time.
    parser.add_argument("--runs", type=int, default=5)

    # Temperature controls randomness:
    # lower temp = more deterministic
    # higher temp = more variation
    parser.add_argument("--temperature", type=float, default=0.7)

    args = parser.parse_args()

    # Pull the list of tests for the selected suite.
    suite_items = TEST_SUITES[args.suite]

    # Store all results across all tests here so I can write one report file.
    all_results = []

    # Print a summary so I know what config I’m running.
    print(f"\nRunning suite: {args.suite}")
    print(f"Model: {args.model} | Runs: {args.runs} | Temp: {args.temperature}\n")

    
    # RUN EACH TEST CASE
    for item in suite_items:
        print(f"--- Test: {item['id']} ---")

        # Collect all responses from repeated runs of the same prompt.
        responses = []

        # Run the same prompt multiple times to measure stability.
        for i in range(args.runs):
            r = run_prompt(
                item["prompt"],
                model=args.model,
                temperature=args.temperature
            )

            # Save the raw response for later evaluation + reporting.
            responses.append(r)

            # Print only the first 120 chars so the terminal doesn’t get overwhelmed.
            print(f"Run {i+1}: {r[:120]}{'...' if len(r) > 120 else ''}")

        # EVALUATE THIS TEST
        # This computes:
        # - consistency_pct (how often the most common response appears)
        # - unique_responses (how many different outputs occurred)
        # - length_variance (how much response lengths fluctuate)
        metrics = evaluate_responses(responses)

        # Print metrics to the console so I can see results live.
        print(f"\nEvaluation:")
        print(f"Consistency: {metrics['consistency_pct']}%")
        print(f"Unique responses: {metrics['unique_responses']}")
        print(f"Length variance: {metrics['length_variance']}\n")

        # Save detailed results for this test.
        # I keep prompt + expected_behavior in the report for traceability.
        all_results.append({
            "test_id": item["id"],
            "prompt": item["prompt"],
            "expected_behavior": item.get("expected_behavior"),
            "responses": responses,
            "metrics": metrics
        })

  
    # BUILD FINAL REPORT PAYLOAD
    # This is the full benchmark output I will save to JSON.
    report = {
        "suite": args.suite,
        "model": args.model,
        "runs": args.runs,
        "temperature": args.temperature,
        "results": all_results
    }

    # Save report to disk under outputs/ with timestamp.
    out_path = save_report(report, args.suite)

    # Confirm where the file was saved.
    print(f"Saved report to: {out_path}\n")


# Standard Python entry point.
# This ensures main() only runs when file is executed directly.
if __name__ == "__main__":
    main()
