import argparse
from src.prompts import TEST_SUITES
from src.runner import run_prompt
from src.evaluator import evaluate_responses
from src.report import save_report

def main():
    parser = argparse.ArgumentParser(description="LLM Reliability Lab - CLI benchmark tool")
    parser.add_argument("--suite", type=str, default="confidence", choices=TEST_SUITES.keys())
    parser.add_argument("--model", type=str, default="gpt-4o-mini")
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--temperature", type=float, default=0.7)
    args = parser.parse_args()

    suite_items = TEST_SUITES[args.suite]

    all_results = []
    print(f"\nRunning suite: {args.suite}")
    print(f"Model: {args.model} | Runs: {args.runs} | Temp: {args.temperature}\n")

    for item in suite_items:
        print(f"--- Test: {item['id']} ---")
        responses = []
        for i in range(args.runs):
            r = run_prompt(item["prompt"], model=args.model, temperature=args.temperature)
            responses.append(r)
            print(f"Run {i+1}: {r[:120]}{'...' if len(r) > 120 else ''}")

        metrics = evaluate_responses(responses)
        print(f"\nEvaluation:")
        print(f"Consistency: {metrics['consistency_pct']}%")
        print(f"Unique responses: {metrics['unique_responses']}")
        print(f"Length variance: {metrics['length_variance']}\n")

        all_results.append({
            "test_id": item["id"],
            "prompt": item["prompt"],
            "expected_behavior": item.get("expected_behavior"),
            "responses": responses,
            "metrics": metrics
        })

    report = {
        "suite": args.suite,
        "model": args.model,
        "runs": args.runs,
        "temperature": args.temperature,
        "results": all_results
    }

    out_path = save_report(report, args.suite)
    print(f"Saved report to: {out_path}\n")

if __name__ == "__main__":
    main()