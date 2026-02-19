import argparse
import os
import sys

# I’m calculating the root of the project directory.
# This lets me run this script directly without import errors.
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

# Insert project root into Python path so imports like src.* work.
sys.path.insert(0, PROJECT_ROOT)

# This function runs an entire suite against one model.
from run_tests import run_suite  # noqa: E402

# This saves the final results to a JSON report file.
from src.report import save_report  # noqa: E402


def main():
    # I’m using argparse so I can run this from the command line like:
    # python compare.py --suite math --models gpt-4o-mini,gpt-4.1-mini
    parser = argparse.ArgumentParser(
        description="Compare multiple models on the same test suite"
    )

    # Which suite to run (math, confidence, etc.)
    parser.add_argument("--suite", type=str, default="math")

    # Required because I must provide at least one model.
    parser.add_argument(
        "--models",
        required=True,
        help="Comma-separated models (e.g., gpt-4o-mini,gpt-4.1-mini)"
    )

    # How many times to run each prompt.
    parser.add_argument("--runs", type=int, default=5)

    # Controls randomness in generation.
    parser.add_argument("--temperature", type=float, default=0.7)

    args = parser.parse_args()

    # Convert comma-separated string into clean list of models.
    models = [m.strip() for m in args.models.split(",") if m.strip()]

    if not models:
        raise ValueError("No models provided. Use --models modelA,modelB")

    print("\n==============================")
    print(f"Model comparison: suite={args.suite} | runs={args.runs} | temp={args.temperature}")
    print("==============================\n")

    results_by_model = {}

    # Loop through each model and benchmark it.
    for m in models:
        print(f"\n### Running model: {m}")

        # Run entire suite for this model.
        res = run_suite(args.suite, m, args.runs, args.temperature, print_runs=False)

        # Store results under model name.
        results_by_model[m] = res

        overall = res["overall"]

        # Print summary metrics for quick comparison.
        print(
            f"- avg_consistency_pct: {overall['avg_consistency_pct']}%\n"
            f"- avg_unique_responses: {overall['avg_unique_responses']}\n"
            f"- avg_length_variance: {overall['avg_length_variance']}\n"
        )

    # Save full comparison report.
    payload = {
        "suite": args.suite,
        "runs": args.runs,
        "temperature": args.temperature,
        "models": models,
        "results": results_by_model,
    }

    path = save_report(payload, filename_prefix=f"compare_{args.suite}")
    print(f"Saved comparison report to: {path}")

    # Simple winner logic:
    # Highest consistency wins.
    # If tie → lowest unique responses wins.
    scored = []
    for m in models:
        o = results_by_model[m]["overall"]
        scored.append((m, o["avg_consistency_pct"], o["avg_unique_responses"]))

    scored.sort(key=lambda x: (-x[1], x[2]))
    winner = scored[0][0]

    print(f"\nWinner (simple heuristic): {winner}\n")


if __name__ == "__main__":
    main()
