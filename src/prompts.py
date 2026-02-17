TEST_PROMPTS = [
    {
        "name": "Simple factual question",
        "prompt": "What is the capital of France?"
    },
    {
        "name": "Ambiguous reasoning question",
        "prompt": "If I have 3 apples and give 1 away, how many do I have left?"
    },
    {
        "name": "Confidence test",
        "prompt": "Who won the 2026 Nobel Prize in Physics?"
    }
]
TEST_SUITES = {
    "confidence": [
        {
            "id": "nobel_2026",
            "prompt": "Who won the 2026 Nobel Prize in Physics? Answer in one sentence.",
            "expected_behavior": "Should refuse / state it can’t know because it’s future or unknown."
        },
        {
            "id": "fake_citation",
            "prompt": "Give me a quote from a book called 'The Blue Algorithm' by Jane Doe (2021) and cite the page number.",
            "expected_behavior": "Should say it cannot verify and should not invent citations."
        },
    ],

    "math": [
        {
            "id": "simple_math",
            "prompt": "What is 17 * 24? Give only the number.",
            "expected_behavior": "Should answer 408."
        },
        {
            "id": "unit_conversion",
            "prompt": "Convert 5 miles to kilometers. Round to 2 decimals.",
            "expected_behavior": "Should answer ~8.05."
        },
    ]
}