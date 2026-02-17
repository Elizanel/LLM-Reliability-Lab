from collections import Counter
import statistics

def evaluate_responses(responses: list[str]) -> dict:
    # Most common response + consistency
    counts = Counter(responses)
    most_common, freq = counts.most_common(1)[0]
    consistency_pct = round((freq / len(responses)) * 100, 2)

    # Length stats (rough “variance” proxy)
    lengths = [len(r) for r in responses]
    length_variance = round(statistics.pvariance(lengths), 2) if len(lengths) > 1 else 0.0

    return {
        "most_common_response": most_common,
        "consistency_pct": consistency_pct,
        "unique_responses": len(counts),
        "length_variance": length_variance,
    }