import argparse
import os
import sys


PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

from run_tests import run_suite  # noqa: E402
from src.report import save_report  # noqa: E402

def main():
    parser = argparse.ArgumentParser(description="Compare multiple models on the same test suite")
    parser.add_argument("--suite", type=str, default="math")
    parser.add_argument("--models", required=True, help="Comma-separated models (e.g., gpt-4o-mini,gpt-4.1-mini)")
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--temperature", type=float, default=0.7)
    args = parser.parse_args()

    models = [m.strip() for m in args.models.split(",") if m.strip()]
    if not models:
        raise ValueError("No models provided. Use --models modelA,modelB")

    print("\n==============================")
    print(f"Model comparison: suite={args.suite} | runs={args.runs} | temp={args.temperature}")
    print("==============================\n")

    results_by_model = {}
    for m in models:
        print(f"\n### Running model: {m}")
        res = run_suite(args.suite, m, args.runs, args.temperature, print_runs=False)
        results_by_model[m] = res

        overall = res["overall"]
        print(
            f"- avg_consistency_pct: {overall['avg_consistency_pct']}%\n"
            f"- avg_unique_responses: {overall['avg_unique_responses']}\n"
            f"- avg_length_variance: {overall['avg_length_variance']}\n"
        )

    payload = {
        "suite": args.suite,
        "runs": args.runs,
        "temperature": args.temperature,
        "models": models,
        "results": results_by_model,
    }

    path = save_report(payload, filename_prefix=f"compare_{args.suite}")
    print(f"Saved comparison report to: {path}")

    # Simple winner logic: highest avg consistency, tie-breaker lowest avg unique responses
    scored = []
    for m in models:
        o = results_by_model[m]["overall"]
        scored.append((m, o["avg_consistency_pct"], o["avg_unique_responses"]))

    scored.sort(key=lambda x: (-x[1], x[2]))
    winner = scored[0][0]
    print(f"\nWinner (simple heuristic): {winner}\n")

if __name__ == "__main__":
    main()