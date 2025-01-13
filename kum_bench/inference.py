import argparse
import json
from datetime import datetime
from pathlib import Path

from datasets import load_dataset
from tqdm import tqdm

from kum_bench.api_model import (
    GEMINI_MODEL_NAMES,
    OPENAI_MODEL_NAMES,
    GeminiModel,
    OpenAIModel,
)
from kum_bench.prompts import INFERENCE_PROMPT_TEMPLATE

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, required=True)
    parser.add_argument("--output_dir", type=str, default="./outputs")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = (
        output_dir / f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{args.model_name}.json"
    )

    if args.model_name in OPENAI_MODEL_NAMES:
        model = OpenAIModel(args.model_name)
    elif args.model_name in GEMINI_MODEL_NAMES:
        model = GeminiModel(args.model_name)
    else:
        raise ValueError(f"Invalid model name: {args.model_name}")

    results = []

    dataset = load_dataset("Inoichan/KUM-Bench", split="test")
    for i, row in tqdm(enumerate(dataset), dynamic_ncols=True):
        year = row["year"]
        problem_number = row["problem_number"]
        question = row["question"]
        prompt = INFERENCE_PROMPT_TEMPLATE.format(question=question)

        response = model.generate(prompt, temperature=0.0, n_generations=1)
        results.append(
            {
                "year": year,
                "problem_number": problem_number,
                "question": question,
                "response": response,
            }
        )

    with open(output_file, "w") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
