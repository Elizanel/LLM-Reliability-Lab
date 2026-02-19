from collections import Counter
import statistics


def evaluate_responses(responses: list[str]) -> dict:
    # Count how many times each exact response appears.
    # This helps measure consistency.
    counts = Counter(responses)

    # Get most common response + its frequency.
    most_common, freq = counts.most_common(1)[0]

    # Calculate consistency percentage.
    # Example: if 4 out of 5 runs are identical → 80%.
    consistency_pct = round((freq / len(responses)) * 100, 2)

    # Measure variation in response length.
    # This is a rough stability signal.
    lengths = [len(r) for r in responses]

    # Population variance of lengths.
    # If model outputs wildly different-length answers,
    # variance will be high.
    length_variance = (
        round(statistics.pvariance(lengths), 2)
        if len(lengths) > 1
        else 0.0
    )

    return {
        "most_common_response": most_common,
        "consistency_pct": consistency_pct,
        "unique_responses": len(counts),
        "length_variance": length_variance,
    }
