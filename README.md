
⸻

LLM Reliability Lab

A small CLI project where I experiment with how consistent large language models actually are.

I built this to better understand how models behave when you run the same prompt multiple times — especially when changing temperature and comparing different models.

This is not a production evaluation framework. It’s a learning project to explore reliability, variability, and basic benchmarking concepts in LLM systems.

⸻

Why I Built This

I’m trying to move deeper into AI engineering, and I realized I didn’t fully understand:
	•	What “temperature” really does
	•	How deterministic models are at low settings
	•	How much responses change across runs
	•	What “consistency” actually looks like in practice

So instead of just reading about it, I built a small testing tool.

This project helped me understand how AI teams might structure repeatable evaluations and compare model behavior.

⸻

What It Does
	•	Runs the same prompt multiple times
	•	Measures:
	•	Consistency percentage
	•	Number of unique responses
	•	Length variance
	•	Supports different test suites (math, confidence, etc.)
	•	Allows temperature adjustments
	•	Can compare multiple models
	•	Saves structured JSON reports

All through a simple CLI interface.

Example Usage

Run a single suite: python run_tests.py --suite math --runs 5 --temperature 0.2
Compare Models: python compare_models.py --suite math --models gpt-4o-mini,gpt-4o --runs 5 --temperature 0.2

What I Learned
	•	Lower temperature = more consistent outputs
	•	Higher temperature = more variability
	•	Even “simple” prompts can vary depending on phrasing
	•	Measuring reliability requires repetition
	•	Structured evaluation is different from just calling an API

This project helped me connect theory to actual behavior.

⸻

Tech Stack
	•	Python
	•	OpenAI API
	•	argparse (CLI interface)
	•	JSON reporting
	•	Custom evaluation logic